#!/usr/bin/python36
print("content-type:text/html")
print("\n")


import subprocess
import os
import cgi
import socket

data = cgi.FieldStorage()
system = int(data.getvalue('system'))
dirname = data.getvalue('dirname')
ch = int(data.getvalue('choice'))
master_ip = data.getvalue('mip')
sys_ip = data.getvalue('ip')
des_pass = data.getvalue('pass')

inet=subprocess.getstatusoutput("sudo ifconfig enp0s3 | grep inet | head -1 | awk {'print $2'}")
ip=inet[1]

print("<pre>")

if system==1:

	if ch==1:	
		#hostname=socket.gethostname()
		#ip=socket.gethostbyname(hostname)
	#Installations
		if subprocess.getstatusoutput('sudo rpm -q jdk1.8 | grep "is not installed"')[1]=='':
			print("JDK is already installed!")
		else:
			x=subprocess.getstatusoutput("sudo rpm -ivh /Softwares/share/Software/jdk-8u171-linux-x64.rpm")
			if x[0]!=0:
				print("Error in installing JDK!\nRestarting...")
				print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))			    
			print("JDK successfully installed")
		y=subprocess.getstatusoutput(" echo 'export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/ >> /root/.bashrc'")
		if y[0]!=0:
			print("Failed to set JAVA_HOME !")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
		print("JAVA_HOME successfullly set")
		z=subprocess.getstatusoutput(" echo 'export PATH=/usr/java/jdk1.8.0_171-amd64/bin/:$PATH >> /root/.bashrc'")
		if z[0]!=0:
			print("Failed to set PATH variable !")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
		print("PATH variable successfully set !")
		if subprocess.getstatusoutput('sudo rpm -q hadoop | grep "is not installed"')[1]!='':
			h=subprocess.getstatusoutput("sudo rpm -ivh /Softwares/share/Software/hadoop-1.2.1-1.x86_64.rpm --force")
			if h[0]!=0:
				print("Error in installing Hadoop!!!")
				print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
			else:
				print("Hadoop installed successfully!")	
		else:
			print("Hadoop already installed!")				
		d=subprocess.getstatusoutput("sudo mkdir /{}".format(dirname))
		if d[0]==0:
			print("Directory successfully created\nStep-1 completed\nSuccessfully installed required packages!")
		else:
			print("Failed to create directory!")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))			
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
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
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
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))

		#firewall

		firewall=subprocess.getstatusoutput("sudo systemctl stop firewalld")
		if firewall[0]==0:
			print("Firewall disabled for network connectivity.")
		se=subprocess.getstatusoutput("sudo setenforce 0")
		if se[0]==0:
			print("SELinux permissive")
		#formatting
		for_mat=subprocess.getstatusoutput("sudo hadoop namenode -format -force")
		if for_mat[0]==0:
			print("NameNode formatted successfully and is ready for use!")
		else:
			print("Failed to format NameNode restarting!!!")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
		#start namemode

		start=subprocess.getstatusoutput("sudo hadoop-daemon.sh start namenode")
		if start[0]==0:
			jps=subprocess.getstatusoutput("sudo jps | grep NameNode")
			if jps[1]!='':	
				print("\n\n\nSuccessfully configured Hadoop NameNode")
			else:
				print("\n\n\nFailed to start Namenode!")
				print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
		print("Want to check status?(y/n)")

		#Report of nodes
		#subprocess.getstatusoutput("hadoop dfsadmin -report")
		#Slave node

	elif ch == 2 :

		#hostname=socket.gethostname()
		#ip=socket.gethostbyname(hostname)
		inet=subprocess.getstatusoutput("sudo ifconfig enp0s3 | grep inet | head -1 | awk {'print $2'}")
		ip=inet[1]
	#Installations
		if subprocess.getstatusoutput('sudo rpm -q jdk1.8 | grep "is not installed"')[1]=='':
			print("JDK is already installed!")
		else:
			x=subprocess.getstatusoutput("sudo rpm -ivh /Softwares/share/Software/jdk-8u171-linux-x64.rpm")
			if x[0]!=0:
				print("Error in installing JDK!\nRestarting...")
				print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))			    
			print("JDK successfully installed")
		y=subprocess.getstatusoutput(" echo 'export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/ >> /root/.bashrc'")
		if y[0]!=0:
			print("Failed to set JAVA_HOME !")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
		print("JAVA_HOME successfullly set")
		z=subprocess.getstatusoutput(" echo 'export PATH=/usr/java/jdk1.8.0_171-amd64/bin/:$PATH >> /root/.bashrc'")
		if z[0]!=0:
			print("Failed to set PATH variable !")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
		print("PATH variable successfully set !")
		if subprocess.getstatusoutput('sudo rpm -q hadoop | grep "is not installed"')[1]!='':
			h=subprocess.getstatusoutput("sudo rpm -ivh /Softwares/share/Software/hadoop-1.2.1-1.x86_64.rpm --force")
			if h[0]!=0:
				print("Error in installing Hadoop!!!")
				print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
			else:
				print("Hadoop installed successfully!")	
		else:
			print("Hadoop already installed!")				
		d=subprocess.getstatusoutput("sudo mkdir /{}".format(dirname))
		if d[0]==0:
			print("Directory successfully created\nStep-1 completed\nSuccessfully installed required packages!")
		else:
			print("Failed to create directory!")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))			
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
			print("Failed to update hdfs-site.xml file")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
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
</configuration>""".format(master_ip))	
			file_open.close()
			print("core-site.xml file succcessfully modified.")		
		except IOError:
			print("Failed to edit core-site.xml file!\nRestarting")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))

		#firewall

		firewall=subprocess.getstatusoutput("sudo systemctl stop firewalld")
		if firewall[0]==0:
			print("Firewall disabled for network connectivity.")
		se=subprocess.getstatusoutput("sudo setenforce 0")
		if se[0]==0:
			print("SELinux permissive")
		#start datanode

		start=subprocess.getstatusoutput("sudo hadoop-daemon.sh start datanode")
		if start[0]==0:
			jps=subprocess.getstatusoutput("sudo jps | grep DataNode")
			if jps[1]!='':	
				print("\n\n\nSuccessfully configured Hadoop DataNode")
			else:
				print("\n\n\nFailed to start DataNode!")
				print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
		print("Want to check status?(y/n")


elif system==2:

#IP	
#		hostname=socket.gethostname()
#		ip=socket.gethostbyname(hostname)
#NAMENODE

	if ch==1:	
		#Installations
		s=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q jdk1.8 | grep 'is not installed' ".format(des_pass,sys_ip))
		if s[1]=='':
			print("JDK is already installed!")
		else:
			t=subprocess.getstatusoutput("sudo sshpass -p {} scp -o StrictHostKeyChecking=no /Softwares/share/Software/jdk-8u171-linux-x64.rpm root@{}:/root ".format(des_pass,sys_ip))
			x=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /root/jdk-8u171-linux-x64.rpm".format(des_pass,sys_ip))
			if x[0]!=0:
				print("Error in installing JDK!\nRestarting...")
				print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))			
			print("JDK successfully installed")
		y=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} 'echo export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/ >> /root/.bashrc'".format(des_pass,sys_ip))
		if y[0]!=0:
			print("Failed to set JAVA_HOME !")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
		print("JAVA_HOME successfullly set")
		z=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} 'echo export PATH=/usr/java/jdk1.8.0_171-amd64/bin/:$PATH >> /root/.bashrc'".format(des_pass,sys_ip))
		if z[0]!=0:
			print("Failed to set PATH variable !")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
		print("PATH variable successfully set !")
		if subprocess.getstatusoutput('sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q hadoop | grep "is not installed"'.format(des_pass,sys_ip))[1]!='':
			t=subprocess.getstatusoutput("sudo sshpass -p {} scp -o StrictHostKeyChecking=no /Softwares/share/Software/hadoop-1.2.1-1.x86_64.rpm root@{}:/root ".format(des_pass,sys_ip))
			h=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /root/hadoop-1.2.1-1.x86_64.rpm --force".format(des_pass,sys_ip))
			if h[0]!=0:
				print("Error in installing Hadoop!!!")
				print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
			else:
				print("Hadoop installed successfully!")	
		else:
			print("Hadoop already installed!")	
			
		d=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} mkdir /{}".format(des_pass,sys_ip,dirname))
		if d[0]==0:
			print("Directory successfully created\nStep-1 completed\nSuccessfully installed required packages!")
		else:
			print("Failed to create directory!")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))

		
		#hdfs-site.xml

		try:
			file_open=open('/hdfs-site.xml','w') 
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
			send=subprocess.getstatusoutput("sudo sshpass -p {} scp -o StrictHostKeyChecking=no /hdfs-site.xml root@{}:/etc/hadoop/".format(des_pass,sys_ip))
			if send[0]==0:
				print("hdfs-site.xml file succcessfully modified.")
		except IOError:
			print("Failed to update ")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))


		#core-site.xml
		try:
			file_open=open('/core-site.xml','w') 
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
			send=subprocess.getstatusoutput("sudo sshpass -p {} scp -o StrictHostKeyChecking=no /core-site.xml root@{}:/etc/hadoop/".format(des_pass,sys_ip))
			if send[0]==0:
				print("core-site.xml file succcessfully modified.")		
		except IOError:
			print("Failed to edit core-site.xml file!\nRestarting")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
		#firewall
		stop=subprocess.getstatusoutput("sudo sshpass -p {} ssh -l root {} systemctl stop firewalld".format(des_pass,sys_ip))
		if stop[0]==0:
			print("Firewall successfully stopped!")
		subprocess.getstatusoutput("sudo sshpass -p {} ssh -l root {} setenforce 0".format(des_pass,sys_ip))
		#formatting
		for_mat=subprocess.getstatusoutput("sudo sshpass -p {} ssh -l root {} hadoop namenode -format -force".format(des_pass,sys_ip))
		time.sleep(3)
		if for_mat[0]==0:
			print("Successfully formatted NameNode.")
		#start namemode
		start=subprocess.getstatusoutput("sudo sshpass -p {} ssh -l root {} hadoop-daemon.sh start namenode".format(des_pass,sys_ip))
		time.sleep(3)
		if start[0]==0:
			jps=subprocess.getstatusoutput("sudo sshpass -p {} ssh -l root {} jps | grep NameNode".format(des_pass,sys_ip))
			if jps[1]!='':	
				print("\n\n\nSuccessfully configured Hadoop Master node")
			else:
				print("\n\n\nFailed to start Namenode!")
				print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))				
#		print("Want to check status?(y/n)")
		print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))

		#Report of nodes
		#subprocess.getstatusoutput("hadoop dfsadmin -report")
		#Slave node


	elif ch == 2 :

#Installations
		if subprocess.getstatusoutput('sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q jdk1.8 | grep "is not installed"'.format(des_pass,sys_ip))[1]=='':
			print("JDK is already installed!")
		else:
			t=subprocess.getstatusoutput("sudo sshpass -p {} scp -o StrictHostKeyChecking=no /Softwares/share/Software/jdk-8u171-linux-x64.rpm root@{}:/root ".format(des_pass,sys_ip))
			x=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l  root {} rpm -ivh /root/jdk-8u171-linux-x64.rpm".format(des_pass,sys_ip))
			if x[0]!=0:
				print("Error in installing JDK!\nRestarting...")
				print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))			
			print("JDK successfully installed")
		y=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} 'echo export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/ >> /root/.bashrc'".format(des_pass,sys_ip))
		if y[0]!=0:
			print("Failed to set JAVA_HOME !")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
		print("JAVA_HOME successfullly set")
		z=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} 'echo export PATH=/usr/java/jdk1.8.0_171-amd64/bin/:'$PATH' >> /root/.bashrc'".format(des_pass,sys_ip))
		if z[0]!=0:
			print("Failed to set PATH variable !")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
		print("PATH variable successfully set !")
		if subprocess.getstatusoutput('sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q hadoop | grep "is not installed"'.format(des_pass,sys_ip))[1]!='':
			t=subprocess.getstatusoutput("sudo sshpass -p {} scp -o StrictHostKeyChecking=no /Softwares/share/Software/hadoop-1.2.1-1.x86_64.rpm root@{}:/root ".format(des_pass,sys_ip))
			h=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /root/hadoop-1.2.1-1.x86_64.rpm --force".format(des_pass,sys_ip))
			if h[0]!=0:
				print("Error in installing Hadoop!!!")
				print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
			else:
				print("Hadoop installed successfully!")	
		else:
			print("Hadoop already installed!")				
		d=subprocess.getstatusoutput("sudo sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} mkdir /{}".format(des_pass,sys_ip,dirname))
		if d[0]==0:
			print("Directory successfully created\nStep-1 completed\nSuccessfully installed required packages!")
		else:
			print("Failed to create directory!")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))

		#hdfs-site.xml

		try:
			file_open=open('/hdfs-site.xml','w') 
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
			send=subprocess.getstatusoutput("sudo sshpass -p {}  scp -o StrictHostKeyChecking=no /hdfs-site.xml root@{}:/etc/hadoop/".format(des_pass,sys_ip))
			if send[0]==0:
				print("hdfs-site.xml file successfully modified!")
		except IOError:
			print("Failed to update hdfs-site.xml file")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
	#core-site.xml
		try:
			file_open=open('/core-site.xml','w') 
			file_open.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:9001</value>
</property>
</configuration>""".format(master_ip))	
			file_open.close()
			send=subprocess.getstatusoutput("sudo sshpass -p {}  scp -o StrictHostKeyChecking=no /core-site.xml root@{}:/etc/hadoop/".format(des_pass,sys_ip))		
			if send[0]==0:
				print("core-site.xml file succcessfully modified.")
		except IOError:
			print("Failed to edit core-site.xml file!\nRestarting")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
		#stop firewall
		subprocess.getstatusoutput("sudo sshpass -p {} ssh -l root {} systemctl stop firewalld".format(des_pass,sys_ip))
		print("Firewall successfully stopped")
		subprocess.getstatusoutput("sudo sshpass -p {} ssh -l root {} setenforce 0".format(des_pass,sys_ip))
		print("SELinux successfully stopped!")
		#start
		start=subprocess.getstatusoutput("sudo sshpass -p {} ssh -l root {} hadoop-daemon.sh start datanode".format(des_pass,sys_ip))
		if start[0]==0:
			jps=subprocess.getstatusoutput("sudo sshpass -p {} ssh -l root {} jps | grep DataNode".format(des_pass,sys_ip))
			if jps[1]!='':	
				print("\n\n\n Successfully configured Hadoop Slave node")
			else:
				print("Failed to start datanode!")
				print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))				
			if con=="n" or con =="N":
				exit()
			elif con=="Y" or con=="y" :
				print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
		else :
			print("Wrong input")
			print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))
	else :
		print("Wrong input!")
		print("<a href='http://{}/hadoop.html'>Press here to continue</a>".format(ip))

print("</pre>")
