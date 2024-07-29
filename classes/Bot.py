from AddressBook import *
from datetime import datetime, timedelta

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"
    return inner

@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args[0], args[1]
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    if len(args) < 3:
        raise ValueError("Give me name, old phone and new phone.")
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if record is not None:
        record.change_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError

@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is not None:
        return ", ".join(str(phone) for phone in record.phones)
    else:
        raise KeyError

@input_error
def show_all(book):
    if not book.data:
        return "No contacts found."
    result = ""
    for name, record in book.data.items():
        phones = ", ".join(str(phone) for phone in record.phones)
        result += f"{name}: {phones}\n"
    return result.strip()

@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError("Give me name and birthday in format DD.MM.YYYY.")
    name, birthday = args[0], args[1]
    record = book.find(name)
    if record is not None:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError

@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is not None and record.birthday is not None:
        return record.birthday.strftime("%d.%m.%Y")
    elif record is None:
        raise KeyError
    else:
        return "Birthday not set."

@input_error
def birthdays(args, book):
    today = datetime.now()
    next_week = today + timedelta(days=7)
    result = ""
    for name, record in book.data.items():
        if record.birthday is not None:
            bday = record.birthday.replace(year=today.year)
            if today <= bday <= next_week:
                result += f"{name}: {bday.strftime('%d.%m.%Y')}\n"
    if result:
        return result.strip()
    else:
        return "No birthdays in the next week."

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
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
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
