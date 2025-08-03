import os
import fontTools.ttLib
import shutil

def install(windows, dest):
    current = os.getcwd()
    dirs = os.listdir(current)
    if dest[0:-1] not in dirs:
        os.mkdir(dest[0:-1])
    get_fonts_from_windows(windows,dest)

def get_fonts_from_windows(windows, dest):
    path= windows
    target = dest
    directories = os.listdir(path)
    print(directories)
    for file in directories:
        if file[-4:].lower() =='.ttf':
            file_path = path + '/' + file
            font=fontTools.ttLib.TTFont(file_path)
            print(font['name'].getDebugName(4))
            shutil.copy(file_path,target)
            try:
                os.rename(f"{target}{file}",f"{target}{font['name'].getDebugName(4)}.ttf")
            except:
                os.remove(f"{target}{file}")