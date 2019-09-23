import subprocess
import os
import socket
import time
con="y"
print("Welcome to HADOOP configuration:\nWhere you want to configure?\n1.Local system\n2.Remote system\n3.Exit")
system=int(input("Enter your choice:"))
if system==1:
	while con=="y" or con=="Y":
		print("Which configuration you want?\n")
		print("1.Name node\n2.Data Node\n")
		ch=int(input("Enter your choice:"))
		if ch==1:	
			#hostname=socket.gethostname()
			#ip=socket.gethostbyname(hostname)
			inet=subprocess.getstatusoutput("ifconfig enp0s3 | grep inet | head -1 | awk {'print $2'}")
			ip=inet[1]
		#Installations
			if subprocess.getstatusoutput('rpm -q jdk1.8 | grep "is not installed"')[1]=='':
				print("JDK is already installed!")
			else:
				x=subprocess.getstatusoutput("rpm -ivh /Softwares/share/Software/jdk-8u171-linux-x64.rpm")
				if x[0]!=0:
					print("Error in installing JDK!\nRestarting...")
					continue			
				print("JDK successfully installed")
			y=subprocess.getstatusoutput("echo export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/ >> /root/.bashrc")
			if y[0]!=0:
				print("Failed to set JAVA_HOME !")
				continue
			print("JAVA_HOME successfullly set")
			z=subprocess.getstatusoutput("echo export PATH=/usr/java/jdk1.8.0_171-amd64/bin/:'$PATH' >> /root/.bashrc")
			if z[0]!=0:
				print("Failed to set PATH variable !")
				continue
			print("PATH variable successfully set !")
			if subprocess.getstatusoutput('rpm -q hadoop | grep "is not installed"')[1]!='':
				h=subprocess.getstatusoutput("rpm -ivh /Softwares/share/Software/hadoop-1.2.1-1.x86_64.rpm --force")
				if h[0]!=0:
					print("Error in installing Hadoop!!!")
					continue
				else:
					print("Hadoop installed successfully!")	
			else:
				print("Hadoop already installed!")	
	
			dirname=input("Enter the name of directory for name node: ")			
			d=subprocess.getstatusoutput("mkdir /{}".format(dirname))
			if d[0]==0:
				print("Directory successfully created\nStep-1 completed\nSuccessfully installed required packages!")
			else:
				print("Failed to create directory!")
				continue			
	#hfds-file configuration
			try:
				file_open=open('/etc/hadoop/hdfs-site.xml','w') 
				file_open.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.name.dir</name>
<value>/{}</value>
</property>
</configuration>""".format(dirname))
				file_open.close()
				print("hdfs-site.xml file successfully modified!")
			except IOError:
				print("Failed to update ")
				continue
	#core-site configuration
			try:
				file_open=open('/etc/hadoop/core-site.xml','w') 
				file_open.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:9001</value>
</property>
</configuration>""".format(ip))	
				file_open.close()
				print("core-site.xml file succcessfully modified.")		
			except IOError:
				print("Failed to edit core-site.xml file!\nRestarting")
				continue

		#firewall

			firewall=subprocess.getstatusoutput("systemctl stop firewalld")
			if firewall[0]==0:
				print("Firewall disabled for network connectivity.")
			se=subprocess.getstatusoutput("setenforce 0")
			if se[0]==0:
				print("SELinux permissive")
		#formatting
			for_mat=subprocess.getstatusoutput("hadoop namenode -format -force")
			time.sleep(3)
			if for_mat[0]==0:
				print("NameNode formatted successfully and is ready for use!")
			else:
				print("Failed to format NameNode restarting!!!")
				continue
		#start namemode

			start=subprocess.getstatusoutput("hadoop-daemon.sh start namenode")
			time.sleep(3)
			if start[0]==0:
				jps=subprocess.getstatusoutput("jps | grep NameNode")
				if jps[1]!='':	
					print("\n\n\nSuccessfully configured Hadoop NameNode")
				else:
					print("\n\n\nFailed to start Namenode!")
					continue
			print("Want to check status?(y/n)")


		#Report of nodes
		#subprocess.getstatusoutput("hadoop dfsadmin -report")
		#Slave node
		elif ch == 2 :
			ip=input("Enter ip of master node:")
		#Installations
			if subprocess.getstatusoutput('rpm -q jdk1.8 | grep "is not installed"')[1]=='':
				print("JDK is already installed!")
			else:
				x=subprocess.getstatusoutput("rpm -ivh /Softwares/share/Software/jdk-8u171-linux-x64.rpm")
				if x[0]!=0:
					print("Error in installing JDK!\nRestarting...")
					continue			
				print("JDK successfully installed")
			y=subprocess.getstatusoutput("echo export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/ >> /root/.bashrc")
			if y[0]!=0:
				print("Failed to set JAVA_HOME !")
				continue
			print("JAVA_HOME successfullly set")
			z=subprocess.getstatusoutput("echo export PATH=/usr/java/jdk1.8.0_171-amd64/bin/:'$PATH' >> /root/.bashrc")
			if z[0]!=0:
				print("Failed to set PATH variable !")
				continue
			print("PATH variable successfully set !")
			if subprocess.getstatusoutput('rpm -q hadoop | grep "is not installed"')[1]!='':
				h=subprocess.getstatusoutput("rpm -ivh /Softwares/share/Software/hadoop-1.2.1-1.x86_64.rpm --force")
				if h[0]!=0:
					print("Error in installing Hadoop!!!")
					continue
				else:
					print("Hadoop installed successfully!")	
			else:
				print("Hadoop already installed!")	
		
			dirname=input("Enter the name of directory for data node: ")			
			d=subprocess.getstatusoutput("mkdir /{}".format(dirname))
			if d[0]==0:
				print("Directory successfully created\nStep-1 completed\nSuccessfully installed required packages!")
			else:
				print("Failed to create directory!")
				continue			

		#hfds-file configuration

			try:
				file_open=open('/etc/hadoop/hdfs-site.xml','w') 
				file_open.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.data.dir</name>
<value>/{}</value>
</property>
</configuration>""".format(dirname))
				file_open.close()
				print("hdfs-site.xml file successfully modified!")
			except IOError:
				print("Failed to update ")
				continue

		#core-site configuration

			try:
				file_open=open('/etc/hadoop/core-site.xml','w') 
				file_open.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:9001</value>
</property>
</configuration>""".format(ip))	
				print("core-site.xml file succcessfully modified.")		
				file_open.close()
			except IOError:
				print("Failed to edit core-site.xml file!\nRestarting")
				continue


		#stop firewall

			subprocess.getstatusoutput("systemctl stop firewalld")
			print("Firewall successfully disabled!")
			subprocess.getstatusoutput("setenforce 0")
			print("SELinux permissive!")

		#start
			start=subprocess.getstatusoutput("hadoop-daemon.sh start datanode")
			time.sleep(3)
			if start[0]==0:
				jps=subprocess.getstatusoutput("jps | grep DataNode")
				if jps[1]!='':	
					print("\n\n\nSuccessfully configured Hadoop data node")
				else:
					print("\n\n\nFailed to start datanode!")
					continue
			con=input("want to continue?(y/n)")
			if con=="n" or con =="N":
				exit()
			elif con=="Y" or con=="y" :
				continue
		else :
			print("Wrong input")
			exit()
elif system==2:

#IP
	sys_ip=input("Enter the IP where you want to configure system:")	
	des_pass=input("Enter the password of destination:")
	while con=="y" or con=="Y":
		print("Welcome to HADOOP configuration:\nWhich configuration you want?\n")
		print("1.Name node\n2.Data Node\n")
		ch=int(input("Enter your choice:"))

#		hostname=socket.gethostname()
#		ip=socket.gethostbyname(hostname)
#NAMENODE

		if ch==1:	
		#Installations
			s=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q jdk1.8 | grep 'is not installed' ".format(des_pass,sys_ip))
			if s[1]=='':
				print("JDK is already installed!")
			else:
				t=subprocess.getstatusoutput("sshpass -p {} scp -o StrictHostKeyChecking=no /Softwares/share/Software/jdk-8u171-linux-x64.rpm root@{}:/root ".format(des_pass,sys_ip))
				x=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /root/jdk-8u171-linux-x64.rpm".format(des_pass,sys_ip))
				if x[0]!=0:
					print("Error in installing JDK!\nRestarting...")
					continue			
				print("JDK successfully installed")
			y=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} 'echo export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/ >> /root/.bashrc'".format(des_pass,sys_ip))
			if y[0]!=0:
				print("Failed to set JAVA_HOME !")
				continue
			print("JAVA_HOME successfullly set")
			z=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} 'echo export PATH=/usr/java/jdk1.8.0_171-amd64/bin/:$PATH >> /root/.bashrc'".format(des_pass,sys_ip))
			if z[0]!=0:
				print("Failed to set PATH variable !")
				continue
			print("PATH variable successfully set !")
			if subprocess.getstatusoutput('sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q hadoop | grep "is not installed"'.format(des_pass,sys_ip))[1]!='':
				t=subprocess.getstatusoutput("sshpass -p {} scp -o StrictHostKeyChecking=no /Softwares/share/Software/hadoop-1.2.1-1.x86_64.rpm root@{}:/root ".format(des_pass,sys_ip))
				h=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /root/hadoop-1.2.1-1.x86_64.rpm --force".format(des_pass,sys_ip))
				if h[0]!=0:
					print("Error in installing Hadoop!!!")
					continue
				else:
					print("Hadoop installed successfully!")	
			else:
				print("Hadoop already installed!")	
		
			dirname=input("Enter the name of directory for name node: ")			
			d=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} mkdir /{}".format(des_pass,sys_ip,dirname))
			if d[0]==0:
				print("Directory successfully created\nStep-1 completed\nSuccessfully installed required packages!")
			else:
				print("Failed to create directory!")
				continue

		
		#hdfs-site.xml

			try:
				file_open=open('/root/hdfs-site.xml','w') 
				file_open.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.name.dir</name>
<value>/{}</value>
</property>
</configuration>""".format(dirname))
				file_open.close()
				send=subprocess.getstatusoutput("sshpass -p {} scp -o StrictHostKeyChecking=no /root/hdfs-site.xml root@{}:/etc/hadoop".format(des_pass,sys_ip))
				if send[0]==0:
					print("hdfs-site.xml file succcessfully modified.")
			except IOError:
				print("Failed to update ")
				continue


		#core-site.xml
			try:
				file_open=open('/root/core-site.xml','w') 
				file_open.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:9001</value>
</property>
</configuration>""".format(sys_ip))	
				file_open.close()
				send=subprocess.getstatusoutput("sshpass -p {} scp -o StrictHostKeyChecking=no /root/core-site.xml root@{}:/etc/hadoop".format(des_pass,sys_ip))
				if send[0]==0:
					print("core-site.xml file succcessfully modified.")		
			except IOError:
				print("Failed to edit core-site.xml file!\nRestarting")
				continue
		#firewall
			stop=subprocess.getstatusoutput("sshpass -p {} ssh -l root {} systemctl stop firewalld".format(des_pass,sys_ip))
			if stop[0]==0:
				print("Firewall successfully stopped!")
			subprocess.getstatusoutput("sshpass -p {} ssh -l root {} setenforce 0".format(des_pass,sys_ip))
		#formatting
			for_mat=subprocess.getstatusoutput("sshpass -p {} ssh -l root {} hadoop namenode -format -force".format(des_pass,sys_ip))
			time.sleep(3)
			if for_mat[0]==0:
				print("Successfully formatted NameNode.")
		#start namemode
			start=subprocess.getstatusoutput("sshpass -p {} ssh -l root {} hadoop-daemon.sh start namenode".format(des_pass,sys_ip))
			time.sleep(3)
			if start[0]==0:
				jps=subprocess.getstatusoutput("sshpass -p {} ssh -l root {} jps | grep NameNode".format(des_pass,sys_ip))
				if jps[1]!='':	
					print("\n\n\nSuccessfully configured Hadoop Master node")
				else:
					print("\n\n\nFailed to start Namenode!")
					continue				
			print("Want to check status?(y/n)")
			continue

		#Report of nodes
		#subprocess.getstatusoutput("hadoop dfsadmin -report")
		#Slave node
		elif ch == 2 :
			ip=input("Enter ip of master node:")
#Installations
			if subprocess.getstatusoutput('sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q jdk1.8 | grep "is not installed"'.format(des_pass,sys_ip))[1]=='':
				print("JDK is already installed!")
			else:
				t=subprocess.getstatusoutput("sshpass -p {} scp -o StrictHostKeyChecking=no /Softwares/share/Software/jdk-8u171-linux-x64.rpm root@{}:/root ".format(des_pass,sys_ip))
				x=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l  root {} rpm -ivh /root/jdk-8u171-linux-x64.rpm".format(des_pass,sys_ip))
				if x[0]!=0:
					print("Error in installing JDK!\nRestarting...")
					continue			
				print("JDK successfully installed")
			y=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} 'echo export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/ >> /root/.bashrc'".format(des_pass,sys_ip))
			if y[0]!=0:
				print("Failed to set JAVA_HOME !")
				continue
			print("JAVA_HOME successfullly set")
			z=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} 'echo export PATH=/usr/java/jdk1.8.0_171-amd64/bin/:'$PATH' >> /root/.bashrc'".format(des_pass,sys_ip))
			if z[0]!=0:
				print("Failed to set PATH variable !")
				continue
			print("PATH variable successfully set !")
			if subprocess.getstatusoutput('sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q hadoop | grep "is not installed"'.format(des_pass,sys_ip))[1]!='':
				t=subprocess.getstatusoutput("sshpass -p {} scp -o StrictHostKeyChecking=no /Softwares/share/Software/hadoop-1.2.1-1.x86_64.rpm root@{}:/root ".format(des_pass,sys_ip))
				h=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /root/hadoop-1.2.1-1.x86_64.rpm --force".format(des_pass,sys_ip))
				if h[0]!=0:
					print("Error in installing Hadoop!!!")
					continue
				else:
					print("Hadoop installed successfully!")	
			else:
				print("Hadoop already installed!")	
	
			dirname=input("Enter the name of directory for data node: ")			
			d=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} mkdir /{}".format(des_pass,sys_ip,dirname))
			if d[0]==0:
				print("Directory successfully created\nStep-1 completed\nSuccessfully installed required packages!")
			else:
				print("Failed to create directory!")
				continue

		#hdfs-site.xml

			try:
				file_open=open('/root/hdfs-site.xml','w') 
				file_open.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.data.dir</name>
<value>/{}</value>
</property>
</configuration>""".format(dirname))
				file_open.close()
				send=subprocess.getstatusoutput("sshpass -p {}  scp -o StrictHostKeyChecking=no /root/hdfs-site.xml root@{}:/etc/hadoop/hdfs-site.xml ".format(des_pass,sys_ip))
				if send[0]==0:
					print("hdfs-site.xml file successfully modified!")
			except IOError:
				print("Failed to update ")
				continue
	#core-site.xml
			try:
				file_open=open('/root/core-site.xml','w') 
				file_open.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:9001</value>
</property>
</configuration>""".format(ip))	
				file_open.close()
				send=subprocess.getstatusoutput("sshpass -p {}  scp -o StrictHostKeyChecking=no /root/core-site.xml root@{}:/etc/hadoop/core-site.xml ".format(des_pass,sys_ip))		
				if send[0]==0:
					print("core-site.xml file succcessfully modified.")
			except IOError:
				print("Failed to edit core-site.xml file!\nRestarting")
				continue
		#stop firewall
			subprocess.getstatusoutput("sshpass -p {} ssh -l root {} systemctl stop firewalld".format(des_pass,sys_ip))
			print("Firewall successfully stopped")
			subprocess.getstatusoutput("sshpass -p {} ssh -l root {} setenforce 0".format(des_pass,sys_ip))
			print("SELinux successfully stopped!")
		#start
			start=subprocess.getstatusoutput("sshpass -p {} ssh -l root {} hadoop-daemon.sh start datanode".format(des_pass,sys_ip))
			time.sleep(4)
			if start[0]==0:
				jps=subprocess.getstatusoutput("sshpass -p {} ssh -l root {} jps | grep DataNode".format(des_pass,sys_ip))
				if jps[1]!='':	
					print("\n\n\n Successfully configured Hadoop Slave node")
				else:
					print("Failed to start datanode!")
					continue				
			con=input("Want to continue?(y/n)")
			if con=="n" or con =="N":
				exit()
			elif con=="Y" or con=="y" :
				continue
		else :
			print("Wrong input")
			exit()
elif system==3:
	print("Exiting!")
	exit()

else :
	print("Wrong input!")
 	continue
