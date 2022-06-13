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
import json

init(autoreset=True)


def hLine():
    print(Fore.RED + '*' * 50)


def del_invalid_pair_img_lb(test_folder, ignore_dirs):
    # delete invalid image/label pairs
    folders = filesys.list_dirs(test_folder)
    for folder in folders:
        if folder in ignore_dirs:
            continue
        img_files = filesys.list_files(f'{test_folder}/{folder}/images')
        files = filesys.list_files(f'{test_folder}/{folder}/labels')

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


def count_img_by_category(test_folder, ignore_dirs):
    count_info = {}
    folders = filesys.list_dirs(test_folder)

    # count by cate
    for folder in folders:
        if folder in ignore_dirs:
            continue
        files = filesys.list_files(f'{test_folder}/{folder}/labels')
        count_info[folder] = {}
        for f in files:
            path = f'{test_folder}/{folder}/labels/{f}'
            lines = textfile.read_line_by_line(path)
            cate = int(lines[0].split(' ')[0])

            if cate in count_info[folder]:
                count_info[folder][cate]['count'] += 1
                count_info[folder][cate]['files'] += [f]
            else:
                count_info[folder][cate] = {'count': 1, 'files': [f]}
    return count_info


def duplicate_to_get_required_size(test_folder, require_dict, count_info, ignore_dirs):
    folders = filesys.list_dirs(test_folder)
    for folder in folders:
        if folder in ignore_dirs:
            continue

        folder_dict = count_info[folder]
        for cat in folder_dict:
            cat_dict = folder_dict[cat]
            no_cate = cat_dict['count']
            files = cat_dict['files']
            lack_no = require_dict[folder] - no_cate
            print(folder, cat, len(files), Fore.GREEN + str(require_dict[folder]), Fore.RED + str(lack_no))

            if(lack_no <= 0):
                continue
            if(lack_no > len(files)):
                lack_no = len(files)

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


def split_train_val(test_folder, count_info, train_img_per_class, valid_img_per_class):
    train_dict = count_info['train']
    for cate in train_dict:
        cate_files = train_dict[cate]['files']
        if len(cate_files) == train_img_per_class:
            continue
        
        valid_files = random.sample(cate_files, valid_img_per_class)
        for lb_file in valid_files:
            k = lb_file.rfind(".")
            img_name = lb_file[:k] + ".jpg"
            img_file_path = f'{test_folder}/train/images/{img_name}'
            lb_file_path = f'{test_folder}/train/labels/{lb_file}'
            
            filesys.move_dir_or_file(img_file_path, f'{test_folder}/valid/images')
            filesys.move_dir_or_file(lb_file_path, f'{test_folder}/valid/labels')

def main():

    test_folder = './mobility15'

    test_img_per_class = 100
    train_img_per_class = int(400 * 0.8)
    valid_img_per_class = int(400 * 0.2)

    # train_img_per_class = 400
    # valid_img_per_class = 0

    require_dict = {'train': train_img_per_class, 'valid': valid_img_per_class, 'test': test_img_per_class}

    del_invalid_pair_img_lb(test_folder, ignore_dirs=['new'])
    count_info = count_img_by_category(test_folder, ignore_dirs=['new'])

    print(json.dumps(require_dict, sort_keys=True, indent=4))
    hLine()
    print(json.dumps(count_info, sort_keys=True, indent=4))
    hLine()
    duplicate_to_get_required_size(test_folder, require_dict, count_info, ignore_dirs=['new'])
    print(Fore.MAGENTA + str(require_dict))

    split_train_val(test_folder, count_info, train_img_per_class, valid_img_per_class)


if __name__ == "__main__":
    main()
