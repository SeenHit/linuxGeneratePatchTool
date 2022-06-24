#########

__author__ = "William <williamsukatube@gmail.com>"
__version__ = "v 0.1"

import os
import sys

### Usage:   python2 SendPathToCommunity.py xxx.patch

# get send patch args by linux kernel script
def get_send_patch_cmd():
	# mail_args is the cmd for send-email
	mail_args = "git send-email " + sys.argv[1]
	os.system("./scripts/get_maintainer.pl %s > maintainer.info" %(sys.argv[1]))

	with open("maintainer.info") as f:
		for line in f.readlines():
			if (line.count("open list", 0, len(line))):
				mail_args += " --to "
				mail_args += line.split(' ')[0]

			if (line.count("moderated list", 0, len(line))):
				mail_args += " --to "
				mail_args += line.split(' ')[0]

			if (line.count("maintainer:", 0, len(line))):
				begin = line.find('<')
				if (begin == -1):
					mail_args += " --to "
					mail_args += line.split(' ')[0]
				else:
					end = line.rfind('>')
					mail_args += " --to "
					mail_args += line[begin + 1 : end]

			if (line.count("reviewer:", 0, len(line))):
				begin = line.find('<')
				end = line.find('>')
				mail_args += " --cc "
				mail_args += line[begin + 1 : end]

			if (line.count("supporter:", 0, len(line))):
				begin = line.find('<')
				end = line.find('>')
				mail_args += " --cc "
				if (end == -1):
					mail_args += line.split(' ')[0]
				else:
					mail_args += line[begin + 1 : end]

	# do clean up
	f.close()
	os.system("rm -rf maintainer.info")

	print "mail info is :" + mail_args
	return mail_args

# check patch if patch exist error or warning
def checkpatch(patch_name):
	os.system("./scripts/checkpatch.pl %s > checkpatch.info" %(patch_name))
	with open("checkpatch.info") as f:
		data = f.readlines()
		for line in data:
			if (line.find("total") != -1 and line.find("0 errors, 0 warnings") == -1):
				print "checkpatch failed!!! please check formath again!!!"
				f.close()
				os.system("rm -rf checkpatch.info")
				os._exit(0)

	f.close()
	os.system("rm -rf checkpatch.info")
	print ("check patch success!")
	return 0

# send patch by shell command
def send_patch(mail_args):
	os.system(mail_args)

if __name__ == "__main__":
	checkpatch(sys.argv[1])
	mail_args = get_send_patch_cmd()
	send_patch(mail_args)
