from flask import Flask, request, render_template
import boto3
import db_handler as db
import json
import key_config as keys
import urllib.parse
from tkinter import *
from tkinter import messagebox




app = Flask(__name__)


dynamodb = boto3.resource(
    'dynamodb',
    #aws_access_key_id     = keys.ACCESS_KEY_ID,
    #aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)

from boto3.dynamodb.conditions import Key, Attr


@app.route('/')
def default():
    return render_template('login.html')
    
@app.route('/login.html')
def login():
    return render_template('login.html')
    
@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/profile-edit.html')
def update():
    return render_template('profile-edit.html')

@app.route('/profile-view.html')
def view():
    return render_template('profile-view.html')
    
@app.route('/search.html')
def search():
    return render_template('search.html')



@app.route('/signup',methods=['POST'])
def addstudent():
    data = request.form.to_dict()
    
    response = db.add_student(data['fullname'],data['regno'],data['email'],data['passw'],data['course'],data['contactno'],data['gpa'],data['intro'],data['skills'])
 
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return render_template('login.html')

    return {  
        'msg': 'Some error occcured',
        'response': response
    }

@app.route('/login',methods = ['POST'])
def check():
     if request.method=='POST':
        
        email = request.form['email']
        password = request.form['passw']
        
        table = dynamodb.Table('student')
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']

        if password == items[0]['passw']:
            
            getname = items[0]['fullname']
            loadregno = getregno = items[0]['regno']
            loademail = getemail = items[0]['email']
            getpass = items[0]['passw']
            
            getcontact = items[0]['contactno']
            getgpa = items[0]['gpa']
            getintro = items[0]['intro']
            getskills = items[0]['skills']
            
            
            
            currentcourse = items[0]['course']
            courses = [{"course_name": "BSc in Computer Science and Engineering"},{"course_name": "BSc in Mechanical Engineering"},{"course_name": "BSc in Civil Engineering"},{"course_name": "BSc in Electrical Engineering"}]
        
        
            return render_template("profile-edit.html",setname = getname,setregno=getregno,setemail=getemail,setpass= getpass,setcontact=getcontact,setgpa=getgpa,setintro=getintro,setskills=getskills,currentcourse=currentcourse,courses=courses)

        else:
            return {  
        'msg': 'Some error occcured',
        'response': response
    }

  
@app.route('/find',methods = ['post'])
def find():
    if request.method=='POST':
        
        regno = request.form['regno']
        
        table = dynamodb.Table('student')
        response =table.scan(
        FilterExpression=Attr('regno').eq(regno))
        
        items = response['Items']

        
        if(regno!=items[0]['regno']):
            
            error="Student not found"
            return render_template("search.html",error)

        
        
        getname = items[0]['fullname']
        getregno = items[0]['regno']
        getemail = items[0]['email']
        getdegree = items[0]['course']
        getcontact = items[0]['contactno']
        getgpa = items[0]['gpa']
        getintro = items[0]['intro']
        getskills = items[0]['skills']

        if regno == items[0]['regno']:
            return render_template("profile-view.html",setname = getname,setregno=getregno,setemail=getemail,setdegree=getdegree,setcontact=getcontact,setgpa=getgpa,setintro=getintro,setskills=getskills)
        else:
            return {  
        'msg': 'Some error occcured',
        'response': response
    }
    
@app.route('/profile/<regno>', methods=['GET', 'POST'])
def profile(regno):
        
        table = dynamodb.Table('student')
        response =table.scan(
        FilterExpression=Attr('regno').eq(regno))
        
        items = response['Items']
        
        getname = items[0]['fullname']
        getregno = items[0]['regno']
        getemail = items[0]['email']
        getdegree = items[0]['course']
        getcontact = items[0]['contactno']
        getgpa = items[0]['gpa']
        getintro = items[0]['intro']
        getskills = items[0]['skills']

        if regno == items[0]['regno']:
            return render_template("profile-view.html",setname = getname,setregno=getregno,setemail=getemail,setdegree=getdegree,setcontact=getcontact,setgpa=getgpa,setintro=getintro,setskills=getskills)
        else:
            return {  
        'msg': 'Some error occcured',
        'response': response
    }


@app.route('/update', methods=['PUT'])
def update_profile(): 
    data = request.get_json()
    response = db.update_studprofile(data)
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        root = Tk()
        root.withdraw()
        messagebox.showinfo("Window Title", "Your Message")

    return {  
        'msg': 'Some error occcured',
        'response': response
    }
    
 
"""
@app.route('/upload', methods=['POST','GET'])
def upload():
    file = request.files['uploadb']
    filename = file.filename
    bucket_name = 'student-pro-pic'
    bucket = db.s3.Bucket(bucket_name)
    bucket.put_object(
        Key=filename,
        Body=file,
        ContentType='image/jpeg',
        ContentDisposition='inline'
    )
    
    return "successfully updated"
    
    #encoded_object_key = urllib.parse.quote(filename)
    #object_url = f"https://{bucket_name}.s3.amazonaws.com/{encoded_object_key}"
    
    #db.update_profilepicture(loademail,loadregno,object_url)
"""


if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')
