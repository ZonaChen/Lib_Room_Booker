import requests
import datetime
import time
import json


def getURL(houseId,current_hourseId,date,strStartTime,strEndTime,startTime,endTime):
    if current_hourseId<=9:
        p1='3675133'
        p2='1506498206412'
    else:
        p1='3674969'
        p2='1530545902099'
    return  'http://202.120.82.2:8081/ClientWeb/pro/ajax/reserve.aspx?'+\
            'dev_id=' + str(houseId[current_hourseId][1]) + \
            '&lab_id=' + '3674920' + \
            '&kind_id=' + p1 + \
            '&room_id=&type=dev&prop=&test_id=&term=&test_name=' \
            '&start=' + str(date) + '+' + strStartTime + \
            '&end=' + str(date) + '+' + strEndTime + \
            '&start_time=' + startTime + \
            '&end_time=' + endTime + \
            '&up_file=&memo=&act=set_resv&_='+p2


startTime="1800"
endTime="2200"
#currcurrent_hourseId=5
run_flag=0
#house data
houseId=[
    [000,0000000],
    [421,3676503],
    [422,3676511],
    [423,3676515],
    [424,3676522],
    [425,3676538],
    [426,3676547],
    [427,3676566],
    [428,3676574],
    [429,3676580],
    [411, 3676604],
    [412, 3676641],
    [413, 3676645],
    [414, 3676656],
    [415, 3676664],
]

#date data
dateTime=(datetime.datetime.now()+datetime.timedelta(days=2))
date= dateTime.date()

#login data
id='xxx'
pwd='xxx'
loginurl='http://202.120.82.2:8081/ClientWeb/pro/ajax/login.aspx'
loginparams={'id':id,'pwd':pwd,'act':'login'}
strStartTime=startTime[0:2]+'%3A'+startTime[2:4]
strEndTime=endTime[0:2]+'%3A'+endTime[2:4]
#login and post book room request
s=requests.Session()
r=s.post(loginurl,data=loginparams)
checkflag=1
# data = json.loads(r.content.decode("utf-8") )

while 1:
    if run_flag==0:
        if (datetime.datetime.now().hour==20 and datetime.datetime.now().minute==58):
            run_flag=1
        else:
            time.sleep(1)
            print("未到程序准备预订时间")
    else:
        while 1:
            while checkflag:
                houseUrl = getURL(houseId, 1, date, strStartTime, strEndTime, startTime, endTime)
                r = s.post(houseUrl)
                data = json.loads(r.content.decode("utf-8"))
                if data['msg'][10:11] != '要':
                    checkflag=0
                    break
                time.sleep(0.5)
                print("未到服务器可预订时间")

            for i in range(1,15):
                houseUrl = getURL(houseId, i, date, strStartTime, strEndTime, startTime, endTime)
                r = s.post(houseUrl)
                data = json.loads(r.content.decode("utf-8"))
                if data['msg'][0:1]=='操':
                    break
                else:
                    print(str(houseId[i][0])+"已经被预订")
                time.sleep(0.3)

            if (data['msg'][0:1] != '2'):
                print(startTime)
                print(endTime)
                print("预订成功")

            ini = int((startTime[0]) + (startTime[1]))
            endTime = str(ini) + "00"
            ini -= 4
            if ini == 8:
                startTime = "0810"
            elif ini < 8:
                exit(0)
            else:
                startTime = str(ini) + "10"
            print("尝试下一次预订")
            print(startTime)
            print(endTime)


            # else:
            #     current_hourseId = int(random.uniform(1,9.99))  # 今天需要去抢哪一间房
        # http://202.120.82.2:8081/ClientWeb/pro/ajax/reserve.aspx?dev_id=3676515&lab_id=3674920&kind_id=3675133&room_id=&type=dev&prop=&test_id=&term=&test_name=&start=2018-07-03+08%3A10&end=2018-07-03+08%3A40&start_time=810&end_time=840&up_file=&memo=&act=set_resv&_=1530546115012
        # http://202.120.82.2:8081/ClientWeb/pro/ajax/reserve.aspx?dev_id=3676645&lab_id=3674920&kind_id=3674969&room_id=&type=dev&prop=&test_id=&term=&test_name=&start=2018-07-04+08%3A00&end=2018-07-04+09%3A00&start_time=800&end_time=900&up_file=&memo=&act=set_resv&_=1530545902099
