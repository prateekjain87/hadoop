#!/usr/bin/python36
print("content-type:text/html")
print("\n")

import subprocess
import cgi	


data = cgi.FieldStorage()
uname = data.getvalue('uname')
client_ip = data.getvalue('client_ip')
client_pass = data.getvalue('client_pass')
ch = data.getvalue('choice')
server_ip = data.getvalue('sip')
server_pass = data.getvalue('sp')
dirname = data.getvalue('dirname')
dirname2 = data.getvalue('dirname2')




if ch=="1":

	if subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q nfs-utils | grep 'is not installed'".format(server_pass,server_ip))[1]=='' :
		print("NFS is already installed!")
	else:		
		send=subprocess.getstatusoutput("sudo sshpass -p {} scp -o StrictHostKeyChecking=no /root/nfs-utils-1.3.0-0.54.el7.x86_64.rpm  root@{}:/root".format(server_pass,server_ip))
		if send[0]!=0:
			print("Error in installing nfs!")
		nfs = subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} 'rpm -ivh /root/nfs-utils-1.3.0-0.54.el7.x86_64.rpm' ".format(server_pass,server_ip))
		if nfs[0]==0:
			print("NFS installed successfully!")
		else:
			print("Error in installing nfs!\nRestarting")
	f = subprocess.getstatusoutput("sudo  sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} 'mkdir -p /udata/{}'".format(server_pass,server_ip,dirname))
	entry = subprocess.getstatusoutput("""sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} 'echo "/udata/{}  {}(rw,no_root_squash)" >> /etc/exports'""".format(server_pass,server_ip,dirname,client_ip))
	if entry[0]!=0:
		print("Error in editing 'exports' file! Restarting!")
	else:
		print("Mounting procedure successful on server side")
	f = subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} mkdir -p /{}".format(client_pass,client_ip,dirname2))
	mount=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} mount {}:/udata/{} /{}".format(client_pass,client_ip,server_ip,dirname,dirname2))
	print(mount)
	start=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl restart nfs".format(client_pass,client_ip))
	enable=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl enable nfs".format(client_pass,client_ip))
	print("Successfully configured NFS server!")

if ch=="2":
	print("\nStarting client configuration....")
	if subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q nfs-utils | grep 'is not installed'".format(client_pass,client_ip))[1]=='' :
		print("NFS is already installed!")
	else:		
		send=subprocess.getstatusoutput("sudo sshpass -p {} scp -o StrictHostKeyChecking=no /root/nfs-utils-1.3.0-0.54.el7.x86_64.rpm  root@{}:/root/".format(client_pass,client_ip))
		if send[0]!=0:
			print("Error in installing nfs!")
		nfs = subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /root/nfs-utils-1.3.0-0.54.el7.x86_64.rpm ".format(client_pass,client_ip))
		if nfs[0]==0:
			print("NFS installed successfully!")
		else:
			print("Error in installing nfs!\nRestarting")
	start=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl restart nfs".format(client_pass,client_ip))
	enable=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl enable nfs".format(client_pass,client_ip))
	print("Successfully configured NFS client!")

if ch=="3": 
	if subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q nfs-utils | grep 'is not installed'".format(client_pass,client_ip))[1]=='' :
		print("NFS is already installed!")
	else:		
		send=subprocess.getstatusoutput("sudo sshpass -p {} scp -o StrictHostKeyChecking=no /root/nfs-utils-1.3.0-0.54.el7.x86_64.rpm  root@{}:/root".format(client_pass,client_ip,client_ip))
		if send[0]!=0:
			print("Error in installing nfs!")
			
		nfs = subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /root/nfs-utils-1.3.0-0.54.el7.x86_64.rpm ".format(client_pass,client_ip))
		if nfs[0]==0:
			print("NFS installed successfully!")
		else:
			print("Error in installing nfs!\nRestarting")	

	if subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q autofs | grep 'is not installed'".format(client_pass,client_ip))[1]=='':
		print("autoFS is already installed!")
	else:
		send=subprocess.getstatusoutput("sudo sshpass -p {} scp -o StrictHostKeyChecking=no /root/autofs-5.0.7-83.el7.x86_64.rpm  root@{}:/root".format(client_pass,client_ip))
		if send[0]!=0:
			print("Error in installing autofs!")
		autofs = subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /root/autofs-5.0.7-83.el7.x86_64.rpm".format(client_pass,client_ip))
		if autofs[0]==0:
			print("AutoFS installed successfully!")
		else:
			print("Error in installing autofs!\nRestarting")
	subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} setsebool -P use_nfs_home_dirs=1".format(client_pass,client_ip))
	entry=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} 'bash -c echo {} {}:/udata/{} >> /etc/auto.misc'".format(client_pass,client_ip,uname,ip,dirname))
	if entry[0]!=0:
		print("Error in editing 'auto.misc' file! Restarting!")
	try:
		s = open("/etc/auto.master").read()
		s = s.replace('/misc','/udata')
		f= open("/etc/auto.master",'w')
		f.write(s)
		f.close()
	except:
		print("Error in editing auto.master file! Restarting!")
	nfs = subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl restart nfs".format(client_pass,client_ip))
	if nfs[0]!=0:
		print("Error in starting NFS service!")	
	afs = subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl restart autofs".format(client_pass,client_ip))	
	if afs[0]!=0:
		print("Error in starting autofs service!")
	else:
		print("Autofs service successfully started.")
	start=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl restart nfs".format(client_pass,client_ip))
	enable=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl enable nfs".format(client_pass,client_ip))
	print("Successfully configured NFS client(with autofs)!")
