import sys

import requests
url = "https://v4pre.h5sys.cn/api/11148689/"
params = {"type": "json"}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
def updata(version_now,url=url):
    url=url+"updata"
    re=requests.get(url).json()
    if re["return"]=="okey":
        version=re["body"][0][0]
        if version > version_now:
            return {"return":"updata","url":re["body"][0][1]}
        else:
            return {"return":"okey"}
def logon(name:str,phone:str,password:str,url=url): #注册账号
    url=url+"newuesr"
    params={"name":name,"phone":phone,"password":password}
    re=requests.get(url,params).json()
    if(re["return"]=="okey"):
        return re
    else:
        return re
def getscore(name:str,subject:str,score:str,url=url):
    url=url+"getscore"
    params={"name":name,"class":subject,"score":score}
    re=requests.get(url,params).json()
    return re
def sign_in(phone:str,password:str,url=url):
    url=url+"signup"
    params={"phone":phone,"password":password}
    re=requests.get(url,params).json()
    return re
def clone_score(name:str,subject:str,url=url):
    url=url+"clone_score"
    params={"name":name,"class":subject}
    re=requests.get(url,params).json()
    return re
def leave_massage(name:str,object:str,text:str,anonymous:bool,url=url):
    url=url+"leave_massage"
    params={"name":name,"留言对象":object,"留言内容":text,"匿名":anonymous}
    re=requests.get(url,params).json()
    return re
def clone_score_teacher(url=url):
    url=url+"clone_score_teather"
    re=requests.get(url).json()
    return re
def clone_massage_teacher(teacher:str,url=url):
    url=url+"clone_massage_teacher"
    params={"teacher":teacher}
    re=requests.get(url,params).json()
    return re
def report(object:str,text:str,name:str,url=url):
    url=url+"report"
    params={"object":object,"text":text,"name":name}
    re=requests.get(url,params).json()
    return re