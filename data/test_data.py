from halib import filesys
from halib import textfile
import re
from matplotlib.pyplot import hlines
import pandas as pd
from regex import F
from sklearn.model_selection import train_test_split
from colorama import Fore, Back, Style, init
import math
import random

init(autoreset=True)


def hLine():
    print(Fore.RED + '*' * 50)


def main():

    test_folder = './mobility4'

    num_class = int(re.findall(r'\d+', test_folder)[0])

    test_img_per_class = 100
    train_img_per_class = int(400 * 0.8)
    valid_img_per_class = int(400 * 0.2)

    require_dict = {'train': train_img_per_class, 'valid': valid_img_per_class, 'test': test_img_per_class}

    folders = filesys.list_dirs(test_folder)

    actual_info = {}

    # delete invalid image/label pairs
    for folder in folders:
        if 'new' in folder:
            continue
        img_files = filesys.list_files(f'{test_folder}/{folder}/images')
        files = filesys.list_files(f'{test_folder}/{folder}/labels')
        actual_info[folder + '_cat'] = {}
        # print(files[0])

        # delete empty files
        for f in files:
            path = f'{test_folder}/{folder}/labels/{f}'
            lines = textfile.read_line_by_line(path)
            if(len(lines) == 0):
                print(f'{path} is empty')
                filesys.delete_file(path)

        for img in img_files:
            k = img.rfind(".")
            txt_name = img[:k] + ".txt"
            path = f'{test_folder}/{folder}/images/{img}'
            path_txt = f'{test_folder}/{folder}/labels/{txt_name}'

            if(not filesys.is_file(path_txt)):
                print(Fore.RED + img)
                print(f'{path_txt} not exists')
                filesys.delete_file(path)

    # count by cate
    for folder in folders:
        if 'new' in folder:
            continue
        files = filesys.list_files(f'{test_folder}/{folder}/labels')
        actual_info[folder + '_cat'] = {}
        for f in files:
            path = f'{test_folder}/{folder}/labels/{f}'
            lines = textfile.read_line_by_line(path)
            cate = int(lines[0].split(' ')[0])

            if cate in actual_info[folder + '_cat']:
                actual_info[folder + '_cat'][cate]['count'] += 1
                actual_info[folder + '_cat'][cate]['files'] += [f]
            else:
                actual_info[folder + '_cat'][cate] = {'count': 1, 'files': [f]}

    print(actual_info)
    # duplicate

    for folder in folders:
        if 'new' in folder:
            continue
        folder_dict = actual_info[folder + '_cat']
        for cat in folder_dict:
            cat_dict = folder_dict[cat]
            no_cate = cat_dict['count']
            files = cat_dict['files']
            lack_no = require_dict[folder] - no_cate
            print(folder, cat, lack_no)

            to_copy_files = random.sample(files, lack_no)
            for cfile in to_copy_files:
                dest_folder_lb = f'{test_folder}/new/{folder}/labels'
                dest_folder_img = f'{test_folder}/new/{folder}/images'

                lb_file = f'{test_folder}/{folder}/labels/{cfile}'

                k = cfile.rfind(".")
                img_name = cfile[:k] + ".jpg"
                img_file = f'{test_folder}/{folder}/images/{img_name}'

                filesys.copy_file(lb_file, dest_folder_lb)
                filesys.copy_file(img_file, dest_folder_img)


if __name__ == "__main__":
    main()
