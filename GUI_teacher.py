import confing
import PySimpleGUI as sg
import sys
import api
from pandas import DataFrame
import xlsxwriter
conf=confing.ID()
put_in = [  [sg.Text('手机号：'),sg.InputText(conf['phone'])],
            [sg.Text('密码：'),sg.InputText(conf['password'])],
            [sg.Text("教师端密码"),sg.InputText()],
            [sg.Button('登录'), sg.Button('注册')] ]
sign_up=[
            [sg.Text("昵称："),sg.InputText()],
            [sg.Text('手机号：'),sg.InputText()],
            [sg.Text('密码：'),sg.InputText()],
            [sg.Text("客户端密码"),sg.InputText()],
            [ sg.Button('注册并登录')] ]
user_home=[
            [sg.Button("下载全部学生数据"),sg.Button("获取留言")]]
putin = sg.Window('积分系统', put_in)
signup = sg.Window('注册', sign_up)
userhome = sg.Window("积分系统", user_home)
while True:
    event, values = putin.read()
    if event==None:
        sys.exit()
    if event=="登录":
        re=api.sign_up(phone=values[0],password=values[1])
        if re["return"]=="okey":
            if values[2]=="7890":
                putin.Hide()
            else:
                print("教师验证失败")
                continue
        else:
            print("账号或密码错误")
            continue
    if event=="注册":
        putin.Hide()
        event,values=signup.read()
        if event==None:
            sys.exit()
        if event=="注册并登录":
            re=api.newuser(name=values[0],phone=values[1],password=values[2])
            if re["return"]=="okey":
                if values[3]=="7890":
                    signup.Hide()
                else:
                    print("教师验证失败")
                    continue
            else:
                print("账号或密码错误")
                continue
    event,values=userhome.read()
    if event==None:
        sys.exit()
    if event=="下载全部学生数据":
        re=api.clone_score_teacher()
        z=0
        list_name={}
        list_Chinese={}
        list_Math={}
        list_English={}
        list_Physics={}
        list_Geography={}
        list_Biology={}
        for i in re["score"]:
            list_name[z]=i[0]           #姓名
            list_Chinese[z]=i[1]        #语文
            list_Math[z]=i[2]           #数学
            list_English[z]=i[3]        #英语
            list_Physics[z]=i[4]        #物理
            list_Biology[z] = i[6]      #生物
            list_Geography[z]=i[5]      #地理
            z = z+1
        del z
        print(list_name,list_Chinese,list_Math,list_English,list_Physics,list_Geography,list_Biology)
        data = {"姓名": list_name, "语文": list_Chinese, "数学": list_Math, "英语": list_English, "物理": list_Physics, "生物": list_Biology, "地理": list_Geography}
        df = DataFrame(data)
        df.to_excel('new.xlsx')
    #if event=="获取留言":
