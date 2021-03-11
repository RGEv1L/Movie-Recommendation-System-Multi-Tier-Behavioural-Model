import datetime

class login_user:
    def __init__(self):
        self.email = ""
        self.password = ""
        self.last_login = datetime.datetime.now()
        self.JWT=""

    #Setters
    def set_email(self,email):
        try:
            if (email):
                self.email = email
            else:  
                    return  "Empty email address"
        except:
            return  "invalid Input Type for Email"  


    def set_password(self,password):
        try:
            if(len(password) <= 5 ):
                return"Password Too Short.Must be greater than 6 alpha-numeric values"
            if(len(password) > 20):
                return("Password Too Long.Reduce length")
            self.password = password
        except:
            return  "Invalid password type, must be of string type"

