import jwt


class token_mecha:
    def __init__(self):
        self.token = ''
        self.secret = "\xa7\xee\xd3^,@\x88\n~\xd3\xa1\x7f\x95Cu\xd6"
    
    def encode_token(self,arg1,arg2):
        self.token = jwt.encode({'email':arg1,'ip':arg2},self.secret,algorithm='HS256')

    def decode_token(self):
        return jwt.decode(self.token,self.secret,'HS256')

    
    def check_state(self):
        if not self.token:
            print("No Token")
            return 1
        try:
            self.decode_token()
            return 0
        except jwt.InvalidTokenError:
            print ("invalid token")
            return 2
        except:
            return 2
        
    def jwt_fetch_email(self):
        token = self.decode_token()
        return token['email']
