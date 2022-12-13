import requests
url = "https://v4pre.h5sys.cn/api/11148689/"
params = {"type": "json"}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
def newuser(name:str,phone:str,password:str):
    url="https://v4pre.h5sys.cn/api/11148689/newuesr"
    params={"name":name,"phone":phone,"password":password}
    re=requests.get(url,params).json()["return"]
    if(re=="okey"):
        return re
    else:
        return re
def getscore(name:str,clas:str,score:str):
    url="https://v4pre.h5sys.cn/api/11148689/getscore"
    params={"name":name,"class":clas,"score":score}
    re=requests.get(url,params).json()["return"]
    return re