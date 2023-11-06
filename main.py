from collections import UserDict

from datetime import datetime

from itertools import islice

import pickle

import os.path



class Field:
    def __init__(self, value: str) -> None:
        self.value = value

class Name(Field):
    def __init__(self, name: str) -> None:
        self.value = name

    def __str__ (self) -> str:
        return f"{self.value}"

class Birthday(Field):
    def __init__(self, value)-> None:
        self._value = None
        self._date_format = "%Y-%m-%d"
        self.value = value
            
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if value:
            self._value = datetime.strptime(value, self._date_format)


    def __str__(self):
        if self.value:
            return datetime.strftime(self.value, self._date_format)
        return ("Birthday - not set")

class Phone(Field):
    def __init__ (self, phone: str) -> None:
        self._value = None
        self.value = phone

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, phone):
        if not all([len(phone) == 10 and phone.isdigit()]):
            raise ValueError ("Please enter phone number in 10 digit format")
        self._value = phone

    def __repr__ (self) -> str:
        return self.value

    def __str__ (self) -> str:
        return f"{self.value}"

    def __eq__(self, __value: object) -> bool:
        return self.value == __value.value

class Record:
    def __init__(self, name: str, phone=None, birthday=None) -> None:
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.birthday = Birthday(birthday)

    def add_birthday(self, birthday):
        if self.birthday.value:
            raise ValueError ("Contact have Birthday date. Can`t add one more date.")
        self.birthday = Birthday(birthday)
        return self.birthday

    def add_phone(self, phone: str) -> list:
        new_phone = Phone(phone)
        if new_phone not in self.phones:
            return self.phones.append(new_phone)
        raise  ValueError("The phone number is already in the list")
         
    def edit_phone(self, phone: str, new_phone: str) -> str:
        old_phone = Phone(phone)
        new_phone = Phone(new_phone)
        if old_phone in self.phones:
            self.phones[self.phones.index(old_phone)] = new_phone
            return 
        raise ValueError("The phone number not in the list")
        
    def remove_phone(self, phone: str) -> list:
        rem_phone = Phone(phone)
        if phone in self.phones:
            return self.phones.remove(rem_phone)
        return "This phone number is not in list"

    def find_phone(self, phone: str) -> str:
        phone_to_find = Phone(phone)
        if phone_to_find in self.phones:
            return phone_to_find
        raise ValueError("This phone number is not in list")

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birthday = self.birthday.value.replace(year=today.year)
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_to_next_birthday = (next_birthday - today).days
            print(f"{days_to_next_birthday} days until next Birthday!")
            return days_to_next_birthday
        raise ValueError("No Birthday date in Address Book")

    def __repr__(self):
        phone_numbers = ', '.join(str(phone) for phone in self.phones)
        birthday = self.birthday if self.birthday else "Birthday - not set"
        return f'{self.name} - {phone_numbers}: {birthday}'

    def __str__(self):
        phone_numbers = ', '.join(str(phone) for phone in self.phones)
        birthday = self.birthday if self.birthday else "Birthday - not set"
        return f'{self.name} - {phone_numbers}: {birthday}'

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}
        self.counter = 0        

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        print("Record added")
        return

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            print("Record not found")

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
        else:
            print("Record not found")  
    
    def search_in_rec(self, somedata: str):
        search_results = []
        search_data = somedata.lower()
        for name, record in book.data.items():
            if search_data in name.lower():
                search_results.append(record)
            if search_data.isdigit():
                for phone in record.phones:
                    ph = phone.value[:]
                    if str(search_data) in str(ph):
                        search_results.append(record)
        if not search_results:
            print("Nothing to find for your request")
        return search_results

    def iterator(self, lines=None):
        if not lines:
            lines = len(self.data)
        while self.counter < len(self.data):
            for item in islice(self.data.items(), self.counter, lines):
                print(item[1])
                yield             
            self.counter += lines    

def read_from_file(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as fn:
            book = pickle.load(fn)
    else:
        book = AddressBook()
    return book   

def write_to_file(filename, book):
    with open(filename, "wb") as fn:
        pickle.dump(book, fn)

if __name__ == "__main__":
    # UserIvan = Record("Ivan")
    # UserIvan.add_phone("7777777777")
    # print(UserIvan)
    # UserIvan.add_phone("2222222222")
    # print(UserIvan)
    # UserIvan.edit_phone("2222222222", "1111111111")
    # print(UserIvan)
    # # UserIvan.remove_phone("1111111111")
    # # print(UserIvan)

    # book = AddressBook()
    # book.add_record(UserIvan)
    # print(str(book))

    # UserAndrey = Record("Andrey")
    # UserAndrey.add_phone("1212121212")
    # book.add_record(UserAndrey)
    # print(book)

    # for name, record in book.data.items():
    #     print(record)

    # john = book.find("Andrey")
    # print(john)

    # Створення нової адресної книги
    # book = AddressBook()

    filename = 'book.bin'

    book = read_from_file(filename)

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # # Видалення запису Jane
    # book.delete("Jane")

    john_record.add_birthday("1900-10-20")
    print(john_record)

    john_record.days_to_birthday()

    print(book.search_in_rec("55"))

    # for re in book.iterator():
    #     input("Press")


    write_to_file(filename, book)
