from collections import UserDict
from datetime import datetime, timedelta, date


class Field:
    def __init__(self, value):
        self.value = value


    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, value):
        self.value = value
        if not self.value.isdigit() or len(self.value) != 10: #перевірка номеру
            raise ValueError("Wrong phone number format")
        

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = value
            datetime.strptime(value,"%d.%m.%Y").date() # та перетворіть рядок на об'єкт datetime                                                        
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") # Додайте перевірку коректності даних
        
    def __str__(self):
        return f"{self.value}" # f"{self.value.strptime("%d.%m.%Y")}"  # відображення дати для команди show-birthday
        
    def __repr__(self):
        return datetime.strptime(self.value,"%d.%m.%Y").date()


class Record:
    def __init__(self, name):
        self.name = Name(name)       # дата дня народження за замовчуванням None
        self.phones = []              # список номерів телефону 
        self.birthday = None         # дата дня народження за замовчуванням None 

    def add_birthday(self, value):
        self.birthday = Birthday(value)            # функція додавання дня народження
        return self.birthday


    def add_phone(self,phone_number:str) -> Phone:   
        self.phones.append(Phone(phone_number))    # ф-ія додавання нового номеру, номер додається у форматі класу Phone
        return self.phones                         # ф-ія повертає список телефонів


    def remove_phone (self, phone_number):
        self.phones=list(filter(lambda x: x.value != phone_number, self.phones))     # видалення номеру телефону зі списку
        return self.phones
    

    def edit_phone (self, old, new):                          # ф-ія редагування номеру телефону
            flag = any(x.value == old for x in self.phones)     # пошук даного телефону у списку телефонів користувача
            if flag:
                self.add_phone(new)      #виклик ф-ії додавання нового номеру телефону
                self.remove_phone(old)       #виклик ф-ії видалення старого номеру телефону
            else:
                raise ValueError("Номеру не існує")
 

    def find_phone(self,phone_number):
        if any(x.value == phone_number for x in self.phones):   # пошук даного телефону у списку телефонів користувача
            find_phone = list(filter(lambda x: x.value == phone_number, self.phones))     # видалення номеру телефону зі списку
            return find_phone[0] # повернення даного номеру телефону
        else:
            return None # у разі відсутності номеру у списку повертаємо None 
        

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record_name:Record):
        self.name = record_name.name.value #і'мя у форматі класу Record
        self.data[self.name] = record_name #номери телефонів у форматі класу Record
        return self.data


    def find(self,name:str) -> Record:  #ф-ія пошуку контакту за іменем
        return self.data.get(name)
    

    def delete(self,name_delete:str):   #ф-ія видалення контакту за іменем
        self.data.pop(self.find(name_delete).name.value)
        return self.data
    
    def find_next_weekday(self,start_date, weekday):   #ф-ія пошуку дати привітання з днем народження
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)


    def adjust_for_weekend(self, birthday):        #ф-ія пошуку дати привітання з днем народження
        if birthday.weekday() >= 5:
            return self.find_next_weekday(birthday, 0)  
        return birthday


    def get_upcoming_birthdays(self, days=7):     #ф-ія пошуку всіх дат привітання з днем народження
        upcoming_birthdays = []                   #ф-ія пошуку всіх дат привітання з днем народження
        today = date.today()
        for user in self.data:
            if self.data[user].birthday:         #перевірка істинності існування запису у полі "birthday"
                day = self.data[user].birthday.value
                bday = datetime.strptime(day,"%d.%m.%Y").date() # перетворюємо рядок у значення datetime
                birthday_this_year = bday.replace(year=today.year)    #якщо поле існує => призначаємо значення змінній "birthday_this_year" та змінюємо рік на теперішній
            else:
                continue
            if birthday_this_year < today:                                                       # якщо день народження вже минув
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)          # додаємо +1 рік, щоб привітати у наступному році
                if 0 <= (birthday_this_year - today).days <= days:                            #умова потрапляння дати привітання у список
                    congratulation_date_str = self.adjust_for_weekend(birthday_this_year)     #вираховуємо день привітання, якщо потрапляє на вихідний
                    upcoming_birthdays.append({"name": self.data[user].name.value, "birthday": congratulation_date_str.strftime("%d.%m.%Y")})#додаємо дату у список привітань
            else:
                if 0 <= (birthday_this_year - today).days <= days:           #умова потрапляння дати привітання у список
                    congratulation_date_str = self.adjust_for_weekend(birthday_this_year)       #вираховуємо день привітання, якщо потрапляє на вихідний
                    upcoming_birthdays.append({"name": self.data[user].name.value, "birthday": congratulation_date_str.strftime("%d.%m.%Y")}) #додаємо дату у список привітань
        return upcoming_birthdays #список привітань


    def __repr__(self):  #відображення об'єктів класу "AdressBook"
        u=[]
        for key in self.data:
            if self.data[key].birthday: 
                b= self.data[key].birthday.value #значення дати дня народження у форматі "день.місяць.рік"
            else:
                b= self.data[key].birthday
            y = self.data[key].name.value     #значення імені
            z = self.data[key].phones         #список телефонів для цього імені
            u.append(f"Name:{y}; tel.: {", ".join(n.value for n in z)}; birthday: {b}")  #додаємо ім'я та номер телефону у список для відображення
        return f"_______________Книга контактів______________\n{"\n".join(k for k in u)}"  #додаємо \n для кращого відображенн
       
        
# book = AddressBook()
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
# john_record.add_phone("5555558555")
# john_record.add_phone("1555555555")
# #john_record.add_birthday("07.03.1000")
# book.add_record(john_record)
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# jane_record.add_phone("1176543211")
# # #jane_record.remove_phone("9876543210")
# # jane_record.edit_phone("1176543211","1234567890")
# jane_record.add_birthday("11.11.1998")
# book.add_record(jane_record)
# # # # john = book.find("John")
# # # # # john1 = book.find("Jane")
# # # # # john1.add_phone("1176543211")
# # # # # john1.edit_phone("1176543211","0987654321")
# # # # # john.edit_phone("1234567890","1112223333")
# # # # # found_phone = john.find_phone("5555555555")
# # # # # print(f"{john.name}: {found_phone}")  #Виведення: John: 5555555555
# Ivan_record = Record("Ivan")
# Ivan_record.add_phone("1907328922")
# #Ivan_record.add_birthday("08.03.1998")
# book.add_record(Ivan_record)
# Igor_record = Record("Igor")
# Igor_record.add_phone("1907328922")
# Igor_record.add_birthday("08.03.1998")
# book.add_record(Igor_record)
# I_record = Record("I")
# I_record.add_phone("2207328422")
# I_record.add_phone("1907428922")
# I_record.add_phone("1907328912")
# I_record.add_phone("1907328922")
# I_record.add_birthday("10.03.1998")
# book.add_record(I_record)
# # # # # # book.delete("Ivan")
# # # # # #Ivan_record.edit_phone("1907328922", "0987654321")

# print(book)
# print(book.get_upcoming_birthdays())
# # print(john_record.birthday)
# # print(jane_record.birthday)
# # print(Ivan_record.birthday)
# # print(Igor_record.birthday)

# # z=book.data["I"].phones
# # print (f"{", ".join(n.value for n in z)}")





