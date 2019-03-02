import os

def handleCSVTax(csv_fp):
    """
    Return dict of tax rate values


    """
    state_name = csv_fp.split('ZIP5_')[1][0:2]


dirpath = os.path.dirname(__file__)
directory = os.fsencode('data/TAXRATES_ZIP5')
dir_path = os.path.join(dirpath, '../../../'+'data/TAXRATES_ZIP5')

print(dir_path)
for file in os.listdir(dir_path):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"):
        #print(os.path.join(dir_path, filename))
        csv_fp = os.path.join(dir_path, filename)
        handleCSVTax(csv_fp)
        continue
    else:
        continue



