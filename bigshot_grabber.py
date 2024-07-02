import os
import shutil
import tkinter as tk
from tkinter import filedialog


shots_to_copy = []
root_dir = ""

# Just a UI and usage explanation
def menu():
    print('''\033[0;35m
  ____  _           _           _   
 |  _ \(_)         | |         | |  
 | |_) |_  __ _ ___| |__   ___ | |_ 
 |  _ <| |/ _` / __| '_ \ / _ \| __|
 | |_) | | (_| \__ \ | | | (_) | |_ 
 |____/|_|\__, |___/_| |_|\___/ \__|
           __/ |  v1.0                  
          |___/   Mass Shot Copying for Toonboom Producer Link - By Lannie Booton

    \033[0m''')

    print('''\033[0;36m
    Usage:
          1. Select the root folder where you have extracted your shots from Producer Link
          2. Type in the start of the prod code, ep#, or other shot id that is the same across ALL shots.
          3. Remember to delete ya extracted files you don't need afterwards, I'm not yer mum :)
    \033[0m''')


# Grabs the first round of folders
def explore_folders(regex):
    global root_dir

    for dir in os.listdir(root_dir):
        if dir.startswith(tuple(map(str, range(10)))):
            folder_path = os.path.join(root_dir, dir)

            print(f"Now checking subfolders of {os.path.normpath(folder_path)}")

            explore_subfolders(folder_path, regex)




# Loops through subfolders til it gets to the shots to copy out
def explore_subfolders(folder_path, regex):

    global shots_to_copy
    
    traversal = folder_path

    for dir in os.listdir(traversal):
        

        # Check if the directory starts with the program or episode code, if it doesn't then join it to the traversal so it can keep going deeper.
        # By default we know that Producer link doesn't send down files with our wanted folder in the first delve, 
        # so we start by checking that it doesn't match.
        try:
            if not dir.startswith(regex):
                
                traversal = os.path.join(traversal, dir)
                # print(f"Next to traverse: {os.path.normpath(traversal)}")

                explore_subfolders(traversal,regex)
            
            else:
                # print("\033[0;32mThis is probably the folder you're after:\033[0m")
                # print(dir)
                

                # Convert backslashes
                to_copy = os.path.join(traversal, dir)
                to_copy = os.path.normpath(to_copy)
                shots_to_copy.append(to_copy)

    

        except:
            print()
                  

def copy_folder():
    print(f"\033[1;32mThese are the shots that will be copied to {root_dir}:\033[0m")
    readout = "\n"
    print(readout.join(shots_to_copy))

    print(f"\n\033[1;32m{len(shots_to_copy)} shot(s) will be copied.\033[0m")
    input("Press any key to continue: ")

    for i in shots_to_copy:
        parent_folder = os.path.dirname(i)
        # print(parent_folder)
        success = shutil.copytree(parent_folder,root_dir, dirs_exist_ok=True)
        print(f"{i} copied to --> {success}")





# Main loop, obviously
def main():

    menu()

    # Set up Tkinter window and hide it
    root = tk.Tk()
    root.withdraw()

    global root_dir

    # Get user to select root directory where they've extracted files to
    print("\033[0;36m 1. Please select the working directory that you extracted the producer downloads to.\n\n\033[0m")
    root_dir = filedialog.askdirectory()
    
    # Check the user actually selected a directory to work from.
    if root_dir:
        print(f"Working folder: {root_dir}\n\n")
        regex = input("\033[0;36m 2. What do the shots start with? E.G production code, ep number, ID. All shots should start with this: \033[0m")


        explore_folders(regex)

        print("\n\n")
        copy_folder()

        print("-" * 50)

    else:
        print("No folder was selected. Exiting.")



if __name__ == "__main__":
    main()