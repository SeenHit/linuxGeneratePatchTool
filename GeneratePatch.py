#########

__author__ = "William <williamsukatube@gmail.com>"
__version__ = "v 0.1"

from collections import Counter
import time
import sys
import os

def getPrefixFromCommit(commitID):
	cmd = "git show " + commitID + " > percommit"
	os.system(cmd)

	count = 0
	prefix = ""
	with open("percommit") as f_percommit:
		for line in f_percommit.readlines():
			count = count + 1
			prefix = line.strip()
			if (count == 5):
				break

	f_percommit.close()
	os.system("rm percommit")
	return prefix

def getFixesString(filepath):
	strlist = filepath.split(':')
	fileName = strlist[1].strip()
	fileLineNumber = strlist[2].strip()

	cmd = "git blame -L " + fileLineNumber + "," + fileLineNumber + " " + fileName + " > blame"
	os.system(cmd)
	fixString = "Fixes: "

	with open("blame") as f_blame_info:
		commitInfo = f_blame_info.readline()
		commitID = commitInfo.split(' ')[0]
		fixString = fixString + commitID + " "
		commitPrefix = getPrefixFromCommit(commitID)
		fixString = fixString + "(\"" + commitPrefix + "\")"
		#print ("!!!!" + fixString + " " + commitPrefix + " \n")

	f_blame_info.close()
	os.system("rm blame")
	return fixString

def get_modify_file_path():
	file_path = ""

	os.system("git diff > head.info")
	with open("head.info") as f_head_info:
		file_path = f_head_info.readline()
		if file_path == "":
			#print ("no file has changed, please check git status\n")
			f_head_info.close()
			os.system("rm head.info")
			os._exit(0)

	f_head_info.close()
	os.system("rm head.info")

	file_path = file_path.split(' ')[3][2 : len(file_path) - 1]
	return file_path

def get_commit_msg_prefix(file_path):
	list_prefix = []

	cmd = "git log --oneline -20 " + file_path[0 : len(file_path) - 1] + " > onelinelog.info"
	os.system(cmd)

	with open("onelinelog.info") as f_log:
		for line in f_log.readlines():
			begin = line.find(' ')
			end = line.rfind(': ')
			if (end == -1):
				continue
			list_prefix.append(line[begin + 1 : end + 1])
	f_log.close()

	os.system("rm -rf onelinelog.info")
	word_counts = Counter(list_prefix)
	real_prefix = word_counts.most_common(1)[0][0]

	return real_prefix

def reset_commit_msg():
	content = ""
	with open("commitmsg.info", 'r') as f_commit:
		line = f_commit.readline()
		begin = line.rfind(':')
		f_commit.seek(begin + 2, 0)
		content = f_commit.read()
	f_commit.close()

	os.system("rm -rf commitmsg.info")
	with open("commitmsg.info", 'w') as f_commit:
		f_commit.write(content)
	f_commit.close()

def format_patch(real_prefix, file_path):
	os.system("git stash")

	with open("commitmsg.info", 'r+') as f_commit:
		line = f_commit.readline()
		f_commit.seek(0, 0)

		content = ""
		for line in f_commit.readlines():
			if (line.find("Fixes:") != -1 and line.find(".c") != -1):
				content = content + getFixesString(line) + "\n"
			else:
				content = content + line
		
		f_commit.seek(0, 0)
		f_commit.write(real_prefix + " " + content)
	f_commit.close()
	os.system("git stash pop")	
	os.system("git add -u")	
	os.system("git commit -F commitmsg.info")
	reset_commit_msg()

	try:
		if "-b" in sys.argv[1] or "BUGFIX" in sys.argv[1]:
			os.system("git format-patch -1 --subject-prefix=\"PATCH\" > format.info")
		else:
			os.system("git format-patch -1 --subject-prefix=\"PATCH -next\" > format.info")
	except:
		os.system("git format-patch -1 --subject-prefix=\"PATCH -next\" > format.info")

	with open("format.info") as f_format:
		patch_name = f_format.readline()
	print ("patch name is " + patch_name)
	f_format.close()
	os.system("rm -rf format.info")

	return patch_name

if __name__ == "__main__":			
	file_path = get_modify_file_path()
	real_prefix = get_commit_msg_prefix(file_path)
	patch_name = format_patch(real_prefix, file_path)


