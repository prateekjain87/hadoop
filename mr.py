import subprocess
print("\n\n\t\t------------Welcome to Mapreduce Menu:------------------\n")
con="y"
while con=="y" or con=="Y":	
	print("""What do you want to configure?
	1. TaskTracker
	2. JobTracker
	3. exit
	""")
	ch=int(input("Enter your choice: "))
	if ch !=3:
		name_ip=input("Enter the ip of NameNode:")
	if ch==1:
		print("Configuring TaskTracker.....")
		job_ip=input("Enter the ip of Jobtracker in your system:")
		task_ip=input("Enter the IP")
		task_host=input("Enter the hostname you want to set:")
		task_pass=input("Enter the password:")
		hostset=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} hostnamectl set-hostname  {}".format(task_pass,task_ip,task_host))			
		if subprocess.getstatusoutput('sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q jdk1.8 | grep "is not installed"'.format(task_pass,task_ip))[1]=='':
			print("JDK is already installed!")
		else:
			x=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /Softwares/share/Software/jdk-8u171-linux-x64.rpm".format(task_pass,task_ip))
			if x[0]!=0:
				print("Error in installing JDK!\nRestarting...")
				continue			
		print("JDK successfully installed")
		y=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} echo export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/ >> /root/.bashrc".format(task_pass,task_ip))
		if y[0]!=0:
			print("Failed to set JAVA_HOME !")
			continue
		print("JAVA_HOME successfullly set")
		z=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} echo export PATH=/usr/java/jdk1.8.0_171-amd64/bin/:'$PATH' >> /root/.bashrc".format(task_pass,task_ip))
		if z[0]!=0:
			print("Failed to set PATH variable !")
			continue
		print("PATH variable successfully set !")
		if subprocess.getstatusoutput('sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q hadoop | grep "is not installed"'.format(task_pass,task_ip))[1]!='':
			h=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /Softwares/share/Software/hadoop-1.2.1-1.x86_64.rpm --force".format(task_pass,task_ip))
			if h[0]!=0:
				print("Error in installing Hadoop!!!")
				continue
			else:
				print("Hadoop installed successfully!")	
		else:
			print("Hadoop already installed!")	
	
	#Mapred-site
			
		try:
			file_open=open('/etc/hadoop/mapred-site.xml','w') 
			file_open.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>mapred.job.tracker</name>
<value>{}:9002</value>
</property>
</configuration>""".format(job_ip))
			file_open.close()
			print("mapred-site.xml file successfully modified!")
		except IOError:
			print("Failed to update ")
			continue		
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
</configuration>""".format(name_ip))
			file_open.close()
			print("core-site.xml file successfully modified!")
		except IOError:
			print("Failed to update ")
			continue
				
		try:
			fopen=open('/hosts.txt','a+')
			fopen.write("{}	{}".format(task_ip,task_host))
			fopen.close()
		except:
			print("Failed to update hosts file!")
			continue
		try:
			fopen=open('/ip.txt','a+')
			fopen.write("{}".format(task_ip))
			fopen.close()
			fopen=open('/p.txt','a+')
			fopen.write("{}".format(task_pass))
			fopen.close()
		except:
			print("Failed to update hosts file!")
			continue
				
		
	elif ch==2:
		print("Configuring jobtracker....")
		job_ip=input("Enter the IP:")
		job_pass=input("Enter the password:")
		job_host=input("Enter the hostname you want to set:")
		hostset=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} hostnamectl set-hostname  {}".format(job_pass,job_ip,job_host))
		if subprocess.getstatusoutput('sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q jdk1.8 | grep "is not installed"'.format(job_pass,job_ip))[1]=='':
						print("JDK is already installed!")
		else:
			x=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /Softwares/share/Software/jdk-8u171-linux-x64.rpm".format(job_pass,job_ip))
			if x[0]!=0:
				print("Error in installing JDK!\nRestarting...")
				continue			
		print("JDK successfully installed")
		y=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} echo export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/ >> /root/.bashrc".format(job_pass,job_ip))
		if y[0]!=0:
			print("Failed to set JAVA_HOME !")
			continue
		print("JAVA_HOME successfullly set")
		z=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} echo export PATH=/usr/java/jdk1.8.0_171-amd64/bin/:'$PATH' >> /root/.bashrc".format(job_pass,job_ip))
		if z[0]!=0:
			print("Failed to set PATH variable !")
			continue
		print("PATH variable successfully set !")
		if subprocess.getstatusoutput('sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -q hadoop | grep "is not installed"'.format(job_pass,job_ip))[1]!='':
			h=subprocess.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} rpm -ivh /Softwares/share/Software/hadoop-1.2.1-1.x86_64.rpm --force".format(job_pass,job_ip))
			if h[0]!=0:
				print("Error in installing Hadoop!!!")
				continue
			else:
				print("Hadoop installed successfully!")	
		else:
			print("Hadoop already installed!")	
	#Mapred-site
			
		try:
			file_open=open('/etc/hadoop/mapred-site.xml','w') 
			file_open.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>mapred.job.tracker</name>
<value>{}:9002</value>
</property>
</configuration>""".format(job_ip))
			file_open.close()
			print("mapred-site.xml file successfully modified!")
		except IOError:
			print("Failed to update ")
			continue	
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
</configuration>""".format(name_ip))
			file_open.close()
			print("core-site.xml file successfully modified!")
		except IOError:
			print("Failed to update ")
			continue		
		try:
			fopen=open('/hosts.txt','a+')
			fopen.write("{}	{}".format(job_ip,job_host))
			fopen.close()
		except:
			print("Failed to update hosts file!")
			continue
		try:
			fopen=open('/ip.txt','a+')
			fopen.write("{}".format(job_ip))
			fopen.close()
			fopen=open('/p.txt','a+')
			fopen.write("{}".format(job_pass))
			fopen.close()
		except:
			print("Failed to update hosts file!")
			continue	
	elif ch==3:
		print("Please wait while changes are being saved...\n\n It may take a while...")
		fopen1=open('/ip.txt','r')
		ips=fopen1.read().split("\n")
		fopen2=open('/p.txt','r')
		passes=fopen2.read().split("\n")
		count=0
		for i in ips:
			count+=1
		i=0	
		while i<count:
			update=subprocess.getstatusoutput("sshpass -p {} scp -o StrictHostKeyChecking=no /hosts.txt root@{}:/etc/hosts".format(ips[i],passes[i]))
			if update[0]!=0:
				print("Failed to update system with changes!")
				print("Setup may not work....\nRetry!")
				exit()
			i+=1
