from flask import Flask, render_template, request, jsonify
from flask_mail import Mail
import datetime
from flask_sqlalchemy import SQLAlchemy
import json

local_server = True
with open('templates/congif.json','r')as c:
    params=json.load(c)["params"]

app = Flask(__name__)
blog_post=[{
    "id": 1,
   "Title" : "Web-development and Al",
    "Subtitle" : "Use of chatgpt and frameworks in web-development",
    "Date": "23-Aug-2023"
},
{
    "id": 2,
   "Title" : "Python language usage",
    "Subtitle" : "How python is easy and efficient language",
    "Date": "31-July-2022"
}
]
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_TLS = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password'],

)

mail= Mail(app)


if local_server:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']

db = SQLAlchemy(app)


class Contact(db.Model):
    """"
    Sno. Name Email Phone_num Message Date
    """
    Sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), unique=False, nullable=False)
    Email = db.Column(db.String(120), nullable=False)
    Phone_num = db.Column(db.String(120),nullable=True)
    Message = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(20),)



@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html", posts=blog_post)

@app.route("/posts")
def list_jobs():
    return jsonify(blog_post)
@app.route("/about.html")
def about():
    return render_template("about.html")


@app.route("/contact.html", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        '''add entry to the database '''
        name = request.form.get('name')
        email = request.form.get('Email')
        phone = request.form.get('Phone_num')
        message = request.form.get('message')
        current_date = datetime.datetime.now()
        """ Sno. Name Email Phone_num Message Date """
        entry= Contact(Name=name, Email=email, Phone_num=phone, Message=message, Date=current_date)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from Blogs' + name,
                          sender='email',
                          recipients= [params['gmail-user']],
                          body= message+'\n'+phone )
    return render_template("contact.html")



@app.route("/post.html")
def post():
    return render_template("post.html")
