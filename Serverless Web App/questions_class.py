import datetime
import matplotlib.pyplot as plt
import numpy as np
import boto3
from botocore.exceptions import NoCredentialsError

class validate_questions:
    def __init__(self):
        self.email = ''
        self.question_list = []
        self.question_start_time = ""
        self.question_end_time = datetime.datetime.now()
        self.traits_scores = {"EXT":0,"AGG":0,"CON":0,"NEU":0,"OPN":0}


    #Setters
    def validate_question_values(self,questions_list):
        try:    
            i = 0
            while (i < 120):
                if ( questions_list[i] == '1' or questions_list[i] == '2' or questions_list[i] == '3' or questions_list[i] == '4' or questions_list[i] == '5' ):
                    i = i + 1
                else:
                    return ("Invalid Answer Value Range in the Questionarre.")
            self.question_list = questions_list
            

        except:
            print("Invalid answer variable type")
        
    
    def ipip_120_scores(self,q_list):
        for i in range(0, len(q_list)): 
            q_list[i] = int(q_list[i])
        
        print(q_list)
        print(type(q_list[i]))
        agg=0 
        con=0
        opn=0
        ext=0
        neu=0
        print("HERE")
        #MAX JUGAR
        for i in range(0, len(q_list)):

            #Neuroticism
            if( i == 0 or i== 5 or i == 10 or i == 15 or i == 20 or i == 25 or i == 30 or i == 35 or i == 40 or i == 45 or i == 50 or i == 55 or i == 60 or i == 65 or i == 70 or i == 75 or i == 80 or i == 85 or i == 90 or i == 95 or i == 100 or i == 105 or i == 110 or i == 115):
                neu = neu + 1
                #Negative Keyed
                if ( i == 50 or i == 80 or i == 95 or i == 100 or i == 105 or i == 110 or i == 115):
                    #Rerversing Scale for Negatively Keyed
                    q_list[i] = 6 - q_list[i]
                    self.traits_scores["NEU"] = self.traits_scores["NEU"] + q_list[i]
                #Positive Keyed
                else:
                    self.traits_scores["NEU"] = self.traits_scores["NEU"] + q_list[i]
            
            #EXTRAVERSION
            elif( i == 1 or i == 6 or i == 11 or i == 16 or i == 21 or i == 26 or i == 31 or i == 36 or i == 41 or i == 46 or i == 51 or i == 56 or i == 61 or i == 66 or i == 71 or i == 76 or i == 81 or i == 86 or i == 91 or i == 96 or i == 101 or i == 106 or i == 111 or i == 116):
                ext = ext + 1
                #Negative Keyed
                if( i == 61 or i == 66 or i == 91 or i == 96 or i == 101 or i == 106):
                    #Rerversing Scale for Negatively Keyed
                    q_list[i] = 6 - q_list[i]
                    self.traits_scores["EXT"] = self.traits_scores["EXT"] + q_list[i]
                #Positive Keyed
                else:
                    self.traits_scores["EXT"] = self.traits_scores["EXT"] + q_list[i]
            
            #Openness
            elif( i == 2 or i == 7 or i == 12 or  i == 17 or i == 22 or i == 27 or i == 32 or i == 37 or i == 42 or i == 47 or i == 52 or i == 57 or i == 62 or i == 67 or i == 72 or i == 77 or i == 82 or i == 87 or i == 92 or i == 97 or i == 102 or i == 107 or i == 112 or i == 117):
                opn = opn + 1
                #Negative Keyed
                if (i == 47 or i == 52 or i == 67 or i == 72 or i == 78 or i == 82 or i == 87 or i == 97 or i == 102 or i == 107 or i == 112 or i == 117):
                    #Rerversing Scale for Negatively Keyed
                    q_list[i] = 6 - q_list[i]
                    self.traits_scores["OPN"] = self.traits_scores["OPN"] + q_list[i]
                #Positive Keyed
                else:
                    self.traits_scores["OPN"] = self.traits_scores["OPN"] + q_list[i]
            
            #Aggreableness
            elif( i == 3 or i == 8 or i == 13 or i == 18 or i == 23 or i == 28 or i == 33 or i == 38 or i == 43 or i == 48 or i == 53 or i == 58 or i == 63 or i == 68 or i == 73 or i == 78 or i == 83 or i == 88 or i == 93 or i == 98 or i == 103 or i == 108 or i == 113 or i == 118):
                agg = agg + 1
                #Negative Keyed
                if (i == 8 or i == 18 or i == 23 or i == 38 or i == 48 or i == 53 or i == 68 or i == 73 or i == 78 or i == 83 or i == 88 or i == 93 or i == 98 or i == 103 or i == 109 or i == 113 or i== 118):
                    #Rerversing Scale for Negatively Keyed
                    q_list[i] = 6 - q_list[i]
                    self.traits_scores["AGG"] = self.traits_scores["AGG"] + q_list[i]
                #Positive Keyed
                else:
                    self.traits_scores["AGG"] = self.traits_scores["AGG"] + q_list[i]
            
            #Conscienciousness
            elif ( i == 4 or i == 9 or i == 14 or i == 19 or i ==24 or i == 29 or i == 34 or i == 39 or i == 44 or i == 49 or i == 54 or i == 59 or i == 64 or i == 69 or i == 74 or i == 79 or i == 84 or i == 89 or i == 94 or i == 99 or i == 104 or i == 109 or i == 114 or i == 119):
                con = con + 1
                #Negative Keyed
                if(i == 29 or i == 39 or i == 59 or i == 69 or i == 74 or i == 79 or i == 84 or i == 89 or i == 99 or i == 104 or i == 109 or i == 114 or i == 119):
                    #Rerversing Scale for Negatively Keyed
                    q_list[i] = 6 - q_list[i]
                    self.traits_scores["CON"] = self.traits_scores["CON"] + q_list[i]
                #Positive Keyed
                else:
                    self.traits_scores["CON"] = self.traits_scores["CON"] + q_list[i]
        
        print(self.traits_scores)
        print (con,agg,neu,ext,opn)

        #Calibrating Scores Accoring to 100th range
        self.traits_scores["CON"] = (self.traits_scores["CON"]/120) * 100
        self.traits_scores["EXT"] = (self.traits_scores["EXT"]/120) * 100
        self.traits_scores["AGG"] = (self.traits_scores["AGG"]/120) * 100
        self.traits_scores["NEU"] = (self.traits_scores["NEU"]/120) * 100
        self.traits_scores["OPN"] = (self.traits_scores["OPN"]/120) * 100
        print(self.traits_scores)

        
        #Graph Plot
        objects = ['OPN', 'AGG', 'CON', 'EXT', 'NEU']
        
        performance = [self.traits_scores["OPN"],self.traits_scores["AGG"],self.traits_scores["CON"],self.traits_scores["EXT"],self.traits_scores["NEU"]]
        y_pos = np.arange(len(objects))
        plt.bar(y_pos, performance, align='center', alpha=0.8)
        plt.xticks(y_pos, objects)
        plt.axis([-1, 5, 0, 100])
        for index, value in enumerate(performance):
            plt.text(value, index, str(value))
        plt.ylabel('Trait Score')
        plt.title('Big Five Model Score')
        score_file = "{email}.png".format(email = self.email)
        directory = "/tmp/"
        plt.savefig(directory+score_file)
        print(score_file)
        print(directory)

        s3 = boto3.client('s3',region_name='us-east-1',aws_access_key_id="Your Key",aws_secret_access_key="Your Key")
        bucket = 'Your Bucket'
        file_name = directory+score_file
        key_name = score_file
        s3.upload_file(file_name, bucket, key_name)



        






