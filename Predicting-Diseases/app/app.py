# -*- coding: utf-8 -*-
"""
Created on Tue May  5 20:24:21 2020

@author: 94712
"""
import smtplib, ssl
from random import randint
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# mail
import numpy as np
import bs4
import selenium.webdriver as selenium
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
import csv
from twilio.rest import Client
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


with open('api.csv', newline='') as f:
    reader = csv.reader(f)
    fresh_data = dict(reader) 
    data = fresh_data.copy()

cred   = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

#print(data.values())
app = Flask(__name__)
model = pickle.load(open('../Models/newTrained/model_decisiontree.pkl','rb'))
df = pd.read_csv('mostImportant.csv')
dict_ = dict(zip(df.Date, df.DateValue))


@app.route('/api/predict',methods=["POST"])
def predict():
    symptom = request.get_json()
    data = fresh_data.copy()
    # print(symptom)
    for i in range(len(symptom)):
        data[symptom[i]] = 1
    #features = data.values()
    #print(features)
    vals = np.fromiter(data.values(), dtype=float)
    disease = model.predict([vals])
    # print(disease)
    return jsonify(disease[0])
@app.route('/api/email',methods=['POST'])
def sendEmail():
    data = request.get_json()
    print(data)
    uid = data[1]
    data = data[0]
    email = (data['email'])
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "ransakaravi@gmail.com"
    password = 'qchaos@123'
    receiver_email = email
    OTP = randint(1000, 9999)
    message = "OTP"
    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        return addOTP(uid,OTP)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        return jsonify(False)
    finally:
        server.quit()
        # return ()

@app.route('/api/disease',methods=["POST"])
def disease():
    disease = request.get_json()
    print(str(disease))
    str_disease = str(disease)
    symptoms = dict_[str_disease]
    symptoms = symptoms.split(',')
    return jsonify(symptoms)

@app.route('/api/doctor_verification',methods=["POST"])
def doctor_verification():
    data = request.get_json()
    # print(data)
    # print(data[1])
    uid = data[1]
    # print(uid)
    data = data[0]
    reg_no = str(data['docID'])
    act_no = str(data['age'])
    FullName = str(data['name'])
    email = str(data['email'])

    try:
        my_url = 'https://www.srilankamedicalcouncil.org/registry.php?registry='+(act_no)+'&initials=&last_name=&other_name=&reg_no='+(reg_no)+'&nic=&part_of_address=&search=Search'
        uCLient = uReq(my_url)
        # print(my_url)
        page_html = uCLient.read()
        uCLient.close()    
        # data = []
        page_soup = soup(page_html,"html.parser")
        table = page_soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="r_table") 
        rows = table.findAll(lambda tag: tag.name=='tr')
        for row in rows:
            cells = row.findAll('td')
            cells = [ele.text.strip() for ele in cells]
        name_web = cells[3].replace(" ","")
        FullName2 = FullName.strip()
        docName = FullName2.replace(" ","")

        print(docName,name_web)

        if(docName==name_web):
            status = "valid doctor"
            return updateFlag(email,FullName, uid,True,status)

        else:
            status = 'invalid doctor'
            return updateFlag(email,FullName,uid,False,status)
        # return jsonify(cells)
    except:
        status = "No Doctor data associated with this credintials"
        return updateFlag(email,FullName,uid,False,status)

def sendTextMessage(FullName,address):
    client = Client("AC8cb4a76d6dcdbb9a29cb5a9cf59a3110", "91774c5f46c2b8d11300d4f1b3432f5f")
    client.messages.create(to="+940712816739", 
                       from_="+12724222837", 
                       body=("Hello "+ FullName +" We verified your account.We will send verification code to your address:\n"+address+"\nThanks for using Onclinic"))
    return "Message Sent!"

def updateFlag(email,name,id,flag,status):
    user_ref = db.collection(u'Users').document(id)
    user_ref.update({u'slmcVerified': flag})
    # dody = [flag,ststus]
    return jsonify(email,name,status)

def addOTP(id,OTP):
    user_ref = db.collection(u'Users').document(id)
    user_ref.update({u'OTP': OTP})
    return jsonify(OTP,True)

def emailVerified(id):
    user_ref = db.collection(u'Users').document(id)
    user_ref.update({u'emailVerified': True})




if __name__ == "__main__":
    app.run(debug=True)