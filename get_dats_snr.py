
    #/Users/caleb/Berkeley_SETI/get_dats_snr.py

import os
import subprocess

h5_list = []
dat_list = []

data_dir = os.getcwd() + "/"

for dirname, _, filenames in os.walk(data_dir):
    for filename in filenames:
        if filename[-3:] == '.h5':
            h5_list.append(data_dir+filename)
        if filename[-4:] == '.dat':
            dat_list.append(data_dir+filename)

target = data_dir.split('/')[-2]
print('target',target)

# remove any files that have been processed
processed_dat_files = [i[:-4] for i in dat_list]
all_h5_files = [i[:-3] for i in h5_list]

files_left = list(set(processed_dat_files).symmetric_difference(set(all_h5_files)))
h5_files_left = [i+'.h5' for i in files_left]
print("LEFT",h5_files_left)

for file in h5_list:
    if f'_{target}_' in file and 'off' not in file:
        cmd = f"seticore --input {file} --output {data_dir}{file.split('/')[-1][:-3]}.dat -M 4 -s 10"
    else:
        cmd = f"seticore --input {file} --output {data_dir}{file.split('/')[-1][:-3]}.dat -M 4 -s 8"
    os.system("echo "+cmd)
    subprocess.run(cmd,shell=True)


