import threading
import requests
import uuid
import os
import json 
import time


#simple_db_data={}
class fileDownload:
    
    def __init__(self,url):
        self.url=url
        self.downloadpath= "/home/vinoth/Desktop/cloudsek/new/cloudsek001/Download/"
        

    def download(self,link, filelocation,uid):
        global simple_db_data
        r = requests.get(link, stream=True)
        Hcontent_request=r.headers
        Hcontent_request.update({"File-Path":filelocation})
        Hcontent_request.update({"Download_Url":link})
        #simple_db_data.update({uid:Hcontent_request})

        file=open("/home/vinoth/Desktop/cloudsek/new/cloudsek001/simple_db_data.txt","a")
        file.write("'"+str(uid)+"'"+":"+str(Hcontent_request)+",")
        file.close()
        
        with open(filelocation, 'wb') as f:
            for chunk in r.iter_content(1024):
                if chunk:
                    f.write(chunk)

    def createNewDownloadThread(self):
        
        
        uid=str(uuid.uuid4())
        link=self.url
        
        filelocation=self.downloadpath+(self.url.split("/")[-1])
        download_thread = threading.Thread(target=self.download, args=(link,filelocation,uid))
        download_thread.start()
        time.sleep(3)
        res={"id":uid}
        
        return json.dumps(res)
        
        
def file_status(uid):
    file=open("/home/vinoth/Desktop/cloudsek/new/cloudsek001/simple_db_data.txt","r")
    simple_db_data=file.read()
    simple_db_data=eval(simple_db_data+'}')
    file.close()

    if (not uid in simple_db_data.keys()):
        return "Invalid-id"
    else:
        
        total_file_Size=int(simple_db_data[uid]['Content-Length'])
        downloaded_file_size=os.path.getsize(simple_db_data[uid]['File-Path'])
        remaining_fileSize=total_file_Size-downloaded_file_size
        status= "Completed" if remaining_fileSize==0 else "In-Progess"
        res=json.dumps({"total_file_Size":str(total_file_Size/1028)+" KB","downloaded_file_size":str(downloaded_file_size/1028)+" KB"
        ,"remaining_fileSize":str(remaining_fileSize/1028)+" KB","status":status})

        
        return res
        
    
 
