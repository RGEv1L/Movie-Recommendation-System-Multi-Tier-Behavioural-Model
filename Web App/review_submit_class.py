import datetime


class user_review_submit:
    def __init__(self):
        self.titleID = ''
        self.rating = 0
        self.submit_date = str(datetime.datetime.today())


    #Setters
    def set_titleID(self,title_ID):
        try:
            if (title_ID == ''):
                return "Title ID is empty"
            else:
                self.titleID = title_ID
        except:
            return 'Invalid format for title ID'



    #Setters
    def set_rating(self,rating_user):
        try:
            rating_user = int(rating_user)
            if (rating_user >= 0 and rating_user <= 10):
                self.rating = rating_user
            else:
                return "Invalid Range. Should be between 0-10"
        except:
            return 'Invalid format for Rating.'