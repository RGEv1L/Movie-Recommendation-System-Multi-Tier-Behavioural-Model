from flask import Flask, request, url_for, redirect, make_response, jsonify, render_template
import jinja2
import boto3
import json
import login_class
import questions_class, register_class, review_submit_class, jwt_mecha, dynamo
import jwt
from botocore.errorfactory import ClientError
import tmdbsimple as tmdb
tmdb.API_KEY = 'Your APi Key'

# FLASK WEB SERVER
app = Flask(__name__,static_url_path='',static_folder='static',template_folder='template')
app.config["SESSION_COOKIE_PATH"] = '/'




@app.route('/', methods=['GET'])
def home():
    # JWT Check Token
    current_user_jwt = jwt_mecha.token_mecha()
    current_user_jwt.token = request.cookies.get('JWT')
    err = current_user_jwt.check_state()

    if (err == 1):# No Token View
        return  render_template('index.html')
    elif  (err == 2):#Invalid Token View
        return  redirect(url_for('logout'), code=302)
    else:#Valid Token View
        return  render_template('index_log.html')
    
    return "200"



    
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        # JWT Check Token
        current_user_jwt = jwt_mecha.token_mecha()
        current_user_jwt.token = request.cookies.get('JWT')
        err = current_user_jwt.check_state()


        if (err == 1):# No Token View
            return  render_template('signup.html',error_log={})
        elif  (err == 2):#Invalid Token View
            return  redirect(url_for('logout'), code=302)
        else:#Valid Token View
            return  render_template('index_log.html',)


    if request.method == 'POST':
        current_user_reg = register_class.register_user()
        error_log={}
        signup_data = {}

        # Adding data to class for validation
        current_user_reg.country = request.form['country']

        err1 = current_user_reg.set_name(request.form['f_name'])
        if (err1):
            error_log['name']= err1
        else:
            signup_data['name'] = current_user_reg.name

        err2 = current_user_reg.set_gender(request.form['gender'])
        if (err2):
            error_log['gender']= err2
        else:
            signup_data['gender'] = current_user_reg.gender

        err3 = current_user_reg.set_email(request.form['email'])
        if (err3):
            error_log['email']= err3
        else:
            signup_data['email'] = current_user_reg.email

        #TWEAK FOR BIRTHDATE
        err4 = current_user_reg.set_birthday(request.form['birthday-year'],request.form['birthday-month'],request.form['birthday-day'])
        if (err4):
            error_log['birthday']= err4
        else:
            signup_data['birthdate'] = current_user_reg.birthday

        err5 = current_user_reg.set_password(request.form['password'], request.form['c_password'])
        if (err5):
            error_log['password']= err5
        else:
            signup_data['password'] = current_user_reg.password

        err6 = current_user_reg.calculate_age(current_user_reg.birthday)
        if  (err6):
            error_log['age']= err6
        else:
            signup_data['age'] = int(current_user_reg.age)

        signup_data['userID'] = current_user_reg.user_id
        signup_data['register_date'] = current_user_reg.register_date
        signup_data['country'] = current_user_reg.country
        signup_data['IP'] = request.remote_addr
        # Pushing data to DynamoDB
        write_signup = dynamo.dynamodb_FindMyMovies()
        state = write_signup.write_signup_data(signup_data)
        print(error_log)
        print(state)
        if (state):
            error_log['dynamodb']= state
            return render_template('signup.html',error_log=error_log) 

        return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        
        # JWT Check Token
        current_user_jwt = jwt_mecha.token_mecha()
        current_user_jwt.token = request.cookies.get('JWT')
        err = current_user_jwt.check_state()

        if (err == 1):# No Token View
            return  render_template('login.html',error_log={})
        elif  (err == 2):#Invalid Token View
            return  redirect(url_for('logout'), code=302)
        else:#Valid Token View
            return  render_template('index_log.html')


    if request.method == 'POST':
        current_user_login = login_class.login_user()
        error_log= {}
        login_data = {}

        # Adding data to class for validation
        # Form Data Extraction
        err1 = current_user_login.set_email(request.form['email'])
        if (err1):
            error_log['email']= err1
        else:
            login_data['email'] = current_user_login.email

        err2 = current_user_login.set_password(request.form['password'])
        if (err2):
            error_log['password']= err2
        else:
            login_data['password'] = current_user_login.password

        check_creds = dynamo.dynamodb_FindMyMovies()
        state = check_creds.read_login_creds(login_data)
        if (state):
            error_log['dynamodb']= state
            return render_template('login.html',error_log=error_log)

        
        
        # Passing Client IP
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr

        # JWT Create Token
        current_user_jwt = jwt_mecha.token_mecha()
        current_user_jwt.encode_token(current_user_login.email, ip)

        # Setting Cookies
        response = make_response(redirect(url_for("home")))
        response.set_cookie('js', "1",samesite='Lax')
        response.set_cookie('JWT', current_user_jwt.token,samesite='Lax')
        

        return response


@app.route('/movies', methods=['GET','POST'])
def movies():
    if request.method == 'GET':
        # JWT Check Token
        current_user_jwt = jwt_mecha.token_mecha()
        current_user_jwt.token = request.cookies.get('JWT')
        err = current_user_jwt.check_state()

        if (err == 1):# No Token View
            return  render_template('login.html',error_log={})
        elif  (err == 2):#Invalid Token View
            return  redirect(url_for('logout'), code=302)
        else:#Valid Token V iew
            return  render_template('main_movie.html')


    if request.method == 'POST':
        # JWT Check Token
        current_user_jwt = jwt_mecha.token_mecha()
        user_email = ''
        current_user_jwt.token = request.cookies.get('JWT')
        err = current_user_jwt.check_state()
        if (err):
            return redirect(url_for('logout'), code=302)

        user_email = current_user_jwt.jwt_fetch_email()  # fetching user email from JWT

        # Form Data Extraction
        print(request.values)
        current_user_review = review_submit_class.user_review_submit()
        err = ''
        review_data = {}

        err = current_user_review.set_titleID(request.values['titleID'])
        if (err):
            return err
        else:
            review_data['titleID'] = current_user_review.titleID

        err = current_user_review.set_rating(request.values['rating'])
        if (err):
            return err
        else:
            review_data['rating'] = current_user_review.rating

        review_data['email'] = user_email
        review_data['r_type'] = current_user_review.submit_date

        # Pushing data to DynamoDB
        write_review = dynamo.dynamodb_FindMyMovies()
        state = write_review.write_movie_rating_response(review_data)
        if (state):
            return str(state)

        return "200"


@app.route('/logout')
def logout():
    response = make_response(render_template('logout.html'))
    response.set_cookie('js', '0')
    response.set_cookie('JWT', '')
    return response


@app.route('/questions', methods=['POST', 'GET'])
def questions():
    if request.method == 'GET':
        # JWT Check Token
        current_user_jwt = jwt_mecha.token_mecha()
        current_user_jwt.token = request.cookies.get('JWT')
        err = current_user_jwt.check_state()

	#GEnerating Signed URL from S3
        if (err == 1):# No Token View
            return  render_template('login.html',error_log={})
        elif  (err == 2):#Invalid Token View
            return  redirect(url_for('logout'), code=302)
        else:#Valid Token View
            email = current_user_jwt.jwt_fetch_email()
            bucket='findmymovies-prod'
            object_name=str(email)+'.png'
            print("here")
            #Check if Obj Exist
            s3 = boto3.client('s3',region_name='us-east-1',aws_access_key_id="Your key for Signed URL",aws_secret_access_key="Your key for Signed URL")
            try:
                s3.head_object(Bucket=bucket, Key=object_name)
                response = s3.generate_presigned_url('get_object',
                                            Params={'Bucket': bucket,
                                                    'Key': object_name},
                                            ExpiresIn=2500)
                print("here")
                return  render_template('personality.html',image=response)
            except ClientError:
                return render_template('questions.html',error_log={})


           
            #return  render_template('questions.html',error_log={})


    if request.method == 'POST':
        current_user_questions = questions_class.validate_questions()
        error_log= {}
        # JWT Check Token
        current_user_jwt = jwt_mecha.token_mecha()
        current_user_jwt.token = request.cookies.get('JWT')
        err = current_user_jwt.check_state()
        if (err):
            return redirect(url_for('logout'), code=302)

        current_user_questions.email = current_user_jwt.jwt_fetch_email()
        questions_data = {}

        # Form Data Extraction
        li = []
        for i in range(0, 120):
            string_form = 'q' + str(i + 1)
            li.append(request.form[string_form])

        err = current_user_questions.validate_question_values(li)
        if (err):
            error_log['questions']= err

        current_user_questions.ipip_120_scores(li)

        # Converting Trait_scores dictionary into List of integers
        trait_scores = []
        trait_scores.append(int(current_user_questions.traits_scores['EXT']))
        trait_scores.append(int(current_user_questions.traits_scores['AGG']))
        trait_scores.append(int(current_user_questions.traits_scores['CON']))
        trait_scores.append(int(current_user_questions.traits_scores['NEU']))
        trait_scores.append(int(current_user_questions.traits_scores['OPN']))

        # Dynamodb push data

        questions_data['ipip_answers'] = trait_scores
        questions_data['email'] = current_user_questions.email

        write_questions = dynamo.dynamodb_FindMyMovies()

        state = write_questions.write_questions_data(questions_data,li)
        if (state):
            error_log['dynamodb']= state
            return render_template('questions.html',error_log=error_log)

        response = make_response(redirect(url_for('movies')))
        return response


@app.route('/rec', methods=['GET'])
def rec():
    if request.method == 'GET':
        # JWT Check Token
        current_user_jwt = jwt_mecha.token_mecha()
        current_user_jwt.token = request.cookies.get('JWT')
        err = current_user_jwt.check_state()


        if (err == 1):# No Token View
            return  render_template('login.html',error_log={})
        elif  (err == 2):#Invalid Token View
            return  redirect(url_for('logout'), code=302)
        #else:#Valid Token V iew
        #    return  render_template('main_movie.html')

        check_creds = dynamo.dynamodb_FindMyMovies()   
        email = current_user_jwt.jwt_fetch_email()
        a,b,c,d,e,f,g,h,i,j = check_creds.read_recs(email)
        pos='https://image.tmdb.org/t/p/w500'
        try:
            movie_a = tmdb.Movies(a)
            response_a = movie_a.info()
            a_title=movie_a.title
            a_poster = movie_a.images()
            a_poster= pos+a_poster['posters'][0]['file_path']
        except:
                a_title= ''
                a_poster= ''
            
        try:
            movie_b = tmdb.Movies(b)
            response_b = movie_b.info()
            b_title=movie_b.title
            b_poster = movie_b.images()
            b_poster= pos+b_poster['posters'][0]['file_path']
        except:
                b_title= ''
                b_poster= ''
        try:    
            movie_c = tmdb.Movies(c)
            response_c = movie_c.info()
            c_title=movie_c.title
            c_poster = movie_c.images()
            c_poster= pos+c_poster['posters'][0]['file_path']
        except:
                c_title= ''
                c_poster= ''        
        
        try:
            movie_d = tmdb.Movies(d)
            response_d = movie_d.info()
            d_title=movie_d.title
            d_poster = movie_d.images()
            d_poster= pos+d_poster['posters'][0]['file_path']
        except:
                d_title= ''
                d_poster= ''  
        try:
            movie_e = tmdb.Movies(e)
            response_e = movie_e.info()
            e_title=movie_e.title
            e_poster = movie_e.images()
            e_poster= pos+e_poster['posters'][0]['file_path']
        except:
                e_title= ''
                e_poster= ''  

        try:
            movie_f = tmdb.Movies(f)
            response_f = movie_f.info()
            f_title=movie_f.title
            f_poster = movie_f.images()
            f_poster= pos+f_poster['posters'][0]['file_path']
        except:
                f_title= ''
                f_poster= ''
        try:  
            movie_g = tmdb.Movies(g)
            response_g = movie_g.info()
            g_title=movie_g.title
            g_poster = movie_g.images()
            g_poster= pos+g_poster['posters'][0]['file_path']
        except:
                g_title= ''
                g_poster= ''  
        try:
            movie_h = tmdb.Movies(h)
            response_h = movie_h.info()
            h_title=movie_h.title
            h_poster = movie_h.images()
            h_poster= pos+h_poster['posters'][0]['file_path']
        except:
                h_title= ''
                h_poster= ''
        try:  
            movie_i = tmdb.Movies(i)
            response_i = movie_i.info()
            i_title=movie_i.title
            i_poster = movie_i.images()
            i_poster= pos+i_poster['posters'][0]['file_path']
        except:
                i_title= ''
                i_poster= ''  
        
        try:
            movie_j = tmdb.Movies(j)
            response_j = movie_j.info()
            j_title=movie_j.title
            j_poster = movie_j.images()
            j_poster= pos+j_poster['posters'][0]['file_path']
        except:
                j_title= ''
                j_poster= ''  

        return  render_template('rec.html',a=a_title,aa=a_poster,b=b_title,bb=b_poster,c=c_title,cc=c_poster,d=d_title,dd=d_poster,e=e_title,ee=e_poster,f=f_title,ff=f_poster,g=g_title,gg=g_poster,h=h_title,hh=h_poster,i=i_title,ii=i_poster,j=j_title,jj=j_poster)



if __name__ == '__main__':
    app.run(host='0.0.0.0')

# def signup():
# signup_data ={
# 'name'    :   request.form['f_name'],
# 'gender'  :   request.form['gender'],
# 'bday'    :   request.form['birthday'],
# 'email'   :   request.form['email'],
# },
# print(signup_data)
# print("\n\n\n\n\n\n\n\n\n\n\n\n")
# table = dynamodb.Table('signup')
# table.put_item(TableName='signup',Item=signup_data)

# DYnamodb put item
# table = dynamodb.Table('signup')
# table.put_item(Item=signup_data)
##Dynamodb get item
# response = table.get_item(
# Key={
#   'email': request.form['email']
# }
# )
##Scan table
# get_data = table.scan()
# print(get_data,'\n')


#  email   =   request.form['email']
# password=   request.form['password']


#  print(password)
#  print('******************')

#  if password=='0':
#   response = make_response(redirect(url_for('static', filename='/html/index.html')))
#      token = jwt.encode({'user_id':email},app.config["SECRET_KEY"],algorithm='HS256')


#     response.set_cookie('js', '1')
#      response.set_cookie('username', 'Ammar')
#  response.set_cookie('JWT', token)
#
#     return response

#   elif password=='1':
#      response = make_response(redirect('/logout'))
#    response.set_cookie('js', '1')
#    response.set_cookie('username', 'Ammar')
#    return response
