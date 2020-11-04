from flask_sqlalchemy import SQLAlchemy
from wsgiref import simple_server
from flask import Flask, render_template ,redirect, url_for,request,session,flash
from functools import wraps
import re
from datetime import datetime
import bcrypt
import json
import time
from keras_preprocessing.text import tokenizer_from_json
from keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json
import pandas as pd

import requests 
link = "https://www.kaggleusercontent.com/kf/46112612/eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0..AkAOfiqZdRbd1eFeI3WFJQ.7eVop-R5834i378A6tu3-SlRrYZJKxG1NvoL3gq5nkHqpfVFF47xmouNxbcQRpwTjA_D0o5fI2AP1fHLw1TqTTbwV1TP3By98LjDmbxtiu8aonfDp9tesmEu9e51QnBZCZPADgrTi1hL1lt-3Di3XritE6smVr4-dPSUXLTJ6cmJofBfZpkUg-3uIqys6wrvT73dNWadzUCLGCTzCeQlWfqEV1_N97vA3O4b92QZT8N0QodhAc8qKWthcnBYWVsw4dsJoo4Q3tlNptiHeW6h78_5mmaqKmgNTdR_fM6yVu8SmakfvJAK66WWYIjaM6j5S5CMRcoSmwBzbgoEjYOd6pDIq4hiKFH_V3CY6-Q5iLa1Wo37-cYOTaKZXvM9tJXfZH6CcTACnb3O-W5VN8NFo8Xcw9yegTuOULI5zwPPXqdlYcWOG1je0Hoe0ENOCdC2W4GgZR7DqyhpF21lx5qwn_bdg19f7NsBoiUYyFUKsu3emzVlhG--amlk2uH0DFAg0T5D6588Y70zhvFUiNMy4UrZY8r8l9pYFk0pVZlRY2oR056syzm6syuDFdSMBxtCyKi7To94j7yY2JD2cDv7iPVQImRo0GoRsX0eYqnCOMUWJtec83_gRRkteogP7bMIgVPUbouGMKknKhELPXPy0m8_T5w-oIsCYWLt5d3yxSY.y84urFSNqoWcGW-foO5T9A/GRU_model_weights.h5"
r = requests.get(link) 
with open("GRU_model_weights.h5",'wb') as f: 
    f.write(r.content) 

link = "https://www.kaggleusercontent.com/kf/46112612/eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0..8FPB4aj2MoVXUkmaCWIe2g.-JE8GSABWNmSLOeLZIgQisLpkQ48YeVhBhKtUfirYv_EVVhjR2-pPedkQhB_i98EezdYUAX38kN7rMwMrlp7O9gMn9xUIudN-fddiFYWFKDOGYYfzSIgAYKQxumxSIoFUgGr-coPBkB8Ik8IxvNoIHF6YRWSMp02iJoQOg6ZNy3tPa0sVUUHAs_ALYvozjgwzoCzsP3JcOVTbUiieMmCVFF2Dl40fcC-WmHiWia1uF_KWrSgG9KUuVtJfF5Su53-nPl3SOg23zae-0AkpYttN_nVtVFC7UaoY2GYYsvwtFhPHDBOJwkDJhuK3w3MGDQAOA2yrfB-dXUyN2zN4ifpuTlEEe57YXk6SqEbmprpW8xk2MDf4-EamaVW0hH2NDkM96IqkW0Nosaezw_XEZYeBePnXMPqZVwhrFAvWmyCStooSDulz_VCs0YkgnXzibh_iS20MOUycXtM4_TVB7qYJcLie2WcqYTTqtwYqOnTcLZmY9aHggYbkdJxstK98cjTjWbpxrr9Ayze7uWoQ9SjKQVABcgMLYIhZ3t679FJmabTedvxOfxcpyp1_Ne8-cEO3dJlJ-F8eUteDXNhWiAqY7nyOKWiETgXtLCraKYKLEK45SYwPXjmZdv_3KaNT1YczuvALi10QrvCpHLHw14CZLrjKS0TyXiw2whXgFvcj6Q.o5zrK5Wjm3DZBP9dHlzsQQ/GRU_model_architecture.json"
r = requests.get(link) 
with open("GRU_model_architecture.json",'wb') as f: 
    f.write(r.content) 

link = "https://www.kaggleusercontent.com/kf/46112612/eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0..o-xW7eD2qSW0-fnIH2KRlQ.TVrSzSZ0b1yhQuzsw71uBED4JpFiG1OfXwdyWnR4-Wnf8ryKfdtBPZbmHPnv7v4kSSnauUsnk3CnLbEcMGRD2t_QfVfBiAxjmzUTYyGkd_r_2jCwjpsIy22D8Za0sI2A_sgv38OuXkkaexuxYoy2lqtcRdOzYIUvRlMZbxdZFH16upKjdDaGFLJG6hKeU4B18gOdJZ_xJH7JlwBU9zVdO0b6-k1cXTYTcp-W6pSpMagjKtvCza8yDTOJgPdZIog9vXFHDtUk5XCj7U8kZLU3coo5mv5ESukVsxRzTkYjRccKL1Cbowa12oggFJTGadL4qJLAE7Lx1awpWdvV5PRtxRVTgnIfkMipA9xbLfGDreeHqKBdjx4rMzaPuJGDZ5FrML8tDJNHrkgIqSlDXSXYyTdlpxmuUsSW-mHt32ho5nZYgObnI86e1JXwsgxFs2GH7gmGBc6FUfQqE6iIJer3UBnQzphRAziLh_aUi6oH26j2Sl_m19pjq33aofwKug9VzQYa7YCT_TfYt6H8gpn-adzVEqcNCifqC_0t1ZQkFZetMs4IUgSkytaVySsI_XN6h5ss4ygectHxeAmqvFZJSHqwZxST82uZP15yhWW9oP3MBK58u__jBnQk7QlnU3P3Ct2I0a32EJaUqN0k4yh-0u4m-ibihEL7dV3ayxhTXbs.bD9TsPT-h2U-LzQH5n_-Sw/tokenizer.json"
r = requests.get(link) 
with open("tokenizer.json",'wb') as f: 
    f.write(r.content) 


def init():
    with open('GRU_model_architecture.json', 'r') as f:
        model = model_from_json(f.read())
    model.load_weights('GRU_model_weights.h5')    
    return model
    
with open('tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)
    
model=init()   
import os
os.remove("GRU_model_architecture.json")
os.remove("tokenizer.json")
os.remove("GRU_model_weights.h5") 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
current_user = ""
current_user_id = 0

def predict(text):
    start_at = time.time()
    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=300)
    # Predict
    score = model.predict([x_test])[0]

    return {"score": float(score),
       "elapsed_time": time.time()-start_at}

print(predict("HI THERE"))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.sentiment}')"


# posts = [
#     {
#         'author':'Sree Ramji',
#         'title':'Blog Post 1',
#         'content':'w0rk 5h0uld b3 m1nd 1nv0lv3d 7h1n6',
#         'date_posted':'Jan 2, 2020'
#     },

#     {
#         'author': 'Hare SRV',
#         'title': 'Blog Post 2',
#         'content': '7h053 v10l3n7 d3l16h75 h4v3 v10l3n7 3nd5',
#         'date_posted': 'Jan 5, 2020'
#     }
# ]

posts = []

# users = {"Chosen_One":"DrewMcintyre123","Architect":"SethRollins123","Rated_R_Superstar":"Edge123","Phenomenal_One":"AJStyles123"}

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.','danger')
            return redirect(url_for('login'))
    return wrap


def validate(password):
        if len(password) < 6:
            return 1
        elif re.search('[0-9]',password) is None:
            return 2
        elif re.search('[A-Za-z]',password) is None:
            return 3
        else:
            return None


def isInvalid(username):
        user=User.query.filter_by(username=username).first()
        if user:
            return 1
        else:
            return 0


def isInvalidMail(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return 1
    else:
        return 0

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        if(column.name=='user_id'):
            # print(int(str(getattr(row, column.name))))
            if(db.session.query(User).filter_by(id=int(str(getattr(row, column.name)))).first()!=None):
                d["author"] =   str(db.session.query(User).filter_by(id=int(str(getattr(row, column.name)))).first().username)
        else:
            d[column.name] = str(getattr(row, column.name))
    return d


def update():
    posts.clear()
    for i in db.session.query(Post).all():
        posts.append(row2dict(i))  
    # print(posts)
@app.route("/")
@app.route("/home")
@login_required
def home():
    update()
    # print(posts)
    return render_template("home.html",posts=posts)

@app.route("/about")
def about():
    return render_template("about.html",title='About')


@login_required
@app.route("/create",methods = ['GET','POST'])
def create():
    if request.method == 'POST':
        if request.form["title"] == "" or request.form["content"] == "":
            flash('Enter all fields','danger')

        else:
            # print(type(current_user_id))
            x=predict(request.form["content"])
            print(x)
            if(x["score"]>0.5):
                sentiment="Toxic";
            else:
                sentiment="Not Toxic";
            db.session.add(Post(title = request.form["title"],content = request.form["content"],user_id = current_user_id,sentiment=sentiment))
            # print(dict(db.session.query(Post).filter_by(title=request.form["title"]).__dict__))
            db.session.commit()
            update()
            return redirect(url_for("home"))
    
    return render_template("new_post.html",title='NEW POST')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # bcrypt.hashpw(request.form['password'].encode('utf-8').encode('utf-8'), hashed_password) == hashed_password
        user = User.query.filter_by(username=request.form['username']).first()
        hashed_password = User.query.filter_by(username=request.form['username']).first().password
        if not (user and (bcrypt.hashpw(request.form['password'].encode('utf-8'), hashed_password) == hashed_password)):
                # error = 'Invalid Credentials. Please try again.'
                flash('Invalid Credentials. Please try again.','danger')
                # print(users)
        else:
            current_user=request.form['username']
            current_user_id = User.query.filter_by(username=request.form['username']).first().id
            current_user_id = int(current_user_id)
            session['logged_in'] = True
            # print("CUR1",current_user)
            flash('You were logged in.','success')
            update()
            
            return redirect(url_for('home'))

    return render_template('login.html', error=error)

@app.route('/deletePost/<blogid>')
@login_required
def deletePost(blogid):
    Post.query.filter_by(id=int(blogid)).delete()
    # db.session.delete(obj)
    print(Post.query.filter_by(id=int(blogid)))
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['fname']=="" or request.form['lname']=="" or request.form['mobile']=="" or request.form['email']=="" or request.form['username']=="" or request.form['password']=="" or request.form['cpassword']=="":
            flash('Fill all Credentials and Try again.',"danger")
        else:
            if not(request.form['password']==request.form['cpassword']):
                flash('Passwords mismatch',"danger")
            else:
                x = validate(request.form['password'])
                if x is not None:
                    if x==1:
                        flash("Make sure your password is atlaest 6 letters","danger")
                    elif x==2:
                        flash("Make sure your password has a number in it","danger")
                    else:
                        flash("Make sure your password has a letter in it","danger")
                elif isInvalid(request.form['username']):
                    flash("Username already exists!!", "danger")
                elif isInvalidMail(request.form['email']):
                    flash("Email already exists!!", "danger")
                else:
                    hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'),bcrypt.gensalt())
                        # .decode('utf-8')
                    user = User(username=request.form['username'],email=request.form['email'],password=hashed_password)
                    db.session.add(user)
                    db.session.commit()
                    flash("Registration Success!! Your Details have been added." ,"warning")
                    # print(hashed_password)
                    # print(users)
                    return redirect(url_for('home'))

    return render_template('register.html', error=error)



@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    current_user=""
    current_user_id=""
    flash('You were logged out.')
    # print("CUR2",current_user)
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    # flash('Non Existent Page',"error")
    return render_template('error.html'), 404

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    httpd.serve_forever()

