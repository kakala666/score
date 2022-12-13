from configparser import ConfigParser
import os
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
        cf.write(open(id_path, "a"))
        print("配置文件成功释放，请填写ID.ini,并重启程序")
        sys.exit()
    else:
        cf.read(id_path)  # 读取配置文件
        conf['webhook'] = cf.get("dingtalk", "webhook")
        conf['secret'] = cf.get("dingtalk", "secret")
        conf["phone"]=cf.get("path","phone")
        conf["password"]=cf.get("path","password")
        #conf['ding_talk_body'] = cf.get("texttalk", "body")
        #conf['talk_sleep_time'] = int(cf.get("texttalk", "sleep_time"))
        return conf
if __name__=='__main__':
    print(ID())