from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import numpy as np
from PIL import Image
import base64
import os
import re
from io import StringIO, BytesIO
import face_recognition
import time
import requests
import pdb
import boto3
import key_config as keys

app = Flask(__name__)
#global pan
#pan='MCLPS8412F'

dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY)
                    

from boto3.dynamodb.conditions import Key, Attr

@app.route("/", methods=['GET', 'POST'])#landing
def kycstart():
    global pan
    filepath = "NOT FOUND"
    filepath2 = "NOT FOUND"
    if request.method == 'POST':
        img = request.files['photograph']
        card = request.files['pan-card']
        phnumber=request.files['mobile-number']
        aadharnumber=request.files['aadhar-card-number']
        name = request.form['f-name']
        pan = request.form['pan-card-number']
        password = request.form['password']
        
        table = dynamodb.Table('users')
        
        table.put_item(
                Item={
        'name': name,
        'pan-number': pan,
        'ph-number': phnumber,
        'aadhar-number':aadharnumber,
        'password':password
        
            }
        )
        if not os.path.isdir('static/user'):
            os.mkdir('static/user')

        #if 'static\user\user.jpg' is found, delete it
        if os.path.isfile('static/user/user.jpg'):
            os.remove('static/user/user.jpg')

        #if 'static\user\user.jpg' is found, delete it
        if os.path.isfile('static/user/pan_user.jpg'):
            os.remove('static/user/pan_user.jpg')

        #storing in file system
        filepath = os.path.join('static/user', img.filename)
        filepath2 = os.path.join('static/user', card.filename)
        newName = "static/user/user.jpg"
        newName2 = "static/user/pan_user.jpg"

        img.save(filepath)
        card.save(filepath2)
        fp = os.rename(filepath, newName)
        fp2 = os.rename(filepath2, newName2)        
            
        return redirect(url_for('verify'))
    
    return render_template('signup.html')

@app.route("/verify", methods=['GET', 'POST'])
def verify():
    if request.method=='POST':
        time.sleep(5)
        original=face_recognition.load_image_file('static/user/user.jpg')
        captured=face_recognition.load_image_file('static/image.png')
        knownFace=[]
        knownEncoding=face_recognition.face_encodings(original)[0]
        knownFace.append(knownEncoding)
        unknownEncodings=face_recognition.face_encodings(captured)
        if len(unknownEncodings)>0:
            result=face_recognition.compare_faces(knownFace,unknownEncodings[0])
        else:
            return redirect(url_for('error'))#redirecting to error page 
        if result==[True]:
            return redirect(url_for('status'))#redirecting to panverification page
        elif result==[False]:
            return redirect(url_for('error'))#redirecting to error page when unsuccessful
        

    return render_template('pic_capture.html')

@app.route("/error", methods=['GET', 'POST'])
def error():
    if request.method=='POST':
        time.sleep(5)
        original=face_recognition.load_image_file('static/user/user.jpg')
        captured=face_recognition.load_image_file('static/image.png')
        knownFace=[]
        knownEncoding=face_recognition.face_encodings(original)[0]
        knownFace.append(knownEncoding)
        unknownEncodings=face_recognition.face_encodings(captured)
        if len(unknownEncodings)>0:
            result=face_recognition.compare_faces(knownFace,unknownEncodings[0])
        else:
            return redirect(url_for('error'))
        if result==[True]:
            return redirect(url_for('status'))
        elif result==[False]:
            return redirect(url_for('error'))
        

    return render_template('error.html')

@app.route('/hook', methods=['POST','GET'])
def hook():
    image_b64 = request.values['imageBase64']
    image_data = re.sub('^data:image/.+;base64,', '', image_b64)
    image_data = base64.b64decode(str(image_data))
    image_PIL = Image.open(BytesIO(image_data))
    image_save = image_PIL.save('static/image.png')
 
    return ''

@app.route("/status",methods=['POST','GET'])#panverification page
def status():
    if request.method=='POST':
        time.sleep(5)
        file='static/image.png'
        
        url = 'https://app.nanonets.com/api/v2/OCR/Model/544b09c6-56dc-404c-8405-f44f9e259bd5/LabelFile/'

        data = {'file': open(file, 'rb')}

        response = requests.post(url, auth=requests.auth.HTTPBasicAuth('eqGTqzu3TQa1jqh9DrCgxegpgSZ3Nq7B', ''), files=data)

        line=response.text
        ind=line.find('ocr_text')
        num=line[ind+11:ind+21]#pan number extracted from the captured pan image
        
        if(line == None):
            return redirect(url_for('panerror'))

        
        #checking if the pan number from captured picture is same as pan number entered in the form
        if(len(num) == 10 and num==pan):
            return redirect(url_for('pan_status'))
                
        return redirect(url_for("panerror"))#when false, redirects to panerror page

    return render_template('panverification.html')


@app.route("/panerror",methods=['POST','GET'])#when pan verification occurs
def panerror():
    if request.method=='POST':
        time.sleep(5)
        file='static/image.png'
        #api for converting text from image
        url = 'https://app.nanonets.com/api/v2/OCR/Model/544b09c6-56dc-404c-8405-f44f9e259bd5/LabelFile/'

        data = {'file': open(file, 'rb')}

        response = requests.post(url, auth=requests.auth.HTTPBasicAuth('eqGTqzu3TQa1jqh9DrCgxegpgSZ3Nq7B', ''), files=data)

        line=response.text
        ind=line.find('ocr_text')
        num=line[ind+11:ind+21]#pan number extracted from the captured pan image
        
        if(line == None):
            return redirect(url_for('status'))

        #checking if the pan number from captured picture is same as pan number entered in the form
        if(len(num) == 10 and num==pan):
            return redirect(url_for('pan_status'))
                
        return redirect(url_for("panerror"))

    return render_template('panerror.html')

@app.route('/pan_status',methods=['POST','GET'])#when everything verified successfully.
def pan_status():
    os.remove('static\\user\\pan_user.jpg')#removing from file system database
    os.remove('static\\user\\user.jpg')
    os.remove('static\\image.png')
    return render_template('userconfirm.html')

@app.route('/login')
def login():    
    return render_template('login.html')

@app.route('/check',methods = ['post'])
def check():
    if request.method=='POST':
        
        aadharnumber = request.form['aadhar-card-number']
        
        password = request.form['password']
        
        table = dynamodb.Table('users')
        response = table.query(
                KeyConditionExpression=Key('aadhar-card-number').eq(aadharnumber)
                
        )
        items = response['Items']
        name = items[0]['name']

        print(items[0]['password'])
        if password == items[0]['password']:
            
            return render_template("details.html",name = name)
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)