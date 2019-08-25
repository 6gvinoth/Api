"""
Routes and views for the flask application.
"""
from flask import render_template,send_file,Response,jsonify
from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import  json

from cloudsek import app

import fileDownload as fd
import os 

limiter =Limiter(app,key_func=get_remote_address)

#@limiter.limit('3 per day')

@app.route('/test')
def home():
        
    uid= request.values["id"]
    return render_template(
        'index.html',
        title='Home Page',uid=uid
    )

@app.route('/download',methods=["POST"])
def download():
    
    url = request.values["url"]
    try:
        r = requests.get(url,stream=True)  
        if "Content-Length" in dict(r.headers).keys():
            sobj_=fd.fileDownload(url)
            result=sobj_.createNewDownloadThread()
            response = app.response_class(
                response=result ,
                status=200,
                mimetype='application/json'
                )       
            return response
        else:
            r={"Error":"Invalid-Adress !!!!"}
            return json.dumps(r)

    except:
        r={"Error":"Connection-Error"}
    
        return json.dumps(r)
    
        
@app.route("/status",methods=["GET"])
def status():
    uid = request.values["id"]
    obj_fb=fd.file_status(uid)
    response = app.response_class(
        response=obj_fb ,
        status=200,
        mimetype='application/json'
        )
    return response

@app.route('/progress',methods=["GET"])
def progress():

    global id_p 
    id_p= request.values["id"]
    file=open("/home/vinoth/Desktop/cloudsek/new/cloudsek001/simple_db_data.txt","r")
    simple_db_data=file.read()
    simple_db_data=eval(simple_db_data+'}')
    file.close()
    def generate():

        if id_p == 'undefined':
            x="stop"
            yield "data:"+str(x) + "\n\n"
        
        elif(not id_p in simple_db_data.keys()):
            while(id_p in simple_db_data.keys()):
                x=0
                yield "data:" + str(x) + "\n\n"
            
        else:
        
            totallenth=int(simple_db_data[id_p]['Content-Length'])
            while  not(os.path.exists(simple_db_data[id_p]['File-Path'])):
                time.sleep(1)

            v=os.path.getsize(simple_db_data[id_p]['File-Path'])

            
            x=round((v/totallenth)*100)

            while x <= 100:
                yield "data:" + str(x) + "\n\n"
                v=os.path.getsize(simple_db_data[id_p]['File-Path'])
                x=round((v/totallenth)*100)
                if x>=100:
                	break
    return Response(generate(), mimetype= 'text/event-stream')  


@limiter.limit("100/day")
@limiter.limit("10/hour")
@limiter.limit("4/minute") 
@app.route('/')     
@app.route('/home')
def test():
    return render_template(
        'download_page.html',
        title='Home Page'
    )
    

@app.route('/data')
def data():
    file=open("/home/vinoth/Desktop/cloudsek/new/cloudsek001/simple_db_data.txt","r")
    simple_db_data=file.read()
    simple_db_data=eval(simple_db_data+'}')
    file.close()
    #files=os.listdir("/home/vinoth/Desktop/cloudsek/new/cloudsek001/Download/")
    files=simple_db_data
    return render_template("filesDowloadDir.html",files=files)   

@app.route('/file')
def downloadFile():
    file=open("/home/vinoth/Desktop/cloudsek/new/cloudsek001/simple_db_data.txt","r")
    simple_db_data=file.read()
    simple_db_data=eval(simple_db_data+'}')
    file.close()
    id= request.values["id"]
    if id in simple_db_data.keys():
        path = simple_db_data[id]["File-Path"]
        return send_file(path, as_attachment=True)
    else:
        return "Invalid - Id ?????"


    
