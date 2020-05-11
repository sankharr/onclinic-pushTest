# -*- coding: utf-8 -*-
"""
Created on Tue May  5 20:24:21 2020

@author: 94712
"""


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
    # print(FullName)
    # FullName = FullName.split(" ","")
    # id = request.args.get('id')
    # print(id)
    # print('Im here')

    # print(type(reg_no))
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
        #general_text_container = page_soup.findAll("tbody",{"tr":"tr0"})
        for row in rows:
            cells = row.findAll('td')
            cells = [ele.text.strip() for ele in cells]
        name_web = cells[3].replace(" ","")##secondly added
        # print(cells)
        # print(cells)
        # print(cells[3])
        FullName2 = FullName.strip()
        docName = FullName2.replace(" ","")##also
        # print(len(FullName2))
        # print(len(cells[3]))
        # print()
        print(docName,name_web)

        if(docName==name_web):
            return updateFlag(uid)
        # if (FullName2==cells[3]):
        #     # return jsonify(True)
        #     return updateFlag(uid)
        #     # return sendTextMessage(FullName,cells[4])
        else:
            return jsonify(cells[3])
        return jsonify(cells)
    except:
        # print('No data')
        failed = "No Doctor data associated with this credintials"
        return jsonify(failed)

def sendTextMessage(FullName,address):
    client = Client("AC8cb4a76d6dcdbb9a29cb5a9cf59a3110", "91774c5f46c2b8d11300d4f1b3432f5f")
    client.messages.create(to="+940712816739", 
                       from_="+12724222837", 
                       body=("Hello "+ FullName +" We verified your account.We will send verification code to your address:\n"+address+"\nThanks for using Onclinic"))
    return "Message Sent!"

def updateFlag(id):
#     doc_ref = db.collection(u'Users').document(id)
#     doc_ref.set({
#     u'slmcVerified': True
# })
#     print(id)
    user_ref = db.collection(u'Users').document(id)

# Set the capital field
    user_ref.update({u'slmcVerified': True})
    return jsonify(True)
  


if __name__ == "__main__":
    app.run(debug=True)