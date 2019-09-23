#!/bin/bash/python36

print("content-type:text/html")
print("\n")

import cgi
import subprocess as sp
import cgitb

cgitb.enable()


form = cgi.FieldStorage()
name = form.getvalue('name')

fh=open('/Cloud/xpra_details.yml','w')
fh.write(str(name))

sp.getstatusoutput("sudo ansible-playbook /var/www/cgi-bin/vlc.yml")

fh.close()
