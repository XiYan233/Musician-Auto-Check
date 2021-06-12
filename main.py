import configparser
import os
import requests

#读取配置文件
root_dir = os.path.abspath(os.curdir)
configpath = os.path.join(root_dir, "config.ini")
cf = configparser.ConfigParser()
cf.read(configpath,encoding='utf-8')

#读取API接口
api = cf.get("setting","api")

#读取md5选项
md5 = cf.get("setting","md5")

#读取手机号码
phone = cf.get("setting","phone")

#读取密码
password = cf.get("setting","password")

#登录
def login():

    if(md5 == "true"):
        login = requests.get(api + "/login/cellphone?phone=" + phone + "&md5_password=" + password)
    login = requests.get(api + "/login/cellphone?phone=" + phone + "&password=" + password)

    #返回cookie
    if login.status_code == 200:
        print("登录成功！")
        return login.cookies


login_cookie = login()
print(login_cookie)

