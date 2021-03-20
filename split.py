import csv
import os
path = './tmp'
def split(txt_file):
    fi = "./tmp/"+txt_file
    line=fi.split("/")
    tmp_line=line[-1]
    list_del = ["[LINE]","とのトーク","txt"]
    t1=tmp_line
    t2=""
    for a in list_del:
        t2=t1.replace(a,"")
        t1=t2
        
    user1_except=t1.strip()
        
    f=open("./tmp/"+txt_file ,"r",encoding='utf-8-sig')
        
    tmp=f.readline()
        
    user1_tmp1=tmp.replace("[LINE]","")
    user1_tmp2=user1_tmp1.replace("とのトーク履歴\n","")
    tm_usn=len(user1_tmp1)
        
    user1=user1_tmp2[1:tm_usn]
        
    f1=open("./tmp/"+txt_file,"r",encoding='UTF-8')
        
    
        
    flag=0
    list_user1=[]
    list_user2=[]
    list_strip=["[ファイル]","[スタンプ]","[写真]","[動画]","[通話]","[ボイスメッセージ]","\n"]
        
        
    while flag!=1:
        data=f.readline()
        if data!="":
            tmp=data.split("\t")
            if len(tmp)==3:
                tm_message=str(tmp[2])
                tm_user=tmp[1]
                for s in list_strip:
                    strips=tm_message.replace(str(s),"")
                    tm_message=strips
                if tm_message!="":
                    if user1==tm_user:
                        list_user1.append(tm_message)
                    else:
                        if len(list_user2)==0:
                            user2=tm_user
                        list_user2.append(tm_message)
        else:
            flag=1
            
    try:
        with open(path+"/"+user1+".csv","w",encoding='UTF-8') as f1:
            writer=csv.writer(f1)
            writer.writerow(list_user1)
    except FileNotFoundError:
        with open(path+"/"+user1_except+".csv","w",encoding='UTF-8') as f1_1:                                   
            writer=csv.writer(f1_1)
            writer.writerow(list_user1)
    try:
        with open(path+"/"+user2+".csv","w",encoding='UTF-8') as f2: #写真等の文字以外を含むファイルを作成ユーザ1
            writer=csv.writer(f2)
            writer.writerow(list_user2)
    except FileNotFoundError:
        with open(path+"/"+user1_except+"の相手"+".csv","w",encoding='UTF-8') as f2_2: #写真等の文字以外を含むファイルを作成ユーザ1
            writer=csv.writer(f2_2)
            writer.writerow(list_user2) 
    
    try:
        with open(path+"/"+user1+".txt","w",encoding='UTF-8') as f1:
           f1.writelines(list_user1)
           a = user1
    except FileNotFoundError:
        with open(path+"/"+user1_except+".txt","w",encoding='UTF-8') as f1_1:                                   
            f1_1.writelines(list_user1)
            a = user1_except
    try:
        with open(path+"/"+user2+".txt","w",encoding='UTF-8') as f2: #写真等の文字以外を含むファイルを作成ユーザ1
            f2.writelines(list_user2)
            b = user2
    except FileNotFoundError:
        with open(path+"/"+user1_except+"の相手"+".txt","w",encoding='UTF-8') as f2_2: #写真等の文字以外を含むファイルを作成ユーザ1
            f2_2.writelines(list_user2)  
            b = user1_except+"の相手"
      
    
    return(a,b,user1,user2)
