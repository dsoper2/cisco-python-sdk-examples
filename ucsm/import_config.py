import sys
import json
from ucsmsdk import ucshandle
from ucsmsdk.utils.ucsbackup import import_ucs_backup

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print "Usage: %s <JSON settings file> [backup filename]" % sys.argv[0]
            sys.exit(0)
        f = open(sys.argv[1], 'r')
        settings_file = json.load(f)
	is_secure = True
	if settings_file['secure'] == "False":
	    is_secure = False
        handle = ucshandle.UcsHandle(settings_file['ip'], settings_file['user'], settings_file['pw'], secure=is_secure)
	handle.login()
        if len(sys.argv) > 2:
            import_name = sys.argv[2]
        else:
            import_name = 'backup.xml'
	print "Importing UCSM settings from %s" % import_name
        import_ucs_backup(handle, file_dir="./", file_name=import_name)
	handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

