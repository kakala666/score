from configparser import ConfigParser
import os
import PySimpleGUI as sg
import sys
def ID():
    conf={}
    cf = ConfigParser()
    id_path = os.path.join(os.getcwd(), "ID.ini")  # 获取当前目录并修改为配置文件目录
    # print(id_path)
    if not os.path.isfile(id_path):  # 若配置文件不存在
        file = open("ID.ini", 'w')
        file.close()
        cf.read(id_path)  # 读取配置文件
        cf.add_section("dingtalk")
        cf.add_section("path")
        cf.write(open(id_path, "a"))
        file=open("ID.ini",'w')
        file.close()
        cf.read(id_path)  # 读取配置文件
        cf.set("dingtalk", "webhook", "")
        cf.set("dingtalk", "secret", "")
        cf.add_section("texttalk")
        cf.set("texttalk","body","")
        cf.set("texttalk","sleep_time","")
        cf.set("path","phone","")
        cf.set("path","password","")
        cf.set("path", "version", "")
        cf.write(open(id_path, "a"))
        print("配置文件成功释放")
        sg.popup("你的配置文件被吃了？？，已重新释放配置文件，请重启程序")
        sys.exit()
    else:
        cf.read(id_path)  # 读取配置文件
        conf['webhook'] = cf.get("dingtalk", "webhook")
        conf['secret'] = cf.get("dingtalk", "secret")
        conf["phone"]=cf.get("path","phone")
        conf["password"]=cf.get("path","password")
        conf["version"]=cf.get("path","version")
        return conf
def updata_conf(conf:dict[str,str],body:str):
    cf = ConfigParser()
    id_path = os.path.join(os.getcwd(), "ID.ini")
    cf.read(id_path)
    cf.set(conf[0],conf[1],body)
    cf.write(open(id_path, "w"))
