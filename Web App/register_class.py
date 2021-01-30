import re
import datetime
import uuid


class register_user:
    def __init__(self):
        self.name = ""
        self.age = 0
        self.email = ""
        self.gender = ""
        self.ip_addr =""
        self.country = ""
        self.birthday = ""
        self.register_date = datetime.datetime.today().strftime('%Y-%m-%d')
        self.password = ""
        self.user_id = str(uuid.uuid4())

    #Setters
    def set_name(self,name):
        try:    
            if  ( len(name) <= 30 and len(name) > 2):
                self.name = name
            else:
                return "Name must be under 30 alphabets and not empty."
        except:
            return "Value is invalid. Name must be a string"

    def set_age(self,age):
        try:
            self.age = int (age)
            if(self.age <= 0):
                del self.age
                return  "Enter valid age"
        except:
            return  "Invalid Age Type."
    

    def set_email(self,email):
        try:
            if (email):
                self.email = email
            else:  
                return "Empty email address field"
        except:
            return  "invalid Input Type for Email"   


    def set_birthday(self,year,month,day):
        date_format = '%Y-%m-%d'
        try:
            month=int(month)
            day=int(day)
            if(month >=1 and month <=9):
                month = '0'+str(month)
            if(int(day) >=1 and int(day) <=9):
                day = '0'+str(day)
            print('date')          
            birthday=str(year)+"-"+str(month)+"-"+str(day)
            print(birthday)
            print('date')
            datetime.datetime.strptime(birthday, date_format)
            self.birthday = birthday
        except:
            return  "B-Day should be DD-MM-YYYY.Example Format is '1-1-1990'"


    def set_ip_addr(self,ip_addr):
        self.ip_addr = ip_addr


    def set_gender(self,gender):
        try:
            if(gender == 'M' or gender == 'F' or gender == "other"):
                self.gender = gender
            else:
                return  "Wrong Gender Type"
        except:
            return  "Invalid value. Must be M,F or other"


    def set_password(self,password,cpassword):
        try:
            if(len(password) <= 5 ):
                return("Password Too Short.Must be greater than 6 or equal to alpha-numeric values")
            if(len(password) > 30):
                return("Password Too Long.Reduce length")
            if(password != cpassword):
                return("Password Donot match")
            self.password = password

        except:
            return  "Invalid password type, must be of string type"

    def calculate_age(self,birthday):
        try:    
            date_format = '%Y-%m-%d'
            today = datetime.date.today()
            objbirthday = datetime.datetime.strptime(birthday, date_format)
            self.age = today.year - objbirthday.year - ((today.month, today.day) < (objbirthday.month,objbirthday.day))
            if (self.age < 0):
                return "You Can't be from future!"
        except:
            pass