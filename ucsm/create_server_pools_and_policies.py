import sys
import json
from ucsmsdk import ucshandle

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print "Usage: %s <JSON settings file>" % sys.argv[0]
            sys.exit(0)
        f = open(sys.argv[1], 'r')
        settings_file = json.load(f)
	is_secure = True
	if settings_file['secure'] == "False":
	    is_secure = False
        handle = ucshandle.UcsHandle(settings_file['ip'], settings_file['user'], settings_file['pw'], secure=is_secure)
        handle.login()
        ##### Start-Of-PythonScript #####

	from ucsmsdk.mometa.uuidpool.UuidpoolPool import UuidpoolPool
	from ucsmsdk.mometa.uuidpool.UuidpoolBlock import UuidpoolBlock

	mo = UuidpoolPool(parent_mo_or_dn="org-root", policy_owner="local", prefix="derived", descr="", assignment_order="default", name="UUID_Pool")
	mo_1 = UuidpoolBlock(parent_mo_or_dn=mo, to="0000-000000000020", r_from="0000-000000000001")
        handle.add_mo(mo)

        handle.commit()
        ##### End-Of-PythonScript #####
        ##### Start-Of-PythonScript #####

        from ucsmsdk.mometa.compute.ComputePool import ComputePool
        from ucsmsdk.mometa.compute.ComputePooledSlot import ComputePooledSlot

	mo = ComputePool(parent_mo_or_dn="org-root", policy_owner="local", name="Openstack_Controller_Pool", descr="")
        for pool_parms in settings_file['controller_pool']:
            mo_1 = ComputePooledSlot(parent_mo_or_dn=mo, chassis_id=pool_parms['chassis'], slot_id=pool_parms['slot'])
        handle.add_mo(mo)

        handle.commit()

        mo = ComputePool(parent_mo_or_dn="org-root", policy_owner="local", name="Openstack_Compute_Pool", descr="")
        for pool_parms in settings_file['compute_pool']:
            mo_1 = ComputePooledSlot(parent_mo_or_dn=mo, chassis_id=pool_parms['chassis'], slot_id=pool_parms['slot'])
        handle.add_mo(mo)

        handle.commit()

        mo = ComputePool(parent_mo_or_dn="org-root", policy_owner="local", name="Openstack_Storage_Pool", descr="")
        for pool_parms in settings_file['storage_pool']:
            mo_1 = ComputePooledSlot(parent_mo_or_dn=mo, chassis_id=pool_parms['chassis'], slot_id=pool_parms['slot'])
        handle.add_mo(mo)

        handle.commit()
        ##### End-Of-PythonScript #####
        ##### Start-Of-PythonScript #####

        from ucsmsdk.mometa.compute.ComputePooledRackUnit import ComputePooledRackUnit

        mo = ComputePool(parent_mo_or_dn="org-root", policy_owner="local", name="Openstack_Installer_Pool", descr="")
        for pool_parms in settings_file['installer_pool']:
            mo_1 = ComputePooledRackUnit(parent_mo_or_dn=mo, id=pool_parms['rack_id'])
        handle.add_mo(mo)

        handle.commit()
        ##### End-Of-PythonScript #####
        ##### Start-Of-PythonScript #####

        from ucsmsdk.mometa.fabric.FabricVConProfile import FabricVConProfile
        from ucsmsdk.mometa.fabric.FabricVCon import FabricVCon

        mo = FabricVConProfile(parent_mo_or_dn="org-root", policy_owner="local", name="Host_Infra", descr="", mezz_mapping="round-robin")
        mo_1 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="assigned-only", transport="ethernet,fc", id="1", inst_type="auto")
        mo_2 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="auto")
        mo_3 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="auto")
        mo_4 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="auto")
        handle.add_mo(mo)

        handle.commit()
        ##### End-Of-PythonScript #####
        ##### Start-Of-PythonScript #####

        from ucsmsdk.mometa.lsmaint.LsmaintMaintPolicy import LsmaintMaintPolicy

        mo = LsmaintMaintPolicy(parent_mo_or_dn="org-root", uptime_disr="user-ack", name="User_Ack", descr="", trigger_config="on-next-boot", sched_name="", policy_owner="local")
        handle.add_mo(mo)

        handle.commit()
        ##### End-Of-PythonScript #####
        ##### Start-Of-PythonScript #####

	from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy
	from ucsmsdk.mometa.lsboot.LsbootLan import LsbootLan
	from ucsmsdk.mometa.lsboot.LsbootLanImagePath import LsbootLanImagePath
	from ucsmsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
        from ucsmsdk.mometa.lsboot.LsbootStorage import LsbootStorage
        from ucsmsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
        from ucsmsdk.mometa.lsboot.LsbootDefaultLocalImage import LsbootDefaultLocalImage

	mo = LsbootPolicy(parent_mo_or_dn="org-root", name="PXE_Boot", descr="", reboot_on_update="no", policy_owner="local", enforce_vnic_name="yes", boot_mode="legacy")
	mo_1 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only", lun_id="0", mapping_name="", order="1")
	mo_2 = LsbootLan(parent_mo_or_dn=mo, prot="pxe", order="2")
	mo_2_1 = LsbootLanImagePath(parent_mo_or_dn=mo_2, prov_srv_policy_name="", img_sec_policy_name="", vnic_name="PXE", i_scsi_vnic_name="", boot_ip_policy_name="", img_policy_name="", type="primary")
        mo_3 = LsbootStorage(parent_mo_or_dn=mo, order="3")
        mo_3_1 = LsbootLocalStorage(parent_mo_or_dn=mo_3, )
        mo_3_1_1 = LsbootDefaultLocalImage(parent_mo_or_dn=mo_3_1, order="3")
        handle.add_mo(mo)

        handle.commit()
        ##### End-Of-PythonScript #####

        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
