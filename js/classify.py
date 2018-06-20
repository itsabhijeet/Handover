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

app = Flask(__name__)

@app.route('/favicon.ico')


@app.route('/<string:text>')
def apicall(text):    
    train = [
        ('I am on this task', 'On progress'),
        ('The billing cycle 2 is complete', 'Completed task'),
        ('I have completed the task that was assigned', 'Completed task'),
        ('I am still on it', 'On progress'),
        ('Not completed', 'On progress'),
        ("The CRM model diagnositics in not complete", 'On progress'),
        ('I need you to check billing cycle 2', 'Follow up'),
        ('I need an update on this tomorrow', 'Follow up'),
        ("This cycle is close now", 'Completed task'),
        ('I have wrapped up the work', 'Completed task'),
        ('Exception no. 3,4 need to be handled', 'On progress'),
        ('I am on this task', 'On progress'),
        ('The billing cycle 2 is complete', 'Completed task'),
        ('I have completed the task that was assigned', 'Completed task'),
        ('I am still on it', 'On progress'),
        ("The CRM model diagnositics in not complete", 'On progress'),
        ('I need you to check billing cycle 2', 'Follow up'),
        ('I need an update on this tomorrow', 'Follow up'),
        ("This cycle is close now", 'Completed task'),
        ('I have wrapped up the work', 'Completed task'),
        ('Exception no. 3,4 need to be handled', 'On progress'),
        ('I am on this task', 'On progress'),
        ('T', 'Completed task'),
        ('I have completed the task that was assigned', 'Completed task'),
        ('I am still on it', 'On progress'),
        ("The CRM model diagnositics in not complete", 'On progress'),
        ('I need you to check billing cycle 2', 'Follow up'),
        ('I need an update on this tomorrow', 'Follow up'),
        ("This cycle is close now", 'Completed task'),
        ('I have wrapped up the workhe billing cycle 2 is complete', 'Completed task'),
        ('Exception no. 3,4 need to be handled', 'On progress')
    ]
    test = [
        ('I am on this task', 'On progress'),
        ('The billing cycle 2 is complete', 'Completed task'),
        ('I have completed the task that was assigned', 'Completed task'),
        ('I am still on it', 'On progress'),
        ("The CRM model diagnositics in not complete", 'On progress'),
        ('I need you to check billing cycle 2', 'Follow up'),
        ('I need an update on this tomorrow', 'Follow up'),
        ("This cycle is close now", 'Completed task'),
        ('I have wrapped up the work', 'Completed task'),
        ('Exception no. 3,4 need to be handled', 'On progress')
    ]
    cl = NaiveBayesClassifier(train)
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
if __name__ == "__main__":
    app.run()        
