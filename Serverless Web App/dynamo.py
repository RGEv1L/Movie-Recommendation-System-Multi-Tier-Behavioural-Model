import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import botocore

class   dynamodb_FindMyMovies():
    def __init__(self):
        # Get the service resource.
        self.dynamodb = ''#boto3.resource('dynamodb',endpoint_url='http://localhost:8000')
        self.table = ''#dynamodb.Table('Your Table name')
        

    def check_state(self):
        try:
            self.dynamodb= boto3.resource('dynamodb',region_name='us-east-1',aws_access_key_id="Enter Your Key",aws_secret_access_key="Enter Your Key")
            self.table= self.dynamodb.Table('Your Table')
            print(self.table.creation_date_time)
            return 0
        
        except botocore.exceptions.ParamValidationError as e:
            print(e)
        except:
            print("Couldn't connect with Database or Table")
            return 1
        


    def read_login_creds(self,data):
        try:
            #Putting login credentials
            state = self.check_state()
            if( state == 0):
                response = self.table.get_item(Key={
                    'email' : data['email'],
                    'r_type': 'login'
                })
                
                check = response["Item"]

                if ( data['password'] == response['Item']['password']): #check if password matches
                    return 0
                else:
                    return "Email or Password Didn't Matched"
                    

        except ClientError as e:
            return e.response['Error']['Message']
        
        except:
            return "Email Doesn't Exits"
            
        


    def write_signup_data(self, data):
        try:
            #Putting login credentials
            state = self.check_state()
            response = ''
            if( state == 0):


                response = self.table.put_item(
                Item={
                'email': data['email'],
                'r_type': 'login',
                'password': data['password']
                },
                ConditionExpression='attribute_not_exists(email)'
                    )
                
            #Putting User metadata
            state = self.check_state()
            if (state == 0):
                response = self.table.put_item(
                Item={
                'email': data['email'],
                'r_type': 'metadata',
                'full_name': data['name'],
                'gender' : data['gender'],
                'age' : data['age'],
                'userID' : data['userID'],
                'register_date' : data['register_date'],
                'ip_addr' : data['IP'],
                'country' : data['country'],
                'birthdate' : data['birthdate']
                    }
                )
            return 0
            
        except ClientError as e:
            if e.response['Error']['Message'] == 'The conditional request failed':
                return 'Email Already Exists'
        except:
            return "Signup procedure error"

            
            
        



    def write_questions_data(self, data,li):
        try:
            #Putting login credentials
            state = self.check_state()
            if( state == 0):
                response = self.table.put_item(
                Item={
                'email': data['email'],
                'r_type': 'ipip120_response',
                'EXT':data['ipip_answers'][0],
                'AGG':data['ipip_answers'][1],
                'CON':data['ipip_answers'][2],
                'NEU':data['ipip_answers'][3],
                'OPN':data['ipip_answers'][4]
                    }
                )

                response = self.table.put_item(
                Item={
                'email': data['email'],
                'r_type': 'ipip120_plain',
                'q1':li[0],
                'q2':li[1],
                'q3':li[2],
                'q4':li[3],
                'q5':li[4],
                'q6':li[5],
                'q7':li[6],
                'q8':li[7],
                'q9':li[8],
                'q10':li[9],
                'q11':li[10],
                'q12':li[11],
                'q13':li[12],
                'q14':li[13],
                'q15':li[14],
                'q16':li[15],
                'q17':li[16],
                'q18':li[17],
                'q19':li[18],
                'q20':li[19],
                'q21':li[20],
                'q22':li[21],
                'q23':li[22],
                'q24':li[23],
                'q25':li[24],
                'q26':li[25],
                'q27':li[26],
                'q28':li[27],
                'q29':li[28],
                'q30':li[29],
                'q31':li[30],
                'q32':li[31],
                'q33':li[32],
                'q34':li[33],
                'q35':li[34],
                'q36':li[35],
                'q37':li[36],
                'q38':li[37],
                'q39':li[38],
                'q40':li[39],
                'q41':li[40],
                'q42':li[41],
                'q43':li[42],
                'q44':li[43],
                'q45':li[44],
                'q46':li[45],
                'q47':li[46],
                'q48':li[47],
                'q49':li[48],
                'q50':li[49],
                'q51':li[50],
                'q52':li[51],
                'q53':li[52],
                'q54':li[53],
                'q55':li[54],
                'q56':li[55],
                'q57':li[56],
                'q58':li[57],
                'q59':li[58],
                'q60':li[59],
                'q61':li[60],
                'q62':li[61],
                'q63':li[62],
                'q64':li[63],
                'q65':li[64],
                'q66':li[65],
                'q67':li[66],
                'q68':li[67],
                'q69':li[68],
                'q70':li[69],
                'q71':li[70],
                'q72':li[71],
                'q73':li[72],
                'q74':li[73],
                'q75':li[74],
                'q76':li[75],
                'q77':li[76],
                'q78':li[77],
                'q79':li[78],
                'q80':li[79],
                'q81':li[80],
                'q82':li[81],
                'q83':li[82],
                'q84':li[83],
                'q85':li[84],
                'q86':li[85],
                'q87':li[86],
                'q88':li[87],
                'q89':li[88],
                'q90':li[89],
                'q91':li[90],
                'q92':li[91],
                'q93':li[92],
                'q94':li[93],
                'q95':li[94],
                'q96':li[95],
                'q97':li[96],
                'q98':li[97],
                'q99':li[98],
                'q100':li[99],
                'q101':li[100],
                'q102':li[101],
                'q103':li[102],
                'q104':li[103],
                'q105':li[104],
                'q106':li[105],
                'q107':li[106],
                'q108':li[107],
                'q109':li[108],
                'q110':li[109],
                'q111':li[110],
                'q112':li[111],
                'q113':li[112],
                'q114':li[113],
                'q115':li[114],
                'q116':li[115],
                'q117':li[116],
                'q118':li[117],
                'q119':li[118],
                'q120':li[119]

                    }
                )
            
            return 0
            
        except ClientError as e:
            return e.response['Error']['Message']
        




    def write_movie_rating_response(self,data):
        try:
            #Putting login credentials
            print(data)
            state = self.check_state()
            if( state == 0):
                response = self.table.put_item(
                Item={
                'email': data['email'],
                'r_type': data['r_type'],
                'titleID':data['titleID'],
                'rating' : data['rating']
                    }
                )
                print(response)
            return 0
            
        except ClientError as e:
            print(e.response['Error']['Message'])
            return 1
        
    def read_recs(self,email):
        try:
            #Putting login credentials
            state = self.check_state()
            if( state == 0):
                response = self.table.get_item(Key={
                    'email' : email,
                    'r_type': 'rec'
                })
                
                check = response["Item"]

                return response["Item"]['r0'],response["Item"]['r1'],response["Item"]['r2'],response["Item"]['r3'],response["Item"]['r4'],response["Item"]['r5'],response["Item"]['r6'],response["Item"]['r7'],response["Item"]['r8'],response["Item"]['r9']
                    

        except ClientError as e:
            return e.response['Error']['Message']
        
        except:
            return "Email Doesn't Exits"
            


