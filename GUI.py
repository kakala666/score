import confing,api
import PySimpleGUI as sg
import sys
import webbrowser as web
conf=confing.ID()
print(conf)
name="NULL"
score_class="0"
score="0"
sg.theme('Default1')   # 设置当前主题
'''
# 界面布局，将会按照列表顺序从上往下依次排列，二级列表中，从左往右依此排列
Sign_in = [  #[sg.Text('积分表路径:'), sg.InputText('')],
            [sg.Text('手机号：'),sg.InputText(conf['phone'])],
            [sg.Text('密码：'),sg.InputText(conf['password'])],
            #[sg.Text('计算内容：'),sg.Combo (['自动      ','最高分(组)','最低分(组)','最高分(班)','最低分(班)']),sg.Text('模式：'),sg.Combo(['普通   ','快速(beta)',],text_color='red')],
            [sg.Button('登录'), sg.Button('注册')] ]
logon=[
            [sg.Text("昵称："),sg.InputText()],
            [sg.Text('手机号：'),sg.InputText()],
            [sg.Text('密码：'),sg.InputText()],
            [ sg.Button('注册并登录')] ]
userhome=[
            [sg.Button("积分提交"),sg.Button("积分查询")],
            [sg.Button("举报"),sg.Button("留言")] ]
getscore=[
            [sg.Text("科目: "),sg.Combo(['语文','数学','英语','物理','生物','地理'])],
            [sg.Text("分数: "),sg.InputText()],
            [sg.Button("提交"),sg.Button("返回")]]
clonescore=[
             [sg.Text("姓名："),sg.InputText()],
             [sg.Text("科目："),sg.Combo(['语文','数学','英语','物理','生物','地理'])],
             [sg.Button("查询"),sg.Button("返回")] ]
leavemassage=[
                [sg.Text("你想留言给谁"),sg.Combo(['语文老师','数学老师','英语老师','物理老师','生物老师','地理老师'])],
                [sg.Text("你想说什么，直接写下来"),sg.InputText()],
                [sg.CBox('是否匿名', size=(10, 1),default=True)],
                [sg.Button("提交"),sg.Button("返回")]]
report_windows=[
         [sg.Text("我要举报"),sg.InputText()],
         [sg.Text("填写举报内容"),sg.InputText(size=(40,20))],
         [sg.Button("举报")] ]
'''
# 事件循环并获取输入值
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
Activity="NULL"
def true_exit():
    exit = [
        [sg.Text("你确定要退出吗")],
        [sg.Button("退出"), sg.Button("取消")]
    ]
    Exit = sg.Window("", exit)
    ev0, ev1 = Exit.read()
    if ev0 == "退出":
        sys.exit()
    elif ev0 == "取消":
        Exit.close()
        return 1;
def Sign_in():
    while True:
        sign_in = [
            [sg.Text('手机号：'), sg.InputText(conf['phone'])],
            [sg.Text('密码：'), sg.InputText(conf['password'])],
            [sg.CBox('记住密码', size=(10, 1), default=True)],
            [sg.Button('登录'), sg.Button('注册')]
        ]
        Sign_in_windows=sg.Window("积分系统",sign_in,finalize=False)
        while True:
            ev0, ev1 = Sign_in_windows.read()
            if ev0 == None:
                if true_exit() == 1:
                    continue
            elif ev0 == "登录":
                re = api.sign_in(phone=ev1[0], password=ev1[1])
                if re["return"] == "okey":
                    Sign_in_windows.close()
                    if (conf["phone"] != ev1[0] and ev1[2] == True) or (conf["password"] != ev1[1] and ev1[2] == True):
                        confing.updata_conf(["path", "phone"], ev1[0])
                        confing.updata_conf(["path", "password"], ev1[1])
                    return {"code": 1, "name": re["name"]}
                else:
                    sg.popup(re["return"], title="")
                    continue
            elif ev0 == "注册":
                Sign_in_windows.close()
                re = Log_on()
                if re["code"] == 1:
                    return re
                elif re["code"] == 2:
                    break
                else:
                    sg.popup("未知错误", title="")
                    sys.exit()
def Log_on():
    while True:
        logon = [
            [sg.Text("昵称："), sg.InputText()],
            [sg.Text('手机号：'), sg.InputText()],
            [sg.Text('密码：'), sg.InputText()],
            [sg.Button('注册并登录'), sg.Button("返回")]
        ]
        Log_on_windows = sg.Window("注册", logon,finalize=False)
        while True:
            ev0, ev1 = Log_on_windows.read()
            if ev0 == None:
                if true_exit() == 1:
                    break
            elif ev0 == "注册并登录":
                re = api.logon(name=ev1[0], phone=ev1[1], password=ev1[2])
                if re["return"] == "okey":
                    re = api.sign_in(phone=ev1[1], password=ev1[2])
                    if re["return"] == "okey":
                        confing.updata_conf(["path", "phone"], ev1[1])
                        confing.updata_conf(["path", "password"], ev1[2])
                        Log_on_windows.close()
                        return {"code": 1, "name": re["name"]}
                    else:
                        sg.popup(re["return"], title="")
                        continue
                else:
                    sg.popup(re["return"], title="")
                    continue
            elif ev0 == "返回":
                Log_on_windows.close()
                return {"code": 2}
def Get_score(name:str):
    while True:
        getscore = [
            [sg.Text("科目: "), sg.Combo(['语文', '数学', '英语', '物理', '生物', '地理'])],
            [sg.Text("分数: "), sg.InputText()],
            [sg.Button("提交"), sg.Button("返回")]
        ]
        Get_score_windows = sg.Window("积分提交", getscore)
        ev0, ev1 = Get_score_windows.read()
        if ev0 == None:
            if true_exit() == 1:
                continue
        elif ev0 == "提交":
            re=api.getscore(name=name,subject=ev1[0],score=ev1[1])
            if re["return"]=="okey":
                sg.popup("提交成功",title="")
                Get_score_windows.close()
                continue
            else:
                sg.popup(re["return"],title="")
                continue
        elif ev0 == "返回":
            Get_score_windows.close()
            return {"code":2}
def Clone_score(name):
    while True:
        clonescore = [
            [sg.Text("姓名："), sg.InputText()],
            [sg.Text("科目："), sg.Combo(['语文', '数学', '英语', '物理', '生物', '地理'])],
            [sg.Button("查询"), sg.Button("返回")]
        ]
        Clone_score_windows = sg.Window("积分查询", clonescore)
        while True:
            ev0, ev1 = Clone_score_windows.read()
            if ev0 == None:
                if true_exit() == 1:
                    break
            elif ev0 == "查询":
                re = api.clone_score(name=ev1[0], subject=ev1[1])
                if re["return"] == "okey":
                    sg.popup(ev1[0] + "在" + ev1[1] + "课上的分数为" + re["score"], title="")
                    continue
                else:
                    sg.popup("未知错误")
                    break
            elif ev0 == "返回":
                Clone_score_windows.close()
                return {"code": 2}
def Leave_massage(name):
    while True:
        leavemassage = [
            [sg.Text("留言给："), sg.Combo(['语文老师', '数学老师', '英语老师', '物理老师', '生物老师', '地理老师'])],
            [sg.Text("你想说什么，直接写下来"), sg.Multiline(size=(50,5))],
            [sg.CBox('是否匿名', size=(10, 1), default=True)],
            [sg.Button("提交"), sg.Button("返回")]]
        Leave_massage_windows = sg.Window("留言", leavemassage,size=(500,200))
        while True:
            ev0, ev1 = Leave_massage_windows.read()
            if ev0 == None:
                if true_exit() == 1:
                    break
            elif ev0 == "提交":
                re=api.leave_massage(name=name,object=ev1[0],text=ev1[1],anonymous=ev1[2])
                if re["return"]=="okey":
                    sg.popup("留言成功，"+ev1[0]+"会看到的",title="")
                    continue
                else:
                    sg.popup("留言失败，请重试")
                    continue
            elif ev0 == "返回":
                Leave_massage_windows.close()
                return {"code":2}
def Report(name):
    while True:
        report = [
                  [sg.Text("举报功能可以举报他人的所有不良行为")],
                  [sg.Text("我要举报(填被举报人姓名)"), sg.InputText()],
                  [sg.Text("填写举报内容（越细致越好）"), sg.Multiline(size=(50,5))],
                  [sg.Button("举报"),sg.Button("返回")]
                 ]
        Report_windows=sg.Window("举报",report,size=(500,200))
        while True:
            ev0, ev1 = Report_windows.read()
            if ev0 == None:
                if true_exit() == 1:
                    continue
            elif ev0 == "举报":
                re=api.report(object=ev1[0],text=ev1[1],name=name)
                if re["return"] == "okey":
                    sg.popup("举报成功",title="")
                    continue
                else:
                    sg.popup("举报失败",title="")
                    continue
            elif ev0 == "返回":
                Report_windows.close()
                return {"code":2}
def User_home(name):
    while True:
        userhome = [
                    [sg.Button("积分提交"), sg.Button("积分查询")],
                    [sg.Button("举报"), sg.Button("留言")]
                   ]
        User_home_windows=sg.Window("积分系统",userhome)
        ev0, ev1 = User_home_windows.read()
        if ev0 == None:
            if true_exit()==1:
                continue
        elif ev0 == "积分提交":
            User_home_windows.close()
            re=Get_score(name)
            if re["code"]==2:
                continue
        elif ev0 == "积分查询":
            User_home_windows.close()
            re=Clone_score(name)
            if re["code"] == 2:
                continue
        elif ev0 == "留言":
            User_home_windows.close()
            re=Leave_massage(name)
            if re["code"] == 2:
                continue
        elif ev0 == "举报":
            User_home_windows.close()
            re=Report(name)
            if re["code"]==2:
                continue
if __name__ == "__main__":
    re=api.updata(version_now=conf["version"])
    if re["return"] == "updata":
        updata=[
                [sg.Text("发现新版本")],
                [sg.Button("立即更新")]
               ]
        Updata=sg.Window("版本更新",updata)
        ev0, ev1 =Updata.read()
        if ev0 == None:
            sys.exit()
        elif ev0 == "立即更新":
            web.open(re["url"])
            sys.exit()
    re=Sign_in()
    if re["code"] == 1:
        name = re["name"]
        print("已登录账号：",name)
        User_home(name)


'''
def Sign_in():
    event, values = sign_in_windows.read()
    while True:
        if event==None:
            sys.exit(0)
        elif event=="登录":
            re=api.sign_in(values[0],values[1])
            if re["return"]=="okey":
                sign_in_windows.close()
                print("登录成功")
                return {"return":"okey","name":re["name"]}
            else:
                print("未知错误")
        elif event=="注册":
            sign_in_windows.close()
            re=Log_on()
            if re["return"]=="okey":
                sign_in_windows.close()
                print("登录成功")
                return {"return":"okey","name":re["name"]}
        else:
            print("未知错误", "event=", event)
            sys.exit(-1)
def Log_on():
    while True:
        event, values = log_on_windows.read()
        if event==None:
            sys.exit(0)
        elif event=="注册并登录":
            re=api.logon(name=values[0],phone=values[1],password=values[2])
            if re["return"]=="okey":
                print("注册成功")
                re=api.sign_in(phone=values[1],password=values[2])
                if re["return"]=="okey":
                    log_on_windows.Hide()
                    print("登录成功")
                    return {"return":"okey","name":re["name"]}
            else:
                print("未知错误", "event=", event)
                sys.exit(-1)
def User_home(name:str):
    user_home_windows = sg.Window("积分系统", userhome)
    event,values=user_home_windows.read()
    if event==None:
        sys.exit(0)
    elif event=="积分提交":
        user_home_windows.close()
        re=get_score(name)
        if re["code"]==2:
            if re["return"]=="user_home_windows":
                get_score_windows.close()
                User_home(name)
    elif event=="积分查询":
        user_home_windows.Hide()
        while True:
            event,values=clone_score_windows.read()
            if event==None:
                sys.exit(0)
            elif event=="查询":
                re=api.clone_score(name=values[0],clas=values[1])
                if re["return"]=="okey":
                    score = re["score"][0]
                    if values[1] == "语文":
                        i = 0
                    elif values[1] == "数学":
                        i = 1
                    elif values[1] == "英语":
                        i = 2
                    elif values[1] == "物理":
                        i = 3
                    elif values[1] == "生物":
                        i = 4
                    elif values[1] == "地理":
                        i = 5
                    sg.popup(values[0] + "在" + values[1] + "的分数为" + score[i], title="")
            elif event=="返回":
                return (2)
                #sg.popup("你敢信一个返回我做不出来？关掉重开吧", title="")
    elif event=="举报":
        user_home_windows.Hide()
        while True:
            event, values=report.read()
            if event==None:
                sys.exit(0)
            elif event=="举报":
                re=api.report(values[0],values[1],name)
                if re["return"]=="okey":
                    sg.popup("举报成功",title="")
                else:
                    sg.popup("未知错误",title="")
                    sys.exit(-1)
            else:
                sg.popup("未知错误",title="")
                sys.exit(-1)
    elif event=="留言":
        user_home_windows.Hide()
        while True:
            event,values=leave_massage_windows.read()
            if event==None:
                sys.exit(0)
            elif event=="提交":
                re=api.leave_massage(name=name,object=values[0],text=values[1],anonymous=values[2])
                if re["return"]=="okey":
                    sg.popup("留言成功",title="")
                else:
                    sg.popup("留言失败",title="")
            elif event=="返回":
                return {"return":2,"code":"leave_massage"}
            else:
                sg.popup("未知错误")
                sys.exit(-1)
                #sg.popup("你敢信一个返回我做不出来？关掉重开吧", title="")
def get_score(name:str):
    while True:
        event, values = get_score_windows.read()
        if event in (None,"返回"):
            return {"code": 2, "return": "user_home_windows"}
        elif event == "提交":
            re = api.getscore(name=name, clas=values[0], score=values[1])
            if re["return"]:
                sg.popup("提交成功", button_type=0, keep_on_top=True)
                get_score_windows.Hide()
                break
            else:
                sg.popup("未知错误", button_type=0, keep_on_top=True)
                break
sign_in_return=Sign_in()
if sign_in_return["return"]=="okey":
    name = sign_in_return["name"]
    del sign_in_return
    while True:
        user_home_return=User_home(name)
'''

'''
while True:
    event, values = putin.read()
    if event ==None:   # 如果用户关闭窗口或点击`Cancel`
        sys.exit()
    if event =="注册":
        putin.Hide()
        event, values = signup.read()
        if event == None:
            signup.close()
            sys.exit()
        if event == "注册并登录":
            re=api.newuser(name=values[0],phone=values[1],password=values[2])
            if re["return"] == "okey":
                re=api.sign_up(phone=values[1],password=values[2])
                if re["return"]=="okey":
                    confing.updata_conf(["path","phone"],values[1])
                    confing.updata_conf(["path","password"],values[2])
                    name=re["name"]
                    signup.Hide()
                    break
            else:
                print(re)
        break

    if event =="登录":
        re = api.sign_up(phone=values[0], password=values[1])
        if re["return"] == "okey":
            name = re["name"]
        if re["return"]=="okey":
            if values[0]!=conf["phone"]:
                confing.updata_conf(["path","phone"],values[0])
            if values[1]!=conf["password"]:
                confing.updata_conf(["path","password"],values[1])
            name=re["name"]
            putin.Hide()
            break
while True:
    event, values=userhome.read()
    if event == None:
        userhome.close()
        sys.exit()
        break
    if event == "积分提交":
        userhome.Hide()
        #getscore.UnHide()
        event,values=getscore.read()
        if event ==None:
            getscore.close()
            sys.exit()
            break
        if event=="提交":
            api.getscore(name=name,clas=values[0],score=values[1])
            getscore.Hide()
            userhome.UnHide()
    if event=="积分查询":
        userhome.Hide()
        event,values=clonescore.read()
        if event=="查询":
            re=api.clone_score(name=values[0],clas=values[1])
            if re["return"]=="okey":
                score=re["score"]
                score=score[0]
                clonescore.Hide()
                if values[1]=="语文":
                    i=0
                elif values[1]=="数学":
                    i=1
                elif values[1]=="英语":
                    i=2
                elif values[1]=="物理":
                    i=3
                elif values[1]=="生物":
                    i=4
                elif values[1]=="地理":
                    i=5
                sg.popup_yes_no(values[0]+"在"+values[1]+"的分数为"+score[i],modal=True,keep_on_top = False,grab_anywhere=False)
    if event=="举报":
        userhome.Hide()
        event,values=report.read()
        if event=="举报":
            re=api.report(object=values[0],text=values[1],name=name)
            if re["return"]=="okey":
                sg.popup_yes_no("举报成功", modal=True, keep_on_top=False,grab_anywhere=False)
    if event=="留言":
        userhome.Hide()
        event,values=leavemassage.read()
        if event=="提交":
            re=api.leave_massage(name=name,object=values[0],text=values[1],anonymous=values[2])
            if re["return"]=="okey":
                leavemassage.Hide()
                sg.popup_yes_no("提交成功", modal=True, keep_on_top=False,grab_anywhere=False)
    '''