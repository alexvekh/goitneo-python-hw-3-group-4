from collections import UserDict
from datetime import datetime
from birthdays import get_birthdays_per_week

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if len(value) > 0 and value[0].isalpha():
            self.value = value.title()
        else:
            raise ValueError('Name should starts with letter')

class Phone(Field):
    def __init__(self, value):
        #super().__init__(value)
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise ValueError('Phone should be 10 digits format')

class Birthday(Field):
    def __init__(self, value: str):
        if len(value) != 10 or not value.count('.') == 2:
            raise ValueError('Invalid date format: Please use DD.MM.YYYY')
        try:
            datetime_obj = datetime.strptime(value, '%d.%m.%Y')
            self.value = datetime_obj.date()
        except ValueError as e:
            raise ValueError('Invalid date value: ' + str(e))
        
        
        
        # else:
        #     dd, mm, yyyy = value.split('.')
        #     print(dd, mm, yyyy)
        #     if int(dd) not in range(31):
        #         raise ValueError('Day should be in range 1-31')
        #     if int(mm) not in range(12):
        #         raise ValueError('Month should be in range 1-12')
        #     if int(yyyy) not in range(1900, 2024):
        #         raise ValueError('Year excepted in range 1900-2024')
        #     self.value = datetime.strptime(value, '%d.%m.%Y').date()
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_phone(self, value):
        self.phones.append(Phone(value))

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, phone, new_phone):
        found = False
        for p in self.phones:
            if p.value == phone:
                p.value = new_phone
                print(f"Phone {phone} was changed to {new_phone}.")
                found = True
        if not found:
            print(f'Phone {phone} wasn\'t found') 

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
    #
    def add_birthday(self, value):
        self.birthday = Birthday(value)
    
    def __str__(self):
        if self.birthday == None:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        else:
            birthday_str = self.birthday.value.strftime('%d.%m.%Y %A')
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {birthday_str}"

class AddressBook(UserDict):
    # def __init__(self):
    #     self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record
        print(f'Added new record: "{record}"')
        
    def find(self, value):
        for name, record in self.data.items():
            if name == value:
                return record
            else:
                print(f"Record for {value} wasn't found")

    def delete(self, name):
        try:
            key_for_delete = None
            for key in self.data.keys():
                if key == name:
                    key_for_delete = key
            self.data.pop(key_for_delete)
            print(f'{name}\'s contact was deleted')
        except(KeyError):
            print(f'{name}\'s contact wasn\'t found')
    
    def get_birthdays_per_week(self):
        users = []
        for name, record in self.data.items():
            if record.birthday != None:
                date_obj = record.birthday.value
                users.append({'name': name, 'birthday': datetime(int(date_obj.year), int(date_obj.month), int(date_obj.day))})
        return get_birthdays_per_week(users)



#Test
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# # Додавання запису John до адресної книги
book.add_record(john_record)
# # Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

alex1_record = Record("Aleg")
alex2_record = Record("Alex")
alex3_record = Record("Alexander")
book.add_record(alex1_record)
book.add_record(alex2_record)
book.add_record(alex3_record)
# # Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# # Знаходження та редагування телефону для John
john = book.find("John")
aleg = book.find("Aleg")
alex = book.find("Alex")
alexand = book.find("Alexander")
aleg.add_birthday('08.03.1978')
alex.add_birthday('10.03.1960')
alexand.add_birthday('08.07.1978')
john.edit_phone("1234567890", "1112223333")
john.add_birthday('23.08.1980')
print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# # Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# # Видалення запису Jane
#book.delete("Jane")
book.get_birthdays_per_week()