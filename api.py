from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder

import pymysql
from pymysql.cursors import DictCursor
import time    
import datetime
from config import *

app = FastAPI()

@app.get('/')
def index():
    return 'hello!!'

#user-----
Prefix = "user"
@app.get('/'+Prefix+'_list')
def read_users():
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor(DictCursor)
        command = "SELECT * FROM user"
  
        cursor.execute(command)

        result = cursor.fetchall()
        response = {"success":1}
        response["data"] = result
        conn.close()
        return response
    except Exception as ex:
        print(ex)

@app.get('/'+Prefix+'/{id}')
def read_user(id:str):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor(DictCursor)
        command = "SELECT * FROM user WHERE uId = '{}'".format(id)
        cursor.execute(command)
        result = cursor.fetchall()

        #建立return 的資料結構
        response = {"success":1}
        response["data"] = result
        conn.close()
        return response
    except Exception as ex:
        print(ex)

@app.post('/'+Prefix)
async def create_user(request: Request):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor() 
        
        _json = await  request.json()
       
        uId = _json["uId"]
        status = _json["status"]
        print(_json)
        command = "INSERT INTO `user`(`uId`, `status`) VALUES ('{}','{}')"
        command = command.format(uId, status)
        
        cursor.execute(command)
        
        #commit 到mysql 關閉連線
        conn.commit()
        conn.close()
        #建立return 的資料結構
        response = {"success":1}
        return response
    except Exception as ex:
        print(ex)

@app.put('/'+Prefix)
async def update_user(request: Request):
    try:
       
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor() 
        #print(request)
        
        _json = await request.json()

        uId = _json["uId"]
        status = _json["status"]
        
        command = "UPDATE `user` SET `status`='{}' WHERE uId = '{}'"
        command = command.format(status, uId)
        cursor.execute(command)
        conn.commit()
        #return the result after update
        cursor = conn.cursor(DictCursor)      
        command = "SELECT * FROM user WHERE uId = '{}'".format(uId)
        cursor.execute(command)
        result = cursor.fetchall()
        #建立return 的資料結構
        response = {"success":1}
        response["data"] = result
        
        conn.close()
        return response

    except Exception as ex:
        print(ex)

@app.delete('/'+Prefix+'/{id}')
def delete_user(id: str):
    try:
       
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor() 
        
        command = "DELETE FROM `user` WHERE `uId` = '{}'"
        command = command.format(id)
        
        cursor.execute(command)
        
        conn.commit()
        conn.close()

        response = {"success":1}
        return response
    except Exception as ex:
        print(ex)

#form-----
Prefix = "form"
@app.get('/'+Prefix)
def read_form():
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor(DictCursor)

        #get max fId
        command = "SELECT MAX(fId) AS fId FROM form"
        cursor.execute(command)
        result = cursor.fetchone()
        id = result["fId"]


        #get the info of form & who is the host
        command = "SELECT * FROM form WHERE fId = '{}'".format(id)
        cursor.execute(command)
        result = cursor.fetchone()
        hostId = result["hostId"]
        
        #get the summation
        command = "SELECT SUM(amount) AS summation FROM user_form WHERE formId = '{}'".format(id)
        cursor.execute(command)
        result = cursor.fetchone()
        summation = result["summation"]

        #get the info of who order what
        command = "SELECT * FROM user_form WHERE formId = '{}'".format(id)
        cursor.execute(command)
        result = cursor.fetchall()

        #建立return 的資料結構
        response = {"success":1}
        response["hostId"] = hostId
        response["total_price"] = summation
        response["data"] = result
        
        conn.close()
        return response
    except Exception as ex:
        print(ex)

@app.post('/'+Prefix)
async def create_form(request: Request):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor() 
        
        _json = await request.json()
       
        hostId = _json["hostId"]
        
        command = "INSERT INTO `form`(`hostId`) VALUES ('{}')"
        command = command.format(hostId)
        cursor.execute(command)
        conn.commit()

        cursor = conn.cursor(DictCursor)
        command = "SELECT MAX(fId) AS `fId` FROM `form`"
        cursor.execute(command)
        result = cursor.fetchone() 
        response = {"success":1}
        conn.close()
        #建立return 的資料結構
        
        return response
    except Exception as ex:
        print(ex)


@app.delete('/'+Prefix+'/{id}')
def delete_form(id: str):
    try:
       
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor() 
        
        command = "DELETE FROM `form` WHERE `fId` = '{}'"
        command = command.format(id)
        
        cursor.execute(command)
        
        conn.commit()
        conn.close()

        response = {"success":1}
        return response
    except Exception as ex:
        print(ex)

#user_form-----
Prefix = "user_form"
@app.post('/'+Prefix)
async def create_user_form(request: Request):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor() 
        
        _json = await  request.json()
       
        clientId = _json["clientId"]

        food = _json["food"]
        num = _json["num"]
        amount = _json["amount"]
        remark = _json["remark"]

        #get formId
        command = "SELECT MAX(`fId`) FROM `form`"
        cursor.execute(command)
        result = cursor.fetchone()
        print(result)
        fId = result[0]
        

        command = "INSERT INTO `user_form`(`clientId`, `formId`, `food`, `num`, `amount`, `remark`) VALUES ('{}','{}','{}','{}','{}','{}')"
        command = command.format(clientId, fId, food, num, amount, remark)
        
        cursor.execute(command)
        
        #commit 到mysql 關閉連線
        conn.commit()
        conn.close()
        #建立return 的資料結構
        response = {"success":1, "command":command}
        return response
    except Exception as ex:
        print(ex)

@app.put('/'+Prefix)
async def update_user_form(request: Request):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor() 
        
        _json = await request.json()
       
        clientId = _json["clientId"]
        formId = _json["formId"]
        food = _json["food"]
        num = _json["num"]
        amount = _json["amount"]
        remark = _json["remark"]
        
        command = "UPDATE `user_form` SET `food` = '{}', `num` = '{}', `amount` = '{}', `remark` = '{}' WHERE `clientId` = '{}' AND `formId` = {}"
        
        command = command.format(food, num, amount, remark, clientId, formId)
        cursor.execute(command)
        conn.commit()
        
        #return the result after update
        #建立return 的資料結構
        response = {"success":1,}
        
        conn.close()
        return response

    except Exception as ex:
        print(ex)

# meeting
Prefix = "meeting"
@app.get('/'+Prefix+"/{uId}")
async def read_meeting_i_host(uId: str):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor(DictCursor)
        
        #command = "SELECT * FROM `meeting`,`choose` WHERE `meeting`.`mId` = `choose`.`mId` AND `meeting`.`hostId`='{}' and `s_time` > now()".format(uId)
        command = "SELECT * FROM `meeting` WHERE `meeting`.`hostId`='{}' and `s_time` > now()".format(uId)
        cursor.execute(command)
        result = cursor.fetchall()

        #建立return 的資料結構
        response = {"success":1}
        response["data"] = result
        response["command"] = command
        conn.close()
        return response
    except Exception as ex:
        print(ex)
        

@app.post('/'+Prefix)
async def create_meeting(request: Request):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor(DictCursor)

        _json = await request.json()
       
        s_time = _json["s_time"]
        location = _json["location"]
        content = _json["content"]
        hostId = _json["hostId"]
        attendee = _json["attendee"]

        print("create meeting")
        print(_json)
        #create meeting
        command = "INSERT INTO `meeting`(`s_time`, `location`, `content`, `hostId`) VALUES ('{}','{}','{}','{}')"
        command = command.format(s_time, location, content, hostId)
        cursor.execute(command)
        conn.commit()
        print("Create meeting")
        print(command)
        #get mId
        command = "SELECT MAX(`mId`) AS max_mId FROM `meeting`"
        cursor.execute(command)
        result = cursor.fetchone()
        mId = result["max_mId"]
        
        print(attendee)
        print(type(attendee))

        attendee = attendee.split(",")
        for at in attendee:
            at = at[2:-1]
            command = "INSERT INTO `choose`(`uId`, `mId`, `choose`, `reason`) VALUES ('{}','{}','{}','{}')"
            command = command.format(at, mId, "reject", "")
            cursor.execute(command)
            conn.commit()
        print("Create choose")
        print(command)

        #建立return 的資料結構
        response = {"success":1}
        #response["command"] = command
        #response["data"] = attendee
        #response["data"] = result
        conn.close()
        return response
    except Exception as ex:
        print(ex)

# choose----
Prefix = "choose"
@app.get('/'+Prefix+'/{uId}')
async def read_choose_i_host_meeting(uId:str):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor(DictCursor)
       
        command = "SELECT MAX(`mId`) AS max_mId FROM `meeting`"
        cursor.execute(command)
        result = cursor.fetchone()
        mId = result["max_mId"]
        command = "SELECT * FROM `meeting`,`choose` WHERE `meeting`.`mId` = `choose`.`mId` AND `meeting`.`mId` ={} AND `meeting`.`hostId`='{}'".format(mId,uId)
        print(command)
        cursor.execute(command)
        result = cursor.fetchall()

        #建立return 的資料結構
        response = {"success":1}
        response["data"] = result
        response["command"] = command
        conn.close()
        return response
    except Exception as ex:
        print(ex)

@app.put('/'+Prefix)
async def update_choose(request: Request):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor(DictCursor)

        _json = await request.json()
       
        uId = _json["uId"]
        command = "SELECT MAX(`mId`) AS max_mId FROM `meeting`"
        cursor.execute(command)
        result = cursor.fetchone()
        mId = result["max_mId"]
        choose = _json["choose"]
        reason = _json["reason"]
        #update the choose
        command = "UPDATE `choose` SET `choose` = '{}', `reason` = '{}' WHERE `uId` = '{}' AND `mId` = {}"
        
        command = command.format(choose, reason, uId, mId)
        cursor.execute(command)
        conn.commit()
        

        #建立return 的資料結構
        response = {"success":1}
        conn.close()
        return response
    except Exception as ex:
        print(ex)




# tag--------
#3個
Prefix = "tag"

@app.get('/'+Prefix)
def read_tag_list():
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor(DictCursor)
        command = "SELECT * FROM tag WHERE reply = '0'"
  
        cursor.execute(command)

        result = cursor.fetchall()
        response = {"success":1}
        response["data"] = result
        conn.close()
        return response
    except Exception as ex:
        print(ex)


@app.get('/'+Prefix+"/{uId}")
def read_tag(uId: str):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor(DictCursor)
        command = "SELECT * FROM tag WHERE clientId = {} and reply = '0' ".format(uId)
  
        cursor.execute(command)

        result = cursor.fetchall()
        response = {"success":1}
        response["data"] = result
        conn.close()
        return response
    except Exception as ex:
        print(ex)

@app.post('/'+Prefix)
async def create_tag(request: Request):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor(DictCursor)
        _json = await request.json()

        hostId = _json["hostId"]
        clientIdList = _json["clientId"]
        content = _json["content"]
        
        for clientId in clientIdList:
            command = "INSERT INTO `tag`(`hostId`, `clientId`,`content`, `reply`) VALUES ('{}','{}','{}','{}')"
            command = command.format(hostId, clientId,content , '0')
            cursor.execute(command)
            conn.commit()
        
 

        response = {"success":1}
        conn.close()
        return response
    except Exception as ex:
        print(ex)

@app.put('/'+Prefix)
async def update_tag(request: Request):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor(DictCursor)
        _json = await request.json()

        msgId = _json["msgId"]

        command = "UPDATE `tag` SET `reply` = 1 WHERE  `msgId` = '{}'"
        command = command.format(msgId)
        cursor.execute(command)
        #print(command)
        conn.commit()

        command = "SELECT * FROM tag WHERE msgId = {}".format(msgId)
        cursor.execute(command)
        result = cursor.fetchall()
        response = {"success":1,"data":result}
        conn.close()
        return response
    except Exception as ex:
        print(ex)
    

#job 
#3個
Prefix = "job"
@app.get('/'+Prefix+"/{uId}")
async def read_job(uId: str):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor(DictCursor)
        
        command = "SELECT * FROM `jobs` WHERE `clientId`='{}' and status!='confirmed' and status!='done'".format(uId)#問題
        cursor.execute(command)
        result = cursor.fetchall()

        #建立return 的資料結構
        response = {"success":1}
        response["data"] = result
        response["command"] = command
        conn.close()
        return response
    except Exception as ex:
        print(ex)

@app.post('/'+Prefix)
async def create_job(request: Request):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor(DictCursor)

        _json = await request.json()
        
        deadline = _json["deadline"]
        content = _json["content"]
        hostId = _json["hostId"]
        clientIdList = _json["clientId"]

        deadline = datetime.datetime.fromtimestamp(int(deadline)/1000.0)

        for clientId in clientIdList:
            timestr = time.strftime('%Y-%m-%d %H:%M:%S')
            command = "INSERT INTO `jobs`(`s_time`, `deadline`, `pre_time`, `content`, `status`, `hostId`, `clientId`) VALUES ('{}','{}','{}','{}','{}','{}','{}')"
            command = command.format(timestr, deadline, timestr, content, "undo", hostId, clientId)
            cursor.execute(command)
            conn.commit()
        conn.close()
        print(deadline)
        return {"success":1}
    except Exception as ex:
        print(ex)

@app.put('/'+Prefix)
async def update_job(request: Request):
    try:
        conn = pymysql.connect(**db_settings)
        cursor = conn.cursor(DictCursor)

        _json = await request.json()
        
        jId = _json["jId"]
        status = _json["status"]
        timestr = time.strftime('%Y-%m-%d %H:%M:%S')
        command = "UPDATE `jobs` SET `status` = '{}', `pre_time` = '{}' WHERE `jId` = '{}'"
        command = command.format(status, timestr, jId)
        print(command)
        cursor.execute(command)
        conn.commit()

        #get hostid
        command = "SELECT * FROM `jobs` WHERE `jId`='{}'".format(jId)
        cursor.execute(command)
        print(command)
        result = cursor.fetchone()
        hostId = result['hostId']
        clientId = result['clientId']
        content = result['content']

        conn.close()
        return {"success":1,"hostId":hostId,"clientId":clientId,"content":content}
    except Exception as ex:
        print(ex)
