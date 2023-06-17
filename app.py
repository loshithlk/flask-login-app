
from flask import Flask, render_template, request
import key_config as keys
import boto3 
import dynamoDB_create_table as dynamodb_ct

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





if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')
