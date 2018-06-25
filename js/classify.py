import os
import pandas as pd 
import pickle
import numpy as np
from flask import Flask, jsonify, request, Markup, render_template,redirect,flash,url_for
from textblob.classifiers import NaiveBayesClassifier
from flaskext.mysql import MySQL
import gspread

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file,client,tools
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from flask_mail import Mail,Message
from flask_wtf import Form 
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
app.secret_key = "abhilearner"
class EmailForm(Form):
    email= TextField("Email",[validators.Required("Recepients Email id"),validators.Email("Enter Email")])


@app.route('/favicon.ico')
def kuchbhi():
    print ("Ignore")
    return ('',204)
 

@app.route('/<string:text>')
def apicall(text): 
    filename = 'model.pk'
    with open(filename,'rb') as filedif:
     cl = pickle.load(filedif)     
     print ('Model loaded')  
    str = cl.classify(text)
   

    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    
    spreadsheet_id = '1TQM0ys75pq2GmQFPIpM1_hiucmR2dhoPhYz6CuAN_lE'
    
    
    range_ = 'sheet1!A1'
           

    value_input_option = 'USER_ENTERED'
    insert_data_option = 'INSERT_ROWS'
    
    if str== "Exception":
       value_range_body = {
        "values": [
            [ text ,"", "" , ""]            
        ] 
    }   
    elif str== "On progress":
        value_range_body = {
        "values": [
            [ "",text , "" , ""]            
        ] 
    }   
    elif str== "Completed task":
        value_range_body = {
        "values": [
            ["","", text, ""]            
        ] 
    }   
    else:
        value_range_body = {
        "values": [
            [ "","", "",text]            
        ] 
    }   
       
    
     
    
    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute() 
    pprint(response)

    
    return render_template('stt.html',values=str,text=text)

@app.route('/takeemail',methods=['GET','POST'])
def takeemail():
     form = EmailForm(request.form)
     
     if request.method == 'POST':
         email=request.form['email']
         print (email)

         if form.validate():
             flash('Recieved :' + email)
             return redirect(url_for('sendemail',email=email))
         else:
             flash('Email Not correct bro!') 
     return render_template('takeemail.html',form=form)



@app.route('/sendemail/<email>')
def sendemail(email):
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    
    spreadsheet_id = '1TQM0ys75pq2GmQFPIpM1_hiucmR2dhoPhYz6CuAN_lE'

     #Reading Now
    RANGE_NAME = 'sheet1'
    read = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,range=RANGE_NAME,majorDimension='COLUMNS').execute()
    values = read.get('values', [])
    
    str0 = ""
    str1 = ""
    str2 = ""
    str3 = ""
    # Making string from Spreadsheet of type Exceptions, etc.
    ignore=0
    for item in values[0]:
        if item!='' and ignore:                        
            str0 = str0 + item 
            str0 = str0 + "<br>"
        else: 
            ignore=1    
    ignore=0     
    for item in values[1]:
        if item!='' and ignore:                        
            str1 = str1 + item 
            str1 = str1 + "<br>"
        else: 
            ignore=1    
    ignore=0        
    for item in values[2]:
        if item!='' and ignore:                        
            str2 = str2 + item 
            str2 = str2 + "<br>"
        else: 
            ignore=1
    ignore=0
    for item in values[3]:
        if item!='' and ignore:                        
            str3 = str3 + item 
            str3 = str3 + "<br>"
        else: 
            ignore=1

              
    #print (onprogress)
    
    #Mail k liye code  
    
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'handoverabhi@gmail.com'
    app.config['MAIL_PASSWORD'] = 'handover'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)

    #Ab bhej Rahe
    msg = Message('Handover Updates', sender = 'handoverabhi@gmail.com', recipients = [email])
    msg.html = "<h3 style='background-color:DodgerBlue;'> Following are the changes: </h3> <hr> <h4 style='background-color:Tomato;'> Exceptions: </h4> <br> " + str0 + "<h4 style='background-color:Orange;'>On progess:</h4> <br> " +  str1 + "<br><h4 style='background-color:Green;'>Completed Task :</h4> <br>" + str2 + "<br> <h4 style='background-color:Gray;'>Follow Up :</h4><br>" + str3 
    mail.send(msg)
    
    return render_template("email.html")

if __name__ == "__main__":
    app.run()   
       
