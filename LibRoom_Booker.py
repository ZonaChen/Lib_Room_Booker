import requests
import random
import datetime
import time
import json

startTime="2000"
endTime="2200"
current_hourseId=5
run_flag=0
while 1:
    if run_flag==0:
        sleep(1)
        if (datetime.datetime.now().hour==20 and datetime.datetime.now().minute==58):
            run_flag=1
    else:
        while 1:

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
                [429,3676580]
            ]

            #date data
            dateTime=(datetime.datetime.now()+datetime.timedelta(days=2))
            date= dateTime.date()

            #login data
            id='xxxxxxxxxxx'
            pwd='xxxxxx'
            loginurl='http://202.120.82.2:8081/ClientWeb/pro/ajax/login.aspx'
            loginparams={'id':id,'pwd':pwd,'act':'login'}

            strStartTime=startTime[0:2]+'%3A'+startTime[2:4]
            strEndTime=endTime[0:2]+'%3A'+endTime[2:4]

            #login and post book room request
            s=requests.Session()
            r=s.post(loginurl,data=loginparams)
            data = json.loads(r.content.decode("utf-8") )
            print(data['msg'])
            houseUrl='http://202.120.82.2:8081/ClientWeb/pro/ajax/reserve.aspx?'+\
                     'dev_id='+str(houseId[current_hourseId][1])+\
                     '&lab_id='+'3674920'+\
                     '&kind_id='+'3675133'+\
                     '&room_id=&type=dev&prop=&test_id=&term=&test_name=' \
                     '&start='+str(date)+'+'+strStartTime+ \
                     '&end='+str(date)+'+'+strEndTime+ \
                     '&start_time='+startTime+ \
                     '&end_time='+endTime+ \
                     '&up_file=&memo=&act=set_resv&_=1506498206412'
            r=s.post(houseUrl)
            data = json.loads(r.content.decode("utf-8") )
            if(data['msg'][0:1]=='操'):
                print(data['msg'])
            num=0
            while(data['msg'][0:1]!='操' and num<1000):
                print(2)
                if(data['msg'][10:11]=='预'):
                    print(data['msg'])
                    print('已经被人订了')
                    break
                r = s.post(houseUrl)
                data = json.loads(r.content.decode("utf-8") )
                num=num+1
                time.sleep(0.3)
            if(data['msg'][0:1]!='2'):
                print(startTime)
                print(endTime)
                ini = int((startTime[0]) + (startTime[1]))
                endTime = str(ini)+"00"
                ini -= 4
                if ini == 8:
                    startTime = "0810"
                elif ini<8:
                    exit(0)
                else:
                    startTime = str(ini) + "10"
            else:
                current_hourseId = int(random.uniform(1,9.99))