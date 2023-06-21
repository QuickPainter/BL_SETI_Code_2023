import subprocess
import sys
import os


target = sys.argv[1]

try:
    os.mkdir(target)
except:
    print("directory already exists")

os.chdir(target)

cmd1 = f"grep '{target},' /home/cgchoza/complete_cadences_catalog.csv | grep ',L,' > {target}.csv"
subprocess.run(cmd1,shell=True)
cmd2 = '''awk -F "\\"*,\\"*" '{print $6}' '''+ f'''{target}.csv > filelist.txt'''
subprocess.run(cmd2,shell=True)
cmd3 = '''awk -F "\\"*,\\"*" '{print $7}' '''+ f'''{target}.csv > datlist.txt'''
subprocess.run(cmd3,shell=True)
cmd4 = '''awk '{print "ln -s", $1, "."}' filelist.txt |  csh'''
subprocess.run(cmd4,shell=True)

    