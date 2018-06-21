import os
import pandas as pd 
import pickle
import numpy as np
from flask import Flask, jsonify, request, Markup, render_template,redirect
from textblob.classifiers import NaiveBayesClassifier
from flaskext.mysql import MySQL
import gspread

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file,client,tools
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from flask_mail import Mail,Message
app = Flask(__name__)



@app.route('/favicon.ico')

 

@app.route('/<string:text>')
def apicall(text): 
    filename = 'model.pk'
    with open(r'C:\xampp\htdocs\animation\js\\' + filename,'rb') as filedif:
     cl = pickle.load(filedif)       
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
    

    if str== "On progress":
        value_range_body = {
        "values": [
            [ text , "" , ""]            
        ] 
    }   
    elif str== "Completed task":
        value_range_body = {
        "values": [
            ["", text, ""]            
        ] 
    }   
    else:
        value_range_body = {
        "values": [
            [ "", "",text]            
        ] 
    }   
       
    
     
    
    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute() 
    pprint(response)

    
    return render_template('stt.html',values=str)




@app.route('/sendemail')
def sendemail():
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
    onprogress = []  #array to hold 
    str1 = ""
    str2 = ""
    str3 = ""
    completedtask = []
    followup = []
    for item in values[0]:
        if item!='':
            onprogress.append(item)
            str1 = str1 + item 
            str1 = str1 + '\n'
            
    for item in values[1]:
        if item!='':
            completedtask.append(item)
            str2 = str2 + item
            str2 = str2 + '\n'
    for item in values[2]:
        if item!='':
            followup.append(item)
            str3 = str3 + item
            str3 = str3 + '\n'                
              
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
    msg = Message('Handover Updates', sender = 'handoverabhi@gmail.com', recipients = ['ohyesabhiblogger@gmail.com'])
    msg.html = "<h3>Following are the changes:</h3>\n <b>On progess:</b>\n " +  str1 + "<b>Completed Task :</b> \n" + str2 + "<b>Follow Up :\n" + str3 
    mail.send(msg)
    
    return render_template("email.html")

if __name__ == "__main__":
    app.run()   
       
