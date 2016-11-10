import sys
import json
from ucsmsdk import ucshandle
from ucsmsdk.utils.ucsbackup import backup_ucs

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
            backup_name = sys.argv[2]
        else:
            backup_name = 'backup.xml'
        print "Backing up UCSM settings to %s" % backup_name

        backup_ucs(handle, backup_type="config-all", file_dir="./", file_name=backup_name)
	handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

