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
            [sg.Text("教师端密码"), sg.InputText()],
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
                if ev1[2]=="7890":
                    re = api.sign_in(phone=ev1[0], password=ev1[1])
                    if re["return"] == "okey":
                        Sign_in_windows.close()
                        if (conf["phone"] != ev1[0] and ev1[3] == True) or (conf["password"] != ev1[1] and ev1[3] == True):
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
                teacher_logon_verification=[
                    [sg.Text("教师端验证密码:")],
                    [sg.Button("确定")]
                ]
                teacher_logon_verification_windows = sg.Window("验证",teacher_logon_verification)
                while True:
                    ev0, ev1 = teacher_logon_verification_windows.read()
                    if ev0 == None:
                        if true_exit() == 1:
                            break
                    if ev0 == "确定":
                        if ev1[0] != "7890":
                            sg.popup("教师端验证密码错误,请重试")
                            continue
                        else:
                            break
                    else:
                        sg.popup("你小子开科技了？")
                        sys.exit()
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
def User_home():
