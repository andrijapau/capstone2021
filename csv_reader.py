from os import listdir
from os.path import isfile, join




def find_files(mypath):
    onlyfiles = [[f.split('_')] for f in listdir(mypath) if isfile(join(mypath, f)) and f[0:8] == 'MATHUSLA']
    print(onlyfiles)

find_files("./data/")