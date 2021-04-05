import pandas as pd
import datetime
import statistics



def text_user(data_line):
    tmp=data_line.split("\t")
    if len(tmp)==3:       
        tm_user=tmp[1]
        return tm_user
    else:
        return ""
def text_catch(data_line):
    list_strip=["\n"]
    tmp=data_line.split("\t")
    if len(tmp)==3:
        tm_message=str(tmp[2])         
        for s in list_strip:
            strips=tm_message.replace(s,"") #ここでイランやつを消してんのね
            tm_message=strips
        return tm_message
    else:
        return ""

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


def make_time(data_line):
    year=year_catch(data_line)
    month=month_catch(data_line)
    day=day_catch(data_line)
    tmp=[year,month,day]
    if year!="" and month!="" and day!="":
        return tmp
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
"""
q1_y=int(request.form["q1_y"]) #記念日:年
q1_m=int(request.form["q1_m"]) #記念日:月
q1_d=int(request.form["q1_d"]) #記念日:日
q2=request.form["q2"] #関係性どのくらい
q3=request.form["q3"] #あなたが何を求めているか
q4=request.form["q4"] #相手が何を求めているかを考えた
koibito_list=[[q1_y,q1_m,q1_d],q2,q3,q4]
"""
        
def sub_analysis_koibito(txt_file,user1,user2):

    dt_1=0
    dt_2=0
    flag=0
    flag_talk_change=0
    flag=0
    day_list_all=[]

    #f=open("./tmp/"+txt_file ,"r",encoding='utf-8-sig')
    f=open("C:/Users/hayat/OneDrive - Shizuoka University/プログラミングデータ/python/アプリ開発練習/txtfile保存場所/[LINE] 浅野秀光（ひでみつ）（創理　物理）とのトーク.txt","r",encoding='utf-8-sig')
    time_list=[]
    day_list=[]

    list_columns=["time","diff_time","message","which_user"]
    df=pd.DataFrame(columns=list_columns)


    tmp_time=[]
    while flag!=1:             #txtfile内を探っている
        data_line=f.readline()
            
        if data_line!="":
            tm_message=text_catch(data_line)
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
                        
                    elif flag_talk_change==1:
                        dt_1=datetime.datetime(day_list[-1][0],day_list[-1][1],day_list[-1][2],day_list[-1][3],day_list[-1][4],day_list[-1][5])
                        if type(dt_1) is datetime.datetime and type(dt_2) is datetime.datetime:
                            seconds_result=round((dt_1-dt_2).total_seconds()/3600,2)
                            tmp_se=pd.Series([dt_1,seconds_result,tm_message,user1],index=df.columns)
                            df= df.append( tmp_se, ignore_index=True )
                            flag_talk_change=0            
                else:
                    if flag_talk_change==0:
                        dt_2=datetime.datetime(day_list[-1][0],day_list[-1][1],day_list[-1][2],day_list[-1][3],day_list[-1][4],day_list[-1][5])
                        if type(dt_1) is datetime.datetime and type(dt_2) is datetime.datetime:
                            seconds_result=round((dt_1-dt_2).total_seconds()/3600,2)
                            tmp_se=pd.Series([dt_2,seconds_result,tm_message,user2],index=df.columns)
                            df= df.append( tmp_se, ignore_index=True )

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
    


    return(day_list,df,round(sum(time_list),1))
"""
txt_file="C:/Users/hayat/OneDrive - Shizuoka University/プログラミングデータ/python/アプリ開発練習/txtfile保存場所/[LINE] 浅野秀光（ひでみつ）（創理　物理）とのトーク.txt"
user1="みっぴー(三輪羽哉人)（創理）"
user2="浅野秀光（ひでみつ）（創理　物理）"
print(sub_analysis_koibito(txt_file,user1,user2))
"""
def analysis_koibito(txt_file,user1,user2,koibito_list):
    year=koibito_list[0][0] #記念日:年
    month=koibito_list[0][1] #記念日:月
    day=koibito_list[0][2] #記念日:日
    relation=koibito_list[1] #関係性どのくらい
    hope_to=koibito_list[2] #あなたが何を求めているか
    hope_from=koibito_list[3] #相手が何を求めているかを考えた
    
    
    list_sub=sub_analysis_koibito(txt_file,user1,user2)
    day_list=list_sub[0]
    df=list_sub[1]
    call_time1=list_sub[2]
    
    
    talk_span=str((df.at[df.index[-1],"time"]-df.at[df.index[0],"time"]).days)
    
    tmp=[[str(day_list[i][j]) for j in range(3)] for i in range(len(day_list))]
    tmp1=sum(tmp,[])
    tmp2=list(((tmp1[i]+"年")+(tmp1[i+1]+"月")+(tmp1[i+2]+"日")) for i in range(0,len(tmp1),3))
    tmp3=list(sorted(set(tmp2)))
    talk_day=str(len(tmp3))
    
    
    time_diff_all=df["diff_time"].values.tolist()    
    
    list_day_user1=list(filter(lambda x:x<0 ,time_diff_all))
    list_day_user2=list(filter(lambda x:x>0 ,time_diff_all))
    user1_reply=round(float(-min(list_day_user1)/24),0)
    user2_reply=round(float(max(list_day_user2)/24),0)
    reply_time_max=0
    
    if user1_reply>user2_reply:
        reply_time_max=user1_reply
    else:
        reply_time_max=user2_reply
    
    user1_t=df[df["which_user"]==user1]
    user2_t=df[df["which_user"]==user2]
    zero_user1=len(user1_t[user1_t["diff_time"]==0])
    zero_user2=len(user2_t[user2_t["diff_time"]==0])
    
    
    
    result1=str(round(float(statistics.mean(time_diff_all)),1))+"日"#平均返信時間二人とも、大幅にずれていなければよいかも？。
    result2=str(statistics.median(time_diff_all))+"日" #中央値がマイナスならuser1に傾いていて、user2はプラスに傾いている場合。？ 
    result3=str(statistics.mode(time_diff_all))+"日" #応答最頻
    result4=str(reply_time_max)+"日" #user1とuser2の応答時間最大値
    result5=str(zero_user1)+"回" #user1即レス
    result6=str(zero_user2)+"回" #user2即レス
    result7=str(len(df))+"回" #総メッセージ数
    result8=str(call_time1)+"時間" #総通話時間
    result9=tmp3[0]+"～"+tmp3[-1]+"の"+talk_span+"日中"+talk_day+"日話している" #期間と会話実行日数を表示したい。
    tmp_date=datetime.datetime(year,month,day)
    
    
    #付き合った前と付き合ったあとの変化を表現する。
    #連絡頻度、電話総合時間、
    #以下の計算により、付き合った後の上昇を見る。
    before=(tmp_date-df.at[df.index[0],"time"]).days #付き合う前の日数を計算
    after=1+(df.at[df.index[-1],"time"]-tmp_date).days #付き合った後の日数を計算
    
    b_df=df[df["time"]<tmp_date]
    
    
    a_df=df[(df["time"]>=tmp_date) & (df["which_user"]==user1)]
    
    return (result1,result2,result3,result4,result5,result6,result7,result8,result9,before,after,df.info(),b_df,a_df)


txt_file="C:/Users/hayat/OneDrive - Shizuoka University/プログラミングデータ/python/アプリ開発練習/txtfile保存場所/[LINE] 浅野秀光（ひでみつ）（創理　物理）とのトーク.txt"
user1="みっぴー(三輪羽哉人)（創理）"
user2="浅野秀光（ひでみつ）（創理　物理）"
q1_y=2020 #記念日:年
q1_m=7 #記念日:月
q1_d=19 #記念日:日
q2=100 #関係性どのくらい
q3="愛情" #あなたが何を求めているか
q4="愛情" #相手が何を求めているかを考えた
koibito_list=[[q1_y,q1_m,q1_d],q2,q3,q4]

print(analysis_koibito(txt_file,user1,user2,koibito_list))







