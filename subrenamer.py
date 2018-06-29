import os, sys, re
import subshifter

root_dir = sys.argv[1]

default = ""
shift = ""
sub_format = ".ass"
eps_format = ".mkv"

while True:
    default = input("Use default? (.ass/.mkv) (y/n): ")
    if(default.lower() == "y"):
        break
    elif(default.lower() == "n"):
        sub_format = input("Input file format of subtitles: ")
        eps_format = input("Input file format of episodes: ")
        break
    else:
        print("Please follow the prompt.")

while True:
    shift = input("Please input how much to shift (end with ms/f for milliseconds/frames, i.e. 24f): ")
    if re.match("\A[\d]*(.?[\d]+|[\d]*)(f|ms)$", shift):
        break
    else:
        print("Please follow the prompt.")

def rename_files():
    subs = []
    eps = []
    for root, dirs, files in os.walk(root_dir, topdown=True):
        dirs.clear()
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext == sub_format or ext == ("." + sub_format):
                subs.append(file)
            elif ext == eps_format or ext == ("." + eps_format):
                eps.append(file)
    subs.sort()
    eps.sort()
    print(len(subs))
    if len(subs) != len(eps):
        print("Amount of subtitles do not match amount of episodes! Subs = {0}, Eps = {1}".format(len(subs), len(eps)))
        return
    for sub, eps in zip(subs,eps):
        sub_name, sub_ext = os.path.splitext(sub)
        eps_name, eps_ext = os.path.splitext(eps)
        os.rename(os.path.join(root, sub), os.path.join(root, eps_name + sub_ext))
        subshifter.shift(os.path.join(root, eps_name + sub_ext), os.path.join(root, eps), shift)
    

rename_files()
os.system("pause")