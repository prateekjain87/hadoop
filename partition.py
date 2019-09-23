#fdisk -l /dev/sdc | grep /dev/sdc: | awk {'print $3'}  // sizeof(sdc)



import subprocess
import os
ch="Y"
while ch=="Y" or ch=="y":
	print("\t\t\tWelcome to partition creation menu!")
	print("Disk 1 (sdb)\nDisk 2 (sdc)")
	drive=input("Enter the name of drive to create the partition in (sd*): ")
	if drive=="sdb":
		total= subprocess.getstatusoutput("fdisk -l /dev/sdb | grep /dev/sdb: | awk {'print $3'}")
		print("Total size of partition is: ",total)
			
		print("Partition table of sdb drive is:")
		print("echo 'print \n q' | parted /dev/sdb | grep extended | awk {'print $1'}")
		total= subprocess.getstatusoutput("fdisk -l /dev/sdc | grep /dev/sdc: | awk {'print $3'}")
		print("Total size of disk (in MB): ",total)
			
		subprocess.getstatusoutput("echo 'n\np\n2\n\n\n\nw' | fdisk /dev/{}".format(drive)

	elif drive=="sdc":




	else:
		print("Wrong partition number!")

	ch=input("Want to make another partition?(Y/N)")
	if ch=="y" or ch=="Y":
		continue
	else:
		exit()
