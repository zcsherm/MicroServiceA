import os
import fontTools.ttLib
import shutil

def install(windows, dest):
    # Get the current directory
    current = os.getcwd()
    dirs = os.listdir(current)

    # If we havent made the destination directory yet, make it
    if dest[0:-1] not in dirs:
        os.mkdir(dest[0:-1])
    get_fonts_from_windows(windows,dest)

def get_fonts_from_windows(windows, dest):
    """
    Fetches all fonts built in to windows, copies them to folder locally
    """
    path= windows
    target = dest
    directories = os.listdir(path)

    # Iterate through all files in windows/fonts
    for file in directories:

        # Check for .tff files
        if file[-4:].lower() =='.ttf':

            # Get the fonts name and copy it to the new directory
            file_path = path + '/' + file
            font=fontTools.ttLib.TTFont(file_path)
            print(font['name'].getDebugName(4))
            shutil.copy(file_path,target)

            # Try to rename the file to a clearer name. If the names taken, just delete the file as it is a duplicate.
            try:
                os.rename(f"{target}{file}",f"{target}{font['name'].getDebugName(4)}.ttf")
            except:
                os.remove(f"{target}{file}")