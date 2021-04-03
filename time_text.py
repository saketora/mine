import statistics
import datetime

#make_time call_time spend_days send_who_catch send_hour_catch send_min_catch

def time_catch(data_line):
    list_day=["月","火","水","木","金","土","日"]
    if len(data_line)==14 and data_line[11] in list_day:
        return data_line.strip()
    else:
        return ""


def year_catch(data_line):
    year=time_catch(data_line)
    if year!="":
        return int(year[0:4])
    else:
        return ""

def month_catch(data_line):
    month=time_catch(data_line)
    if month!="":
        tmp=month[5:7]
        if tmp[0]=="0":
            month=tmp[1]
        else:
            month=tmp
        return int(month)
    else:
        return ""

def day_catch(data_line):
    day=time_catch(data_line)
    if day!="":
        tmp=day[8:10]
        if tmp[0]=="0":
            day=tmp[1]
        else:
            day=tmp
        return int(day)
    else:
        return ""

def send_hour_catch(data_line):
    tmp1=data_line.split("\t")
    if len(tmp1)==3:
        hour_min=tmp1[0]
        hour_str=hour_min[0:2]

        if hour_str[0]=="0":
            hour=hour_str[1]
        else:
            hour=hour_str

        return int(hour)
    else:
        return ""

def send_min_catch(data_line):
    tmp1=data_line.split("\t")
    if len(tmp1)==3:
        hour_min=tmp1[0]
        min_str=hour_min[3:5]
        if min_str[0]=="0":
            minuites=min_str[1]
        else:
            minuites=min_str
        return int(minuites)
    else:
        return ""

def send_who_catch(data_line):
    tmp1=data_line.split("\t")
    if len(tmp1)==3:
        return tmp1[1].strip()
    else:
        return ""


def isLeapYear(year,month):
    if month==2 and year%4==0 and (year%100!=0 or year%400==0):
        return 29
    else:
        return 28

def lastday_cal(year,month,day):
    month_judge_31=[1,3,5,7,8,10,12]
    month_judge_30=[4,6,9,11]

    if year!="" and month!="" and day!="":
        if month in month_judge_31:
            lastday=31
        elif month in month_judge_30:
            lastday=30
        elif month==2:
            lastday=isLeapYear(year,month)
        return lastday
    else:
        return ""

def make_time(data_line):
    year=year_catch(data_line)
    month=month_catch(data_line)
    day=day_catch(data_line)
    tmp=[year,month,day]
    if year!="" and month!="" and day!="":
        return tmp
    else:
        return ""


#day_list.append(str(year)+"/"+str(month)+"/"+str(day))

def make_1week_tmp(day_list):
    tmp_1week_list=[]
    tmp_day=day_list[-1]
    tmp_day_list=tmp_day.split("/")
    tmp_year=int(tmp_day_list[0])
    tmp_month=int(tmp_day_list[1])
    tmp_day=int(tmp_day_list[2])
    lastday=lastday_cal(tmp_year,tmp_month,tmp_day)
    flag=0
    for i in range(7):
        tmp_day+=1

        if lastday<tmp_day:
            if flag==0:
                tmp_month+=1
                flag=1
            if tmp_month==13:
                tmp_month=1
                tmp_year+=1
            tmp_1week_list.append(str(tmp_year)+"/"+str(tmp_month)+"/"+str(tmp_day-lastday))
        else:
            tmp_1week_list.append(str(tmp_year)+"/"+str(tmp_month)+"/"+str(tmp_day))

    return tmp_1week_list


def make_1week(data_line,tmp_1week_list,week_list):
    time=make_time(data_line)
    if time in tmp_1week_list and time!="":
        week_list.append(time)
        return week_list

def call_time(data_line):
    tmp=data_line.split("\t")
    if len(tmp)==3 and "通話時間" in tmp[2]:
        t=tmp[2]
        tmp1=t.split()
        time_a=tmp1[2]
        a=time_a.split(":")
        h=0
        m=0
        s=0
        if len(a)==2:
            m=int(a[0])
            s=int(a[1])
        elif len(a)==3:
            h=int(a[0])
            m=int(a[1])
            s=int(a[2])
        time_sum=float(h+m/60+s/3600)
        return time_sum
    else:
        return ""

def spend_days(day_list):
    if len(day_list)%2==0 and len(day_list)!=0:
        day_list1=day_list[-2].split("/")
        year1=int(day_list1[0])
        month1=int(day_list1[1])
        day1=int(day_list1[2])    
            
        day_list2=day_list[-1].split("/")
        year2=int(day_list2[0])
        month2=int(day_list2[1])
        day2=int(day_list2[2])

    lastday_start=lastday_cal(year1,month1,day1)
    sum_start=lastday_start-day1+1
    lastday_end=day2
    sum_end=lastday_end-day2+1

    list_sum_day=[]
    c=0
    if year1!=year2:
        tmp_year=year1
        tmp_month=month1
        while tmp_year!=year2 and c!=300:
            for a in range(tmp_month,12+1,1):
                tmp_lastday1=lastday_cal(tmp_year,a,1)
                list_sum_day.append(tmp_lastday1)
                if a==12:
                    tmp_year+=1
                    tmp_month=1
            c+=1

    elif year1==year2:
        for k in range(month1,month2,1):
            tmp_lastday2=lastday_cal(year1,k,1)
            list_sum_day.append(tmp_lastday2)
    
    sum_day=sum_start+sum(list_sum_day)+sum_end
    
    return sum_day


def text_user(data_line):
    tmp=data_line.split("\t")
    if len(tmp)==3:       
        tm_user=tmp[1]
        return tm_user
    else:
        return ""
def text_catch(data_line):
    list_strip=["[ファイル]","[スタンプ]","[写真]","[動画]","[通話]","[ボイスメッセージ]","\n"]
    tmp=data_line.split("\t")
    if len(tmp)==3:
        tm_message=str(tmp[2])         
        for s in list_strip:
            strips=tm_message.replace(s,"") #ここでイランやつを消してんのね
            tm_message=strips
        return tm_message
    else:
        return ""





        
def analysis(txt_file,user1,user2):

    dt_1=0
    dt_2=0
    flag=0
    

    flag_talk_change=0
    flag=0
    day_list_all=[]

    count_user1=0
    count_user2=0


    

    f=open("./tmp/"+txt_file ,"r",encoding='utf-8-sig')
    #f=open("C:/Users/hayat/OneDrive - Shizuoka University/プログラミングデータ/python/アプリ開発練習/txtfile保存場所/[LINE] 志方響（静岡大学 創理）🥺🥺🥺🌲とのトーク.txt","r",encoding='utf-8-sig')
    time_list=[]
    dict_day={}
    dicta={user1:0,user2:0}
    flag1=100
    time_diff_all=[]
    message_count=0
    day_list=[]


    tmp_day_list=[]

    zero_list_user1=[]  #一分を誤差としようかな
    zero_list_user2=[]
    time_diff_user1=[]
    time_diff_user2=[]

    tmp_time=[]
    while flag!=1:             #txtfile内を探っている
        data_line=f.readline()
            
        if data_line!="":
            tm_message=text_catch(data_line)
            if tm_message!="":
                message_count+=1
            tm_user=text_user(data_line)
            hour=send_hour_catch(data_line)
            minuites=send_min_catch(data_line)
            time=make_time(data_line)
            if time=="" and hour!="" and minuites!="":
                tmp_time.append(hour)
                tmp_time.append(minuites)
                tmp_time.append(0)
                day_list.append(tmp_time)
                if user1==tm_user:
                    
                    if len(day_list)==1:
                        flag_talk_change=0
                    
                    if flag_talk_change==0:
                        dt_1=datetime.datetime(day_list[-1][0],day_list[-1][1],day_list[-1][2],day_list[-1][3],day_list[-1][4],day_list[-1][5])
                        #print(dt_1)
                        
                    elif flag_talk_change==1:
                        dt_1=datetime.datetime(day_list[-1][0],day_list[-1][1],day_list[-1][2],day_list[-1][3],day_list[-1][4],day_list[-1][5])
                        if type(dt_1) is datetime.datetime and type(dt_2) is datetime.datetime:
                            time_diff_all.append(round((dt_1-dt_2).total_seconds()/3600,2)) 
                            
                            #user1がプラスでuser2がマイナス
                            if abs(round((dt_1-dt_2).total_seconds()/3600,2))==0.0:
                                zero_list_user1.append(0)
                            flag_talk_change=0            
                else:
                    if flag_talk_change==0:
                        dt_2=datetime.datetime(day_list[-1][0],day_list[-1][1],day_list[-1][2],day_list[-1][3],day_list[-1][4],day_list[-1][5])
                        #print(dt_2)
                        if type(dt_1) is datetime.datetime and type(dt_2) is datetime.datetime:
                            time_diff_all.append((round((dt_1-dt_2).total_seconds()/3600,2)))  #user1がプラスでuser2がマイナス
                            if abs(round((dt_1-dt_2).total_seconds()/3600,2))==0.0:
                                zero_list_user2.append(0)
                        flag_talk_change=1
                        
                    elif flag_talk_change==1:
                        dt_2=datetime.datetime(day_list[-1][0],day_list[-1][1],day_list[-1][2],day_list[-1][3],day_list[-1][4],day_list[-1][5])
                        
                    if len(day_list)==1:
                        flag_talk_change=1
                
                day_list_all.append(tmp_time)
                del tmp_time[3:6]
    
            
            elif time!="":
                tmp_time=time
                #print(tmp_time)
    
            call_time1=call_time(data_line)
            if str(call_time1)!="":
                time_list.append(call_time1)
                

            #print(dicta)
        else:
            flag=1
    
    talk_start=datetime.datetime(day_list[0][0],day_list[0][1],day_list[0][2])
    talk_end=datetime.datetime(day_list[-1][0],day_list[-1][1],day_list[-1][2])
    talk_span=str((talk_end-talk_start).days)
    tmp=[[str(day_list[i][j]) for j in range(3)] for i in range(len(day_list))]
    tmp1=sum(tmp,[])
    tmp2=list(((tmp1[i]+"年")+(tmp1[i+1]+"月")+(tmp1[i+2]+"日")) for i in range(0,len(tmp1),3))
    tmp3=list(sorted(set(tmp2)))
    talk_day=str(len(tmp3))
    list_day_user1=list(filter(lambda x:x<0 ,time_diff_all))
    list_day_user2=list(filter(lambda x:x>0 ,time_diff_all))
    user1_reply=round(float(-min(list_day_user1)/24),0)
    user2_reply=round(float(max(list_day_user2)/24),0)
    reply_time_max=0
    if user1_reply>user2_reply:
        reply_time_max=user1_reply
    else:
        reply_time_max=user2_reply
        
    result1=str(round(float(statistics.mean(time_diff_all)),1))+"日"#平均返信時間二人とも、大幅にずれていなければよいかも？。
    result2=str(statistics.median(time_diff_all))+"日" #中央値がマイナスならuser1に傾いていて、user2はプラスに傾いている場合。？ 
    result3=str(statistics.mode(time_diff_all))+"日" #応答最頻
    result4=str(reply_time_max)+"日" #user1とuser2の応答時間最大値
    result5=str(zero_list_user1.count(0))+"回" #user1即レス
    result6=str(zero_list_user2.count(0))+"回" #user2即レス
    result7=str(message_count)+"回" #総メッセージ数
    result8=str(round(sum(time_list),1))+"時間" #総通話時間
    result9=tmp3[0]+"～"+tmp3[-1]+"の"+talk_span+"日中"+talk_day+"日話している" #期間と会話実行日数を表示したい。

 
    return(result1,result2,result3,result4,result5,result6,result7,result8,result9)
"""
txt_file="C:/Users/hayat/OneDrive - Shizuoka University/プログラミングデータ/python/アプリ開発練習/txtfile保存場所/[LINE] 志方響（静岡大学 創理）🥺🥺🥺🌲とのトーク.txt"
user1="みっぴー(三輪羽哉人)（創理）"
user2="志方響（静岡大学 創理）🥺🥺🥺🌲"
print(analysis(txt_file,user1,user2))
"""