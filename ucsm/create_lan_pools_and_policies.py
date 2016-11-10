import sys
import json
import csv
from ucsmsdk import ucshandle

if __name__ == "__main__":
    try:
        if len(sys.argv) < 3:
            print "Usage: %s <JSON settings file> <csv file>" % sys.argv[0]
            print "       <settings file>:   access settings (IP/user/password)"
            print "       <csv file>: settings for MAC pools, VLANs, vNICs, etc."
            sys.exit(0)
        f = open(sys.argv[1], 'r')
        settings_file = json.load(f)
	is_secure = True
	if settings_file['secure'] == "False":
	    is_secure = False
        handle = ucshandle.UcsHandle(settings_file['ip'], settings_file['user'], settings_file['pw'], secure=is_secure)
        handle.login()

        # apply hardcoded policies
        from ucsmsdk.mometa.nwctrl.NwctrlDefinition import NwctrlDefinition
        from ucsmsdk.mometa.dpsec.DpsecMac import DpsecMac

        mo = NwctrlDefinition(parent_mo_or_dn="org-root", lldp_transmit="disabled", name="Enable_CDP", lldp_receive="disabled", mac_register_mode="only-native-vlan", policy_owner="local", cdp="enabled", uplink_fail_action="link-down", descr="")
        mo_1 = DpsecMac(parent_mo_or_dn=mo, forge="allow", policy_owner="local", name="", descr="")
        handle.add_mo(mo)

        handle.commit()

        # setup ext-mgmt IP pool
        from ucsmsdk.mometa.ippool.IppoolBlock import IppoolBlock

        mo = IppoolBlock(parent_mo_or_dn="org-root/ip-pool-ext-mgmt", to="192.168.1.199", r_from="192.168.1.100", def_gw="192.168.1.1")
        handle.add_mo(mo)

        handle.commit()

        # apply settings from each row in the csv file
        csv_filename = sys.argv[2]
        csv_file = open(csv_filename, "r")
        if not csv_file:
            print "Error: could not open %s" % csv_filename
            sys.exit(1)
        csv_reader = csv.DictReader(csv_file)
        row_num = 1
        for row in csv_reader:
            row_num += 1
	    
            # set org (org-root as default)
	    if row['org']:
	        org = row['org']
	    else:
	        org = 'org-root'
            if row['MAC_pool'] and row['MAC_From'] and row['MAC_To']:
                # create MAC pool
                from ucsmsdk.mometa.macpool.MacpoolPool import MacpoolPool
                from ucsmsdk.mometa.macpool.MacpoolBlock import MacpoolBlock

                mo = MacpoolPool(parent_mo_or_dn=org, policy_owner="local", descr="", assignment_order="default", name=row['MAC_pool'])
                mo_1 = MacpoolBlock(parent_mo_or_dn=mo, to=row['MAC_To'], r_from=row['MAC_From'])
                handle.add_mo(mo)

                handle.commit()
            if row['VLAN'] and row['VLAN_ID']:
                # create vLANs
                from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan

                # create a range if needed based on all VLANs given in VLAN_ID
	        vlanList = row['VLAN_ID'].split('-')
                vlansStart = int(vlanList[0])
	        if len(vlanList) > 1:
                    vlansEnd = int(vlanList[1])
	        else:
	            vlansEnd = vlansStart
	        for vlan in range(vlansStart, vlansEnd+1):
		    vlanName = "%s%d" % (row['VLAN'], vlan)

		    mo = FabricVlan(parent_mo_or_dn="fabric/lan", sharing="none", name=vlanName, id=str(vlan), mcast_policy_name="", policy_owner="local", default_net="no", pub_nw_name="", compression_type="included")

	            handle.add_mo(mo)
                handle.commit()
	    if row['vNIC_Template'] and row['vNIC_Fabric'] and row['vNIC_VLAN'] and row['vNIC_Native_VLAN'] and row ['vNIC_MTU'] and row['vNIC_MAC']:
	        # create vNIC templates
                from ucsmsdk.mometa.vnic.VnicLanConnTempl import VnicLanConnTempl
                from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf

                mo = VnicLanConnTempl(parent_mo_or_dn=org, templ_type="updating-template", name=row['vNIC_Template'], descr="", stats_policy_name="default", admin_cdn_name="", switch_id=row['vNIC_Fabric'], pin_to_group_name="", mtu=row['vNIC_MTU'], policy_owner="local", qos_policy_name="", ident_pool_name=row['vNIC_MAC'], cdn_source="vnic-name", nw_ctrl_policy_name="Enable_CDP")
		# allow multiple vlans if specified as a list in the csv
		# note that native vlan is set globally, so native  only works here if a single VLAN is specified
		for vlans in [row['vNIC_VLAN']]:
		    vlans = vlans.split(',')
		    for vlan in vlans:
		        # strip unnecessary characters
	                vlan = vlan.strip(' ')
	                vlan = vlan.strip('\"')
                        mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net=row['vNIC_Native_VLAN'], name=vlan)

                handle.add_mo(mo)
                handle.commit()
	    if row['LAN_Policy'] and row['vNIC_Name'] and row['vNIC_Order'] and row['LAN_Policy_vNIC_Template']:
	        # LAN Connectivity policy
                from ucsmsdk.mometa.vnic.VnicLanConnPolicy import VnicLanConnPolicy
                from ucsmsdk.mometa.vnic.VnicEther import VnicEther

                # if policy doesn't exist, create it
		dn = org + '/lan-conn-pol-' + row['LAN_Policy']
		mo = handle.query_dn(dn)
		if not mo:
                    mo = VnicLanConnPolicy(parent_mo_or_dn=org, policy_owner="local", name=row['LAN_Policy'], descr="")
                # add vnic and set vcon and vcon order.  Policy is always "Linux"
                mo_1 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", admin_cdn_name="", switch_id="NONE", pin_to_group_name="", name=row['vNIC_Name'], order=row['vNIC_Order'], qos_policy_name="", adaptor_profile_name="Linux", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name=row['LAN_Policy_vNIC_Template'], addr="derived")

                handle.add_mo(mo, modify_present=True)
                handle.commit()
	handle.logout()

    except Exception, err:
        print "Exception:", str(err)
	import traceback, sys
	print '-'*60
	traceback.print_exc(file=sys.stdout)
	print '-'*60

