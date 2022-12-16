import confing
import PySimpleGUI as sg
import sys
import api
conf=confing.ID()
print(conf)
name="0"
score_class="0"
score="0"
sg.theme('Default1')   # 设置当前主题
# 界面布局，将会按照列表顺序从上往下依次排列，二级列表中，从左往右依此排列
put_in = [  #[sg.Text('积分表路径:'), sg.InputText('')],
            [sg.Text('手机号：'),sg.InputText(conf['phone'])],
            [sg.Text('密码：'),sg.InputText(conf['password'])],
            #[sg.Text('计算内容：'),sg.Combo (['自动      ','最高分(组)','最低分(组)','最高分(班)','最低分(班)']),sg.Text('模式：'),sg.Combo(['普通   ','快速(beta)',],text_color='red')],
            [sg.Button('登录'), sg.Button('注册')] ]
sign_up=[
            [sg.Text("昵称："),sg.InputText()],
            [sg.Text('手机号：'),sg.InputText()],
            [sg.Text('密码：'),sg.InputText()],
            [ sg.Button('注册并登录')] ]
user_home=[
            [sg.Button("积分提交"),sg.Button("积分查询")],
            [sg.Button("留言")] ]
get_score=[
            [sg.Text("科目: "),sg.Combo(['语文','数学','英语','物理','生物','地理'])],
            [sg.Text("分数: "),sg.InputText()],
            [sg.Button("提交")]]
clone_score=[
             [sg.Text("姓名："),sg.InputText()],
             [sg.Text("科目："),sg.Combo(['语文','数学','英语','物理','生物','地理'])],
             [sg.Button("查询")] ]
leave_massage=[
                [sg.Text("你想留言给谁"),sg.Combo(['语文老师','数学老师','英语老师','物理老师','生物老师','地理老师'])],
                [sg.Text("你想说什么，直接写下来"),sg.InputText()],
                [sg.CBox('是否匿名', size=(10, 1),default=True)],
                [sg.Button("提交")]]
# 创造窗口
putin = sg.Window('积分系统', put_in)
signup = sg.Window('注册', sign_up)
userhome = sg.Window("积分系统", user_home)
getscore=sg.Window("积分提交",get_score)
clonescore=sg.Window("积分查询",clone_score)
leavemassage=sg.Window("留言",leave_massage)
#初始化窗口并隐藏
# 事件循环并获取输入值
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
while True:
    event, values = putin.read()
    if event in (None, 'Cancel'):   # 如果用户关闭窗口或点击`Cancel`
        putin.close()
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
    if event=="留言":
        userhome.Hide()
        event,values=leavemassage.read()
        if event=="提交":
            re=api.leave_massage(name=name,object=values[0],text=values[1],anonymous=values[2])
            if re["return"]=="okey":
                leavemassage.Hide()
                sg.popup_yes_no("提交成功", modal=True, keep_on_top=False,grab_anywhere=False)