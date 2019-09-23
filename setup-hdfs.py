#!/usr/bin/python2

import commands as sp
import cgi
import cgitb
cgitb.enable()

print("content-type:text/html")
print("\n")


form = cgi.FormContent()

host = open('/hadoop/hostfile','a')
fopen = open('/hadoop/count','r')
x = int(float(fopen.read()))
fh = open('/var/www/cgi-bin/hosts','w')
fopen = open('/hadoop/count','w')

print(form)

for i in form.keys():

	if 'mip' in i:
		x+=1
		fh.write("[name]\n")
		fh.write(form[i][0] + "\n")
		sp.getoutput("sshpass -p redhat ssh-copy-id {} -o StrictHostKeyChecking=no".format(form[i][0]))
		host.write('\nname{}  {}'.format(x,form[i][0]))
		
	if 'dip' in i:
		x=x+1
		fh.write("[data]\n")
		fh.write(form[i][0] + "\n")
		sp.getoutput("sshpass -p redhat ssh-copy-id {} -o StrictHostKeyChecking=no".format(form[i][0]))
		host.write('\ndata{}  {}'.format(x,form[i][0]))		

	if 'jip' in i:

		x+=1
		jmip = form['jn'][0]
		fopen = open('/hadoop/j.yml','w')
		fopen.write('mip: {}'.format(jmip))
		fopen.write('jip: {}'.format(form[i][0]))
		host.write('\nname{}  {}'.format(x,jmip))		
		x+=1
		fh.write("[job]\n")
		fh.write(form[i][0] + "\n")
		sp.getoutput("sshpass -p redhat ssh-copy-id {} -o StrictHostKeyChecking=no".format(form[i][0]))
		host.write('job{}  {}'.format(x,form[i][0]))
		

	if 'tip' in i:

		x+=1
		fh.write("[task]\n")
		fh.write(form[i][0] + "\n")
		sp.getoutput("sshpass -p redhat ssh-copy-id {} -o StrictHostKeyChecking=no".format(form[i][0]))
		host.write('\ntask{}  {}'.format(x,form[i][0]))		


if 'mip' in form.keys():

	print("In mip")
	res = sp.getstatusoutput("ansible-playbook /hadoop/name.yml -i /var/www/cgi-bin/hosts")
	if  res[0] == 0:
		print("Successfully Configured NameNode! ")
	else: 
		print("Failed!")
	print("ok1")

if 'dip' in form.keys():

	x+=1
	dmip = form['dm'][0]
	fopen = open('/hadoop/d.yml','w')
	fopen.write('mip: {}'.format(dmip))
	host.write('\nname{}  {}'.format(x,dmip))		

	res = sp.getstatusoutput("ansible-playbook /hadoop/data.yml -i /var/www/cgi-bin/hosts")
	if  res[0] == 0:
		print("Successfully Configured DataNode! ")
	else: 
		print("Failed!")

print("ok2")


if 'jip' in form.keys():

	res = sp.getstatusoutput("sudo ansible-playbook /hadoop/job.yml -i /var/www/cgi-bin/hosts")
	if  res[0] == 0:
		print("Successfully Configured JobTracker! ")
	else: 
		print("Failed!")
	
if 'tip' in form.keys():
	
	tjip = form['tj'][0]
	fopen = open('/hadoop/t.yml','w')
	fopen.write('jip: {}'.format(tjip))	
	x+=1
	host.write('job{}  {}'.format(x,tjip))
	
	res = sp.getstatusoutput("ansible-playbook /hadoop/task.yml -i /var/www/cgi-bin/hosts")
	if  res[0] == 0:
		print("Successfully Configured TaskTracker!")
	else: 
		print("Failed!")
print("done")

host.close()
fh.close()
fopen.write(str(x))
fopen.close()

