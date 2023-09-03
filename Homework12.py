import pickle
from collections import UserDict
from datetime import datetime, timedelta
import re
import os
import json
# Hello, Vitaliрy!рррр
class Field:
    def __init__(self, value):
        self.__value=None
        self.value=value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self.__value=None
        self.value=value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value:
            pattern_for_phone=r'^\+?\d{11,16}$|^\d{10,12}$|^\+?\d{0,4}\(\d{3}\)\d{7,9}$|^\+?\d{0,4}\(\d{3}\)\d{1,3}-\d{1,3}-\d{1,3}$|^\(\d{3}\)\d{1,3}-\d{1,3}-\d{1,3}|^\d{3}-\d{1,3}-\d{1,3}-\d{1,3}$'
            if re.match(pattern_for_phone, value):
                self.__value=value
            else:
                raise ValueError('Invalid phone number format, use correct one that can include "+" or/and "-", pair of "(...)" or just number by lenght from 10 to 16 symbols')



class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value:
            try:
                datetime.strptime(value, "%Y-%m-%d")
                self.__value = value
            except ValueError:
                raise ValueError("Invalid date format, format should be like 2000-01-31")


class Record:
    def __init__(self, name: str, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birt_list = []
        self.birthday=birthday
        if phone:
            self.add_phone(phone)
        if birthday:
            self.listb(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone).value)

    def listb(self,birthday):
        self.birt_list.append(Birthday(birthday).value)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.get_value() == phone:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.get_value() == old_phone:
                p.set_value(new_phone)

    def days_to_birthday(self):
        today = datetime.today()
        if self.birt_list:
            birthday_date = datetime.strptime(self.birt_list[0], "%Y-%m-%d")
            next_birthday = birthday_date.replace(year=today.year)
            if next_birthday < today and next_birthday.day!=today.day:
                next_birthday = next_birthday.replace(year=today.year + 1)
            elif next_birthday < today and next_birthday.day==today.day:
                return f"0 days, congratulate today"
            days_left = (next_birthday - today).days
            return f"{days_left} days"
        else:
            return "unreal to measure days because of lack data"


class AddressBook(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_size = 1 # Розмір однієї сторінки
        self.current_page = 0

    def __call__(self,n=0):
        if n:
            self.page_size = n  # Розмір однієї сторінки
        return self.__iter__()

    def __iter__(self):
        self.current_page = 0
        return self

    def __next__(self):
        start_idx = self.current_page * self.page_size
        end_idx = (self.current_page + 1) * self.page_size
        records = list(self.data.values())[start_idx:end_idx]
        if not records:
            raise StopIteration
        self.current_page += 1
        yield records

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, n=None):
        try:
            generator = address_book(n)
            for records_list in generator:
                for records in records_list:
                    print(f"--------------PAGE {self.current_page}---------------")
                    for record in records:
                        print(f"|->Name: {record.name.value}")
                        for phone in record.phones:
                            print(f"|->Phone: {phone}")
                        for _ in record.birt_list:
                            print(f"|->Total days to Birthday: {record.days_to_birthday()}")
                        print("***********************************")
        except RuntimeError:
            return ">>>>>>>>>>>>>>>END<<<<<<<<<<<<<<<<<"

    def find(self):
        search_str=str(input("Enter the name or number or phone fully or partly: ")).lower()
        start="*******************************\n"
        result=""
        for name,phone in self.data.items():
            name_lower=name.lower()
            if search_str in name_lower:
                result+=f"|->Name: {name}\n|->Phone: {','.join(phone.phones)}\n|->Total days to Birthday: {phone.days_to_birthday()}\n-------------------------------\n"
            for el in phone.phones:
                if search_str in el:
                    result+=f"|->Name: {name}\n|->Phone: {el}\n|->Total days to Birthday: {phone.days_to_birthday()}\n-------------------------------\n"
        if result=="":
            result="There's no exist the same ontact\n"
        end="*******************************"
        print(start+result+end)


    def dump(self):
        file_name=input("Write name of file that should be created in format 'name.file extension': ")
        with open(file_name,"wb") as file:
            pickle.dump(self.data,file)
            print("It's ok. Operation Dump has finished")

    def load(self):
        while True:
            file_name = input("Write name of file from where should be imported data in format 'name.file extension': ")
            try:
                with open(file_name, "rb") as file:
                    self.data=pickle.load(file)
                    print("It's ok. Operation Load has finished")
                    break
            except:
                print("There's no exists. Enter true filename!")







if __name__ == "__main__":
    address_book = AddressBook()
    record1 = Record("Dima Smith")
    record2 = Record("Jane Smith", "+38(798)5433521", "1959-08-26")
    record3 = Record("Jane Rozhko", "22228765664321", "1925-10-6")
    record4 = Record("Stas Polyakov", "222287654321", "1925-08-24")
    record5 = Record("Ksusha Onegina", "123456789133", "1925-08-07")
    record6 = Record("Vitalik Ivanov", "12345678789133", "1925-08-18")

    record1.add_phone("+380984335213")

    address_book.add_record(record1)
    address_book.add_record(record2)
    address_book.add_record(record3)
    address_book.add_record(record4)
    address_book.add_record(record5)
    address_book.add_record(record6)




