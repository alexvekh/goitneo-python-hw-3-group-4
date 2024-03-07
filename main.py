#from collections import UserDict
from classes import Field, Name, Phone, Record, AddressBook

# class Field:
#     def __init__(self, value):
#         self.value = value

#     def __str__(self):
#         return str(self.value)

# class Name(Field):
#     def __init__(self, value):
#         if len(value) > 0 and value[0].isalpha():
#             self.value = value.title()
#         else:
#             raise ValueError('Name should starts with letter')

# class Phone(Field):
#     def __init__(self, value):
#         super().__init__(value)
#         if len(value) == 10 and value.isdigit():
#             self.value = value
#         else:
#             raise ValueError('Phone should be 10 digits format')

# class Record:
#     def __init__(self, name):
#         self.name = Name(name)
#         self.phones = []
    
#     def add_phone(self, value):
#         self.phones.append(Phone(value))

#     def remove_phone(self, phone):
#         self.phones.remove(phone)

#     def edit_phone(self, phone, new_phone):
#         found = False
#         for p in self.phones:
#             if p.value == phone:
#                 p.value = new_phone
#                 print(f"Phone {phone} was changed to {new_phone}.")
#                 found = True
#         if not found:
#             print(f'Phone {phone} wasn\'t found') 

#     def find_phone(self, phone):
#         for p in self.phones:
#             if p.value == phone:
#                 return p.value
    
#     def __str__(self):
#         return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

# class AddressBook(UserDict):
#     # def __init__(self):
#     #     self.data = {}

#     def add_record(self, record):
#         self.data[record.name] = record
#         print(f'Added new record: "{record}"')
        
#     def find(self, value):
#         for name, record in self.data.items():
#             if name.value == value:
#                 return record
#             else:
#                 print(f"Record for {value} wasn't found")

#     def delete(self, name):
#         try:
#             key_for_delete = None
#             for key in self.data.keys():
#                 if key.value == name:
#                     key_for_delete = key
#             self.data.pop(key_for_delete)
#             print(f'{name}\'s contact was deleted')
#         except(KeyError):
#             print(f'{name}\'s contact wasn\'t found')


# Decorator
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me a name and phone please."
        except KeyError:
            return "Give me a name please."
        except IndexError:
            return "Enter user name, please"
    
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
  #  print("book", book)
  #  print("record", record)
    return "Contact added."

@input_error
def change_contact(args, book):
    name, phone = args
    if name in book:
        record = book[name]
        record.phones = []
        record.add_phone(phone)
        return "Contact updated."
    else:
        return "Sorry, " + name + " isn't exist."

@input_error
def show_phone(args, book):
    name, = args
    if name in book:
        record = book[name]
        # Out         print(record)
        res = []
        for phone in record.phones:
            res.append(phone.value)
        return f"{name}: {','.join(res)}"
    else:
        return "Sorry, {name} isn't exist. Use 'add' for append this contact."
    
def show_all(book):
    res = []
    res.append("{:^20}".format("CONTACTS"))
    res.append("{:^20}".format("-"*10))
    for name, phone in book.items():
        res.append("{:<8} {} ".format(name+":", phone))
    res.append("{:^20}".format("="*20))
    return "\n".join(res)

@input_error
def add_birthday(args, book):
    name = args
    if name in book:
        phone = book[name]
        return f"{name}: {phone}"
    else:
        return f"Sorry, {name} isn't exist. Use 'add' for append this contact."

def show_commands():
    commands = {
        "help": "for help",
        "hello": "just fo say 'Hi!'",
        "add name phone": "for add new contact",
        "change name phone": "for change exist contact",
        "phone name": "for get phone number",
        "add-birthday name": "for add birthday",
        "show_birthday name": "for get birthday",
        "birthdays": "for get birtdays next week ",
        "all": "for get all contact list",
        "exit": "for exit",
    }
    res = []
    for command, desctiption in commands.items():
        res.append("{:<19} {} ".format(command, desctiption))
    return "\n".join(res)

def main():
    
    book = AddressBook()
    book = book
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "good bye"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
        elif command == "help":
            print(show_commands())
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(berthdays(book))
        else:
            print("Invalid command. Enter \"help\" for help")

if __name__ == "__main__":
    main()

#Test
#book = AddressBook()

# Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")

# # # Додавання запису John до адресної книги
# book.add_record(john_record)
# # # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)

# # # Виведення всіх записів у книзі
# for name, record in book.data.items():
#     print(record)

# # # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")

# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# # # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# # # Видалення запису Jane
# book.delete("Jane")