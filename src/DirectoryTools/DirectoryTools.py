from utils import extract_info, save_info, load_info, print_info, compare_directories
from pathlib import Path
from datetime import datetime

class DirectoryTools:
    def __init__(self) -> None:
        self.__slot1 = None
        self.__slot1_info = 'Nothing loaded'
        self.__slot2 = None
        self.__slot2_info = 'Nothing loaded'
        self.__comparison = None

    def export_comparison(self,file_path:str=None) -> None:
        if self.__comparison == None:
            raise Exception('Nothing was compared. Run compare().')

        if file_path == None: file_path = f"{datetime.now()}.comparison"

        path = Path(file_path)
        if path.suffix != '.comparison':
            raise Exception('File suffix has to be .comparison')
        
        save_info(self.__comparison,path)
        print(f'Comparison has been exported to {path.absolute()}')

    def export_slot(self,slot:int,file_path:str=None) -> None:
        if slot == 1:
            info = self.__slot1
        elif slot == 2:
            info = self.__slot2
        else:
            raise Exception('Slot must be 1 or 2')
        if info == None:
            raise Exception(f'Slot {slot} is empty.')
        
        if file_path == None: file_path = f"{datetime.now()}.slot"

        path = Path(file_path)
        if path.suffix != '.slot':
            raise Exception('File suffix has to be .slot')
        
        save_info(info,path)
        print(f'Slot {slot} content has been exported to {path.absolute()}')

    def load_slot(self,slot_num:int,from_:str,path:str) -> None:
        if from_ == 'loadfile':
            self.__load_from_file(path,slot_num)
        elif from_ == 'loadpath':
            self.__load_from_path(path,slot_num)

    def __load_from_file(self,file_path:str,load_num:int) -> None:
        if load_num == 1:
            self.__slot1 = load_info(file_path)
            self.__slot1_info = f"[from file] {file_path}"
        elif load_num == 2:
            self.__slot2 = load_info(file_path)
            self.__slot2_info = f"[from file] {file_path}"
        else:
            raise IndexError('load_num must be 1 or 2')
        self.__comparison = None
    
    def __load_from_path(self,path:str,load_num:int) -> None:
        if load_num == 1:
            self.__slot1 = extract_info(path)
            self.__slot1_info = f"[from path] {path}"
        elif load_num == 2:
            self.__slot2 = extract_info(path)
            self.__slot2_info = f"[from path] {path}"
        else:
            raise IndexError('load_num must be 1 or 2')
        self.__comparison = None
        
    def compare(self) -> None:
        if self.__slot1 == None or self.__slot2 == None:
            if self.__slot1 == None and self.__slot2 == None:
                raise Exception('Slot 1 and 2 have no directory loaded')
            elif self.__slot1 == None:
                raise Exception('Slot 1 has no directory loaded')
            elif self.__slot2 == None:
                self.__load_from_path(self.__slot1[0]['path'],2)
        self.__comparison = compare_directories(self.__slot1, self.__slot2)
    
    def get_comparison(self) -> list:
        return self.__comparison

    def print(self) -> None:
        print_info(self.__comparison)

    def info(self) -> None:
        print('-'*50)
        print('Slot 1:', self.__slot1_info)
        print('Slot 2:', self.__slot2_info)
        if self.__slot1 == None or self.__slot2 == None:
            print('One or more slots are empty')
            print('Use load_from_file() or load_from_path() to load.')
        print()
        if self.__comparison == None:
            print('Nothing compared yet')
            print('Use compare() and then print() to see the comparison.')
        else:
            print('Slots have already compared')
            print('Use print() to see the comparison.')
        print('-'*50)