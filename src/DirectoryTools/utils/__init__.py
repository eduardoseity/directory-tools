import os
import json
import datetime
from pathlib import Path
from colorama import Fore, Style

EQUAL_STYLE = Fore.RESET + Style.RESET_ALL
UPDATED_STYLE = Fore.YELLOW + Style.BRIGHT
NEW_STYLE = Fore.GREEN + Style.BRIGHT
DELETED_STYLE = Fore.RED + Style.BRIGHT
NORMAL_STYLE = Fore.RESET + Style.RESET_ALL

def save_info(info:list,filename:str=f'{datetime.datetime.now()}.json') -> None:
    with open(filename, 'w') as file:
        file.write(json.dumps(info))

def load_info(file_path:str) -> list:
    with open(file_path,'r') as file:
        info = json.loads(file.read())
    return info    

def print_info(info:list):
    print('')
    for i in info:
        if i['status'] == 'deleted':
            style = DELETED_STYLE
        elif i['status'] == 'updated':
            style = UPDATED_STYLE
        elif i['status'] == 'new':
            style = NEW_STYLE
        elif i['status'] == 'equal':
            style = EQUAL_STYLE
        else:
            style = NORMAL_STYLE

        print(style + i['path'])
    print()
    print(f"{EQUAL_STYLE}[untouched] {UPDATED_STYLE}[updated] {NEW_STYLE}[new] {DELETED_STYLE}[deleted]")
    print(NORMAL_STYLE)

def extract_info(path:str) -> list | bool: 
    if not os.path.exists(path):
        return False
    path = os.path.abspath(path)
    info = []
    for root, _, files in os.walk(path):
        p = os.path.join(root)
        info.append(__get_info(p))

        for file in files:
            p = os.path.join(root, file)
            info.append(__get_info(p))
    return info    

def __get_info(path:str) -> dict:
    size = os.path.getsize(path)
    type = 'file' if os.path.isfile(path) else 'folder'
    created = os.path.getctime(path)
    modified = os.path.getmtime(path)
    return {
        'path': path,
        'size': size,
        'type': type,
        'created': created,
        'modified': modified
    }

def __find_info(info:list,path:str,type:str) -> tuple:
    for index,i in enumerate(info):
        if Path(i['path']) == Path(path) and i['type'] == type:
            return index, i
    return None, False

def compare_directories(info1:list,info2:list) -> list:
    comparison = []
    info2_index = []
    for i1 in info1:
        index, info = __find_info(info2,i1['path'],i1['type'])
        if info == False:
            i1['status'] = 'deleted'
        else:
            info2_index.append(index)
            info = __compare_info(i1,info)
            if info == None:
                i1['status'] = 'equal'
            else:
                i1.update(info)
                i1['status'] = 'updated'
        comparison.append(i1)

    for index, i2 in enumerate(info2):
        if index in info2_index:
            continue
        i2['status'] = 'new'
        comparison.append(i2)

    comparison = sorted(comparison, key=lambda d: d['path'])

    return comparison

def __compare_info(info1:dict,info2:dict):
    attrs = ['size','created','modified']
    info = {}
    for attr in attrs:
        if info1[attr] != info2[attr]:
            info[attr] = [info1[attr], info2[attr]]
    if len(info.keys()) == 0:
        return None
    else:
        return info