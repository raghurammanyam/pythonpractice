from zipfile import ZipFile
import os
from os.path import expanduser
home = expanduser('~')



def main():


    file_paths=[]

    for root, directories, files in os.walk(home+'/copy/passport'):
        for filename in files:
            print(filename)
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    with ZipFile(home+'/'+'my_python_files.zip','w') as zip:
        for file in file_paths:
            zip.write(file)

    


if __name__ == "__main__":
    main()
