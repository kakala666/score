import main,confing
import PySimpleGUI as sg
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, CardItem
import requests
conf=confing.ID()
import api
print(conf)
name="0"
sg.theme('Default1')   # 设置当前主题
# 界面布局，将会按照列表顺序从上往下依次排列，二级列表中，从左往右依此排列
putin = [  #[sg.Text('积分表路径:'), sg.InputText('')],
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

# 创造窗口
window = sg.Window('积分系统', putin)
# 事件循环并获取输入值
url = "https://api.vvhan.com/api/view"
params = {"type": "json"}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
def newpeople():
    window = sg.Window('注册', sign_up)
    url = "https://v4pre.h5sys.cn/api/11148689/newuesr"
    while True:
        event, values = window.read()
        if event == None:
            window.close()
            return -1
        if event == "注册并登录":
            re=api.newuser(name=values[0],phone=values[1],password=values[2])
            if re == "okey":
                window.close()
                break
            else:
                print(re)
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):   # 如果用户关闭窗口或点击`Cancel`
        window.close()
        break
    if event =="注册":
        window.close()
        if newpeople() == -1:
            break
        window.close()
        break
window = sg.Window("积分系统", user_home)
while True:
    event, values=window.read()
    if event == None:
        window.close()
        break
    if event == "积分提交":
        window.close()
        window=None
        window=sg.Window("积分提交",get_score)
        event,values=window.read()
        if event ==None:
            window.close()
            break
        if event=="提交":
            api.getscore(name=values)