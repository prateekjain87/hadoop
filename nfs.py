import subprocess
con="y"
print("\n\n\n\n--------------------------------Welcome to NFS---------------------------\n\n")
while(con=="Y" or con=="y"):
	uname = input("Enter the name of user:")		
	client_ip = input("Enter the IP of client:")
	client_pass = input("Enter the password of client:")
	print("1. NFS server \n2. NFS client \n3. NFS client (using autofs)")
	ch = input("Enter your choice:")
	if ch=="1":
		server_ip=input("Enter the IP on which you want to configure NFS server:")
		server_pass=input("Enter the password:") 
		if subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q nfs-utils | grep 'is not installed'".format(server_pass,server_ip))[1]=='' :
			print("NFS is already installed!")
		else:		
			send=subprocess.getstatusoutput("sshpass -p {} scp -o StrictHostKeyChecking=no /root/nfs-utils-1.3.0-0.54.el7.x86_64.rpm  root@{}:/root".format(server_pass,server_ip))
			if send[0]!=0:
				print("Error in installing nfs!")
				continue
			nfs = subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /root/nfs-utils-1.3.0-0.54.el7.x86_64.rpm ".format(server_pass,server_ip))
			if nfs[0]==0:
				print("NFS installed successfully!")
			else:
				print("Error in installing nfs!\nRestarting")
				con=input("Want to continue?(Y/N)") 				
				if con=="y" or con=="Y" : 			
					continue
				else:
					print("Exiting!")
					exit()
		dirname = input("Enter the name of directory for mounting on server:")
		f = subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} mkdir -p /udata/{}".format(server_pass,server_ip,dirname))
		entry = subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} 'bash -c echo /udata/{}  {}(rw,no_root_sqaush) >> /etc/exports'".format(server_pass,server_ip,dirname,client_ip))
		if entry[0]!=0:
			print("Error in editing 'exports' file! Restarting!")
			continue
		else:
			print("Mounting procedure successful on server side")
		dirname2=input("Enter the name of directory to mount with on client side:")
		f = subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} mkdir -p /{}".format(client_pass,client_ip,dirname2))
		mount=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} mount {}:{} {}".format(client_pass,client_ip,server_ip,dirname,dirname2))
		start=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl restart nfs".format(client_pass,client_ip))
		enable=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl enable nfs".format(client_pass,client_ip))
		print("Successfully configured NFS server!")
		input("Want to continue?(Y/N)")
		if con=="y" or con == "Y":
			continue
		else:
			exit()

	if ch=="2":
		
		print("\nStarting client configuration....")
		if subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q nfs-utils | grep 'is not installed'".format(client_pass,client_ip))[1]=='' :
			print("NFS is already installed!")
		else:		
			send=subprocess.getstatusoutput("sshpass -p {} scp -o StrictHostKeyChecking=no /root/nfs-utils-1.3.0-0.54.el7.x86_64.rpm  root@{}:/root/".format(client_pass,client_ip))
			if send[0]!=0:
				print("Error in installing nfs!")
				continue
			nfs = subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /root/nfs-utils-1.3.0-0.54.el7.x86_64.rpm ".format(client_pass,client_ip))
			if nfs[0]==0:
				print("NFS installed successfully!")
			else:
				print("Error in installing nfs!\nRestarting")
				con=input("Want to continue?(Y/N)") 				
				if con=="y" or con=="Y" : 			
					continue
				else:
					print("Exiting!")
					exit()
		start=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl restart nfs".format(client_pass,client_ip))
		enable=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl enable nfs".format(client_pass,client_ip))
		print("Successfully configured NFS client!")
		input("Want to continue?(Y/N)")
		if con=="y" or con == "Y":
			continue
		else:
			exit()

	if ch=="3": 
		if subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q nfs-utils | grep 'is not installed'".format(client_pass,client_ip))[1]=='' :
			print("NFS is already installed!")
		else:		
			send=subprocess.getstatusoutput("sshpass -p {} scp -o StrictHostKeyChecking=no /root/nfs-utils-1.3.0-0.54.el7.x86_64.rpm  root@{}:/root".format(client_pass,client_ip,client_ip))
			if send[0]!=0:
				print("Error in installing nfs!")
				continue			
			
			nfs = subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /root/nfs-utils-1.3.0-0.54.el7.x86_64.rpm ".format(client_pass,client_ip))
			if nfs[0]==0:
				print("NFS installed successfully!")
			else:
				print("Error in installing nfs!\nRestarting")
				continue
		con=input("Want to continue?(Y/N)") 				
		if con=="y" or con=="Y" : 			
			continue
		else:
			print("Exiting!")
			exit()	


		if subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q autofs | grep 'is not installed'".format(client_pass,client_ip))[1]=='':
			print("autoFS is already installed!")
		else:
			send=subprocess.getstatusoutput("sshpass -p {} scp -o StrictHostKeyChecking=no /root/autofs-5.0.7-83.el7.x86_64.rpm  root@{}:/root".format(client_pass,client_ip))
			if send[0]!=0:
				print("Error in installing autofs!")
				continue

			autofs = subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /root/autofs-5.0.7-83.el7.x86_64.rpm".format(client_pass,client_ip))
			if autofs[0]==0:
				print("AutoFS installed successfully!")
			else:
				print("Error in installing autofs!\nRestarting")
				continue
		subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} setsebool -P use_nfs_home_dirs=1".format(client_pass,client_ip))
		entry=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} 'bash -c echo {} {}:/udata/{} >> /etc/auto.misc'".format(client_pass,client_ip,uname,ip,dirname))
		if entry[0]!=0:
			print("Error in editing 'auto.misc' file! Restarting!")
			continue
		try:
			s = open("/etc/auto.master").read()
			s = s.replace('/misc','/udata')
			f= open("/etc/auto.master",'w')
			f.write(s)
			f.close()
		except:
			print("Error in editing auto.master file! Restarting!")
			continue
		nfs = subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl restart nfs".format(client_pass,client_ip))
		if nfs[0]!=0:
			print("Error in starting NFS service!")	
		afs = subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl restart autofs".format(client_pass,client_ip))	
		if afs[0]!=0:
			print("Error in starting autofs service!")
		else:
			print("Autofs service successfully started.")
		start=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl restart nfs".format(client_pass,client_ip))
		enable=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl enable nfs".format(client_pass,client_ip))
		print("Successfully configured NFS client(with autofs)!")
		input("Want to continue?(Y/N)")
		if con=="y" or con == "Y":
			continue
		else:
			exit()
