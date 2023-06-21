import subprocess
import sys
import os


def main(off_snr):
    main_dir = os.getcwd() + "/"
   
    target_list = ['AND_II', 'AND_I', 'AND_X', 'AND_XI', 'AND_XIV', 'AND_XVI', 'AND_XXIII', 'AND_XXIV', 'BOL520', 'CVNI', 'DDO210', 'DRACO', 'DW1', 'HERCULES', 'HIZSS003', 'IC0010', 'IC0342', 'IC1613', 'LEOA', 'LEOII', 'LEOT', 'LGS3', 'MAFFEI1', 'MAFFEI2', 'MESSIER031', 'MESSIER033', 'MESSIER081', 'MESSIER101', 'MESSIER49', 'MESSIER59', 'MESSIER60', 'MESSIER84', 'MESSIER86', 'MESSIER87', 'NGC0185', 'NGC0628', 'NGC0672 ', 'NGC1052', 'NGC1172 ', 'NGC1400', 'NGC1407', 'NGC2403'] 
    for target in target_list:
        print("Downloading Data for target:",target)
        already = grab_data(target)
        
        print("Running Seticore for target:",target)
        get_dats(off_snr)
        os.chdir(main_dir)


def grab_data(target):

    try:
        os.mkdir(target)
        os.chdir(target)
    except:
        os.chdir(target)
        print("directory already exists")
        print("Checking that all .h5 files have corresponding .dat files")
        return True
        

    

    cmd1 = f"grep '{target},' /home/cgchoza/complete_cadences_catalog.csv | grep ',L,' > {target}.csv"
    subprocess.run(cmd1,shell=True)
    cmd2 = '''awk -F "\\"*,\\"*" '{print $6}' '''+ f'''{target}.csv > filelist.txt'''
    subprocess.run(cmd2,shell=True) 
    cmd3 = '''awk -F "\\"*,\\"*" '{print $7}' '''+ f'''{target}.csv > datlist.txt'''
    subprocess.run(cmd3,shell=True)
    cmd4 = '''awk '{print "ln -s", $1, "."}' filelist.txt |  csh'''
    subprocess.run(cmd4,shell=True) 
    return False

def get_dats(off_snr):
    subprocess.run(f"echo '{off_snr}' >> s_val.txt",shell=True) 
    h5_list = []

    
    data_dir = os.getcwd() + "/"

    for dirname, _, filenames in os.walk(data_dir):
        for filename in filenames:
            if filename[-3:] == '.h5':
                h5_list.append(data_dir+filename)

    # grab just name of files to see if they are in .h5

    h5_files_converted = []
    for dirname, _, filenames in os.walk(data_dir):
        for filename in filenames:
            if filename[-4:] == '.dat':
                h5_files_converted.append(data_dir+filename[:-4]+".h5")

    target = data_dir.split('/')[-2]
    print('Target',target)
    print("Target has this many .h5 files:",len(h5_list))
    remaining_h5 = list(set(h5_files_converted).symmetric_difference(set(h5_list)))

    if len(remaining_h5) > 0:
        print(f"There were {len(remaining_h5)} h5 files not yet converted. Converting those now.")
        print(remaining_h5)
        h5_list = remaining_h5


        for file in h5_list:
            if f'_{target}_'.lower() in file.lower() and '_off_' not in file.lower():
                cmd = f"seticore --input {file} --output {data_dir}{file.split('/')[-1][:-3]}.dat -M 4 -s 10"
            else:
                cmd = f"seticore --input {file} --output {data_dir}{file.split('/')[-1][:-3]}.dat -M 4 -s {off_snr}"
            os.system("echo "+cmd)
            subprocess.run(cmd,shell=True)

if __name__ == '__main__':
    off_snr = sys.argv[1]
    main(off_snr)



    '''batch1 = ['AND_II', 'AND_I', 'AND_X', 'AND_XI', 'AND_XIV', 'AND_XVI', 'AND_XXIII', 'AND_XXIV', 'BOL520', 'CVNI', 'DDO210', 'DRACO', 'DW1', 'HERCULES', 'HIZSS003', 'IC0010', 'IC0342', 'IC1613', 'LEOA', 'LEOII', 'LEOT', 'LGS3', 'MAFFEI1', 'MAFFEI2', 'MESSIER031', 'MESSIER033', 'MESSIER081', 'MESSIER101', 'MESSIER49', 'MESSIER59', 'MESSIER60', 'MESSIER84', 'MESSIER86', 'MESSIER87', 'NGC0185', 'NGC0628', 'NGC0672 ', 'NGC1052', 'NGC1172 ', 'NGC1400', 'NGC1407', 'NGC2403'] 
    batch2 = ['NGC2683', 'NGC2787', 'NGC3193', 'NGC3226', 'NGC3344', 'NGC3379', 'NGC4136', 'NGC4168', 'NGC4239', 'NGC4244', 'NGC4258', 'NGC4318', 'NGC4365', 'NGC4387', 'NGC4434', 'NGC4458', 'NGC4473', 'NGC4478', 'NGC4486B', 'NGC4489', 'NGC4551', 'NGC4559', 'NGC4564', 'NGC4600', 'NGC4618', 'NGC4660', 'NGC4736', 'NGC4826', 'NGC5194', 'NGC5195', 'NGC5322', 'NGC5638', 'NGC5813', 'NGC5831', 'NGC584', 'NGC5845', 'NGC5846', 'NGC596', 'NGC636', 'NGC6503', 'NGC6822', 'NGC6946', 'NGC720', 'NGC7454 ', 'NGC7640', 'NGC821', 'PEGASUS', 'SAG_DIR', 'SEXA', 'SEXB', 'SEXDSPH', 'UGC04879', 'UGCA127', 'UMIN']'''