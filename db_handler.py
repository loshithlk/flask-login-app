import boto3
import json
import key_config as keys



dynamodb_resource = boto3.resource(
    'dynamodb',
    #aws_access_key_id     = keys.ACCESS_KEY_ID,
    #aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = keys.REGION_NAME,
)


s3 = boto3.resource(
    's3',
    #aws_access_key_id     = keys.ACCESS_KEY_ID,
    #aws_secret_access_key = keys.ACCESS_SECRET_KEY,
    region_name           = 'ap-southeast-1',
)

table = dynamodb_resource.Table('student')


def add_student(fullname, regno, email,passw,course,contactno,gpa,intro,skills):
    response = table.put_item(
        Item = {
            'fullname'     : fullname,
            'regno'  : regno,
            'email' : email,
            'passw' : passw,
            'course'  : course,
            'contactno':contactno,
            'gpa':gpa,
            'intro':intro,
            'skills':skills
        }
    )
    return response
    
def update_studprofile(data:dict):
    response = table.update_item(
        Key = {
           'email': data['email'],
           'regno':data['regno']
        },
        AttributeUpdates={
            
            'fullname': {
               'Value'  : data['fullname'],
               'Action' : 'PUT' 
            },
            'passw': {
               'Value'  : data['passw'],
               'Action' : 'PUT'
            },
            'course': {
               'Value'  : data['course'],
               'Action' : 'PUT'
            },
            'contactno': {
               'Value'  : data['contactno'],
               'Action' : 'PUT'
            },
            'gpa': {
               'Value'  : data['gpa'],
               'Action' : 'PUT'
            },
            'intro': {
               'Value'  : data['intro'],
               'Action' : 'PUT'
            },
            'skills': {
               'Value'  : data['skills'],
               'Action' : 'PUT'
            }
        },
        
    )
    return response
    
def update_profilepicture(email,regno,url):
    response = table.update_item(
        Key = {
           'email': email,
           'regno':regno
        },
        AttributeUpdates={
            
            'fullname': {
               'Value'  : url,
               'Action' : 'PUT' 
            }
        },
        
    )
    return response