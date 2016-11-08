import sys
import json

from pyghmi.ipmi.command import Command

def kick_via_ipmi(lom_ip, username, password):
    ipmi_session = Command(lom_ip, username, password)
    ipmi_session.set_power('off', wait=True)
    ipmi_session.set_bootdev('network')
    ipmi_session.set_power('on')

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
	print "power cycle host at %s" % settings_file['ip']
        kick_via_ipmi(settings_file['ip'], settings_file['user'], settings_file['pw'])

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
	if handle:
	    handle.logout()
