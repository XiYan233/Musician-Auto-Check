import configparser
import os
import requests
import json

#读取配置文件
root_dir = os.path.abspath(os.curdir)
configpath = os.path.join(root_dir, "config.ini")
config = configparser.ConfigParser()
config.read(configpath,encoding='utf-8')

#读取API接口
api = config.get("setting","api")

#读取md5选项
md5 = config.get("setting","md5")

#读取手机号码
phone = config.get("setting","phone")

#读取密码
password = config.get("setting","password")

#读取推送机器人开关
pushswitch = config.get("setting","pushswitch")

#读取企业微信机器人Key
robot_key = config.get("setting","robotkey")

#登录
def login():

    global loginlog

    if md5 == "true":
        login = requests.get(api + "/login/cellphone?phone=" + phone + "&md5_password=" + password)
    elif md5 == "false":
        login = requests.get(api + "/login/cellphone?phone=" + phone + "&password=" + password)

    #返回cookie
    if login.status_code == 200:
        print("登录成功！")
        loginlog = '>' + '登陆成功！'
        return login.cookies


login_cookie = login()
#print(login_cookie)

#签到
def check():

    global checklog

    check = requests.get(api + "/musician/sign",cookies=login_cookie)
    if check.status_code == 200:
        print("登录音乐人中心完成！")
        checklog = '>' + '登录音乐人中心完成！'

check()

#获取任务userMissionId和period
def get_task():

    global userMissionId
    global userMissionId1
    global userMissionId2
    global userMissionId3
    global period
    global period1
    global period2
    global period3
    global get_task_log

    get_task = requests.get(api + "/musician/tasks",cookies=login_cookie)

    if get_task.status_code == 200:
        
        task_json = get_task.json()
        #print(jsonstr)

        json_array = json.loads(json.dumps(json.loads(json.dumps(task_json))['data']['list']))[8]
        json_array1 = json.loads(json.dumps(json.loads(json.dumps(task_json))['data']['list']))[9]
        json_array2 = json.loads(json.dumps(json.loads(json.dumps(task_json))['data']['list']))[10]
        json_array3 = json.loads(json.dumps(json.loads(json.dumps(task_json))['data']['list']))[12]
        #print(json_array)
        userMissionId = str(json_array['userMissionId'])
        userMissionId1 = str(json_array1['userMissionId'])
        userMissionId2 = str(json_array2['userMissionId'])
        userMissionId3 = str(json_array3['userMissionId'])
        print("获取missionId成功！")
        get_task_log = '>' + '获取missionId成功！\n'

        period = str(json_array['period'])
        period1 = str(json_array1['period'])
        period2 = str(json_array2['period'])
        period3 = str(json_array3['period'])
        print("获取period成功！")
        get_task_log += '>' + '获取period成功！'

get_task()

#领取登录音乐人中心云豆
def receiveCheck():

    global checklog

    check = requests.get(api + "/musician/cloudbean/obtain?id=" + userMissionId + "&period=" + period,cookies=login_cookie)
    check1 = requests.get(api + "/musician/cloudbean/obtain?id=" + userMissionId1 + "&period=" + period1,cookies=login_cookie)
    check2 = requests.get(api + "/musician/cloudbean/obtain?id=" + userMissionId2 + "&period=" + period2,cookies=login_cookie)
    check3 = requests.get(api + "/musician/cloudbean/obtain?id=" + userMissionId3 + "&period=" + period3,cookies=login_cookie)
    if check.status_code == 200:
        print("领取登录音乐人中心云豆成功！")
        checklog = '>' + '领取登录音乐人中心云豆成功！\n ' + '>' + '领取里程碑奖励成功！'

receiveCheck()



#获取账户云豆数
def userinfo():
    userinfo = requests.get(api + "/musician/cloudbean",cookies=login_cookie)
    if userinfo.status_code == 200:
        userinfo_json = userinfo.json()
        print("目前账户云豆：" + str(userinfo_json['data']['cloudBean']) + "个")
        return str(userinfo_json['data']['cloudBean'])

userinfo = userinfo()


#企业微信机器人推送

def push():
    if pushswitch == "true":
        headers = {"Content-Type": "text/plain"}
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": "<font color=\"warning\">网易音乐人签到通知</font>\n" + '> 当前云豆总数：' + "<font color=\"warning\">" + userinfo + "</font>个" + '\n ' + '\n 运行日志：\n' + loginlog + '\n' + get_task_log + '\n' + checklog
            }
        }
        push = requests.post(url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + robot_key, headers=headers, json=data)
        data = json.loads(push.text)
        print(push.text)
        if data['errmsg'] == 'ok':
            print('企业微信机器人推送成功')
        else:
            print('企业微信机器人推送失败,请检查key是否正确')
    else:
        print("未开启企业机器人推送")

push()
