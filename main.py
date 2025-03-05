from book import AddressBook, Record

welcome ="""
╦ ╦╔═╗╦  ╔═╗╔═╗╔╦╗╔═╗
║║║║╣ ║  ║  ║ ║║║║║╣ 
╚╩╝╚═╝╩═╝╚═╝╚═╝╩ ╩╚═╝"""
comands = """
КОМАНДИ:
add [ім'я] [телефон]: Додати або новий контакт з іменем та телефонним номером, або телефонний номер до контакту який вже існує.
change [ім'я] [старий телефон] [новий телефон]: Змінити телефонний номер для вказаного контакту.
phone [ім'я]: Показати телефонні номери для вказаного контакту.
all: Показати всі контакти в адресній книзі.
add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту.
show-birthday [ім'я]: Показати дату народження для вказаного контакту.
birthdays: Показати дні народження на найближчі 7 днів з датами, коли їх треба привітати.
hello: Отримати вітання від бота.
close або exit: Закрити програму."""
goodbye = """
  ______  _____   _____  _____   ______  _     _ _______ 
 / _____)/ ___ \ / ___ \(____ \ (____  \| |   | (_______)
| /  ___| |   | | |   | |_   \ \ ____)  ) |___| |_____   
| | (___) |   | | |   | | |   | |  __  ( \_____/|  ___)  
| \____/| |___| | |___| | |__/ /| |__)  )  ___  | |_____ 
 \_____/ \_____/ \_____/|_____/ |______/  (___) |_______)
                                                         
"""
# ДЕКОРАТОРИ ДЛЯ ОБРОБКИ ПОМИЛОК:
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command"
        except IndexError:
            return "Enter the argument for the command"
        except KeyError:
            return "Enter the argument for the command"
        except UnboundLocalError:
            return "Enter the argument for the command"
    return inner

@input_error
def parse_input(user_input):         #парсер команд
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook): #ф-ія додати контакт
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def add_birthday(args, book):       #ф-ія додати дату народження
    name, birthday_date, *_ = args
    record = book.find(name)
    message = "Contact not in book"
    if record is not None:
        record.add_birthday(birthday_date)
        message = "birthday added."
    return message


@input_error
def show_birthday(args,book):      #ф-ія перегляду дня народження окремого юзера
    name, *_ = args
    record = book.find(name)
    if record is not None:
        message = f"birthday {record.birthday}"
    return message


@input_error
def birthdays(book):            #ф-ія перегляду днів народження у найближчі 7 днів
    return book.get_upcoming_birthdays()


@input_error
def change_number(args,book): # функція зміни контакту 
    name, old_p, new_p , *_ = args
    record = book.find(name)
    if record is not None:
        record.edit_phone(old_p, new_p)
        message = "phone changed."
    return message
    

@input_error   
def view_number(args,book): # функція перегляду номеру телефону конкретного користувача
    name, *_ = args
    return  ", ".join(n.value for n in book.data[name].phones)


@input_error
def view_all_contacts(x):     #виводимо контакти
    return x


def main():     # основна функція циклу
    print(welcome)  #виведення привітання
    print(comands)   # виведення команд
    book = AddressBook()
    while True:
        user_input = input("Enter a command: ")    #ввід команди користувачем
        command, *args = parse_input(user_input)   #запускаємо парсер команд
        if command in ["close", "exit", "quit"]:  #вихід з програми
            print(goodbye)                        #вивід гудбай
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":                  #команда додати новий контакт
            print(add_contact(args, book))   
        elif command == "change":
            print(change_number(args, book))    #команда змінити номер телефону
        elif command == "phone":
            print(view_number(args,book))   #команда перегляд номеру телефону окремого юзера
        elif command == 'all':                  
            print(view_all_contacts(book))      #команда перегляду всіх контактів
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":        #команда перегляду дня народжєння окремого юзера
            print(show_birthday(args,book))
        elif command == "birthdays":            #команда перегляду днів народження у найближчі 7 днів
            print(birthdays(book))
        else: 
            print ("Enter the argument for the command")


if __name__ == "__main__":
    main()