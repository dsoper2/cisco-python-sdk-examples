import sys
import json
import csv
from ucsmsdk import ucshandle
from ucsmsdk_samples.server import service_profile
from ucsmsdk.mometa.ls.LsRequirement import LsRequirement

if __name__ == "__main__":
    try:
        if len(sys.argv) < 3:
            print "Usage: %s <JSON settings file> <csv file>" % sys.argv[0]
            print "       <settings file>: access settings (IP/user/password)"
            print "       <csv file>: settings for service profile creation"
            sys.exit(0)
        f = open(sys.argv[1], 'r')
        settings_file = json.load(f)
	is_secure = True
	if settings_file['secure'] == "False":
	    is_secure = False
        handle = ucshandle.UcsHandle(settings_file['ip'], settings_file['user'], settings_file['pw'], secure=is_secure)
        handle.login()
        
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
            if not row['Template']:
	        print "Error on row %d: no template name found" % row_num
	        continue
	    template = row['Template']
	    profile_name = row['profile']
	    if not profile_name:
	        profile_name = "%s-instance-" % template
	    num_instances = int(row['instances'])
	    if not num_instances:
	        num_instances = 1
	    print "Creating %s service profiles with name prefix %s" % (num_instances, profile_name)
	    # use the sample template creation function
	    mo = service_profile.sp_template_create(handle, name=template, type="updating-template",
                                               resolve_remote="yes", descr="", usr_lbl="",
					       src_templ_name="", ext_ip_state="pooled",
					       ext_ip_pool_name=row['Mgmt_IP_Pool'],
					       ident_pool_name=row['UUID'],
					       agent_policy_name="",
					       bios_profile_name="",
					       boot_policy_name=row['Boot_Policy'],
					       dynamic_con_policy_name="",
	                                       host_fw_policy_name="",
                                     	       kvm_mgmt_policy_name="",
                                   	       lan_conn_policy_name=row['LAN_Policy'],
                                     	       local_disk_policy_name="",
                                   	       maint_policy_name=row['Maint_Policy'],
                                   	       mgmt_access_policy_name="",
                                   	       mgmt_fw_policy_name="",
                                   	       power_policy_name="",
                                   	       san_conn_policy_name="",
                                   	       scrub_policy_name="",
                                   	       sol_policy_name="",
                                   	       stats_policy_name="",
                                   	       vcon_profile_name=row['vNIC_placement'],
                                   	       vmedia_policy_name="",
                                   	       parent_dn=org)
	    # create the actual service profiles
            service_profile.sp_create_from_template(handle,
                                                    naming_prefix=profile_name,
                                                    name_suffix_starting_number="1",
                                                    number_of_instance=num_instances,
                                                    sp_template_name=template,
                                                    in_error_on_existing="true",
						    parent_dn=org)
            server_pool = row['Server-Pool'] if (row['Server-Pool']) else 'default'
	    for instance in range(1, num_instances + 1):
	        dn = "%s/ls-%s%d" % (org, profile_name, instance)
	        mo = LsRequirement(parent_mo_or_dn=dn, restrict_migration="no",
		                   name=server_pool, qualifier="")
	        handle.add_mo(mo, True)
	        handle.commit()
        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

