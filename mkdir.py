import os
from os.path import expanduser
from pathlib import Path
home = str(Path.home())
print("home path",home)

home = expanduser('~')
print("/////",home)

dl_path =  home + '/Downloads/PDMB'

def main():
    if not os.path.exists(dl_path):
       print ("path doesn't exist. trying to make")
       os.makedirs(dl_path)


if __name__ == '__main__':
    main()
