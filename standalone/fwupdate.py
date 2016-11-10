import sys
import json

from imcsdk.imchandle import ImcHandle
from imcsdk.utils.imcfirmwareinstall import update_imc_firmware_huu

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print "Usage: %s <settings_file>" % sys.argv[0]
            sys.exit(0)
        f = open(sys.argv[1], 'r')
        settings_file = json.load(f)
	is_secure = True
	if settings_file['secure'] == "False":
	    is_secure = False
        handle = ImcHandle(settings_file['ip'], settings_file['user'], settings_file['pw'], secure=is_secure)
        handle.login()
	
        print "update firmware on %s" % settings_file['ip']
        update_imc_firmware_huu(handle=handle,
                                remote_ip=settings_file['remote_ip'],
                                remote_share=settings_file['remote_share'],
                                share_type=settings_file['share_type'],
                                username='',
                                password='',
                                update_component='all',
                                stop_on_error='yes',
                                verify_update='no',
                                cimc_secure_boot='no',
                                timeout='60')

        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
	if handle:
	    handle.logout()
