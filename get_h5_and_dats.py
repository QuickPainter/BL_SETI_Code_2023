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

h5_list = []
data_dir = os.getcwd() + "/"

for dirname, _, filenames in os.walk(data_dir):
    for filename in filenames:
        if filename[-3:] == '.h5':
            h5_list.append(data_dir+filename)

target = data_dir.split('/')[-2]
print('target',target)

for file in h5_list:
    if f'_{target}_'.lower() in file.lower() and '_off_' not in file.lower():
        cmd = f"seticore --input {file} --output {data_dir}{file.split('/')[-1][:-3]}.dat -M 4 -s 10"
    else:
        cmd = f"seticore --input {file} --output {data_dir}{file.split('/')[-1][:-3]}.dat -M 4 -s 8"
    os.system("echo "+cmd)
    subprocess.run(cmd,shell=True)
