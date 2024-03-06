from collections import UserDict

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
        super().__init__(value)
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise ValueError('Phone should be 10 digits format')

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    
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
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    # def __init__(self):
    #     self.data = {}

    def add_record(self, record):
        self.data[record.name] = record
        print(f'Added new record: "{record}"')
        
    def find(self, value):
        for name, record in self.data.items():
            if name.value == value:
                return record
            else:
                print(f"Record for {value} wasn't found")

    def delete(self, name):
        try:
            key_for_delete = None
            for key in self.data.keys():
                if key.value == name:
                    key_for_delete = key
            self.data.pop(key_for_delete)
            print(f'{name}\'s contact was deleted')
        except(KeyError):
            print(f'{name}\'s contact wasn\'t found')


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
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        return "Sorry, " + {name} + " isn't exist."

@input_error
def show_phone(args, contacts):
    name = args
    if name in contacts:
        phone = contacts[name]
        return "{name}: {phone}"
    else:
        return "Sorry, {name} isn't exist. Use 'add' for append this contact."
    
def show_all(contacts):
    res = []
    res.append("{:^20}".format("CONTACTS"))
    res.append("{:^20}".format("-"*10))
    for name, phone in contacts.items():
        res.append("{:<8} {} ".format(name+":", phone))
    res.append("{:^20}".format("="*20))
    return "\n".join(res)

def show_commands():
    commands = {
        "help": "for help",
        "hello": "just fo say 'Hi!'",
        "add name phone": "for add new contact",
        "change name phone": "for change exist contact",
        "phone name": "for get phone number",
        "all": "for get all contact list",
        "exit": "for exit",
    }
    res = []
    for command, desctiption in commands.items():
        res.append("{:<19} {} ".format(command, desctiption))
    return "\n".join(res)

def main():
    contacts = {}
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
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
            # print("{:^20}".format("CONTACTS"))
            # for name, phone in contacts.items():
            #     print("{:<8} {} ".format(name+":", phone))
            # print("{:>20} ".format("Done"))
        else:
            print("Invalid command. Enter \"help\" for help")

if __name__ == "__main__":
    main()

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

# # Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# # Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# # Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# # Видалення запису Jane
book.delete("Jane")