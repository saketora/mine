from flask import Flask, request, abort,render_template, redirect, url_for
from werkzeug.utils import secure_filename


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os
import wordcount as co
import time_text as an
import split as dv
app = Flask(__name__)

#LINEBOT関連

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = "Ug2O9rIdPypeupUwtsAAgcFPp4o097Hh5tPBj7PH1jnSbiYNif8nF1BZYJIDMdQlDZ8CqxX/1DPEB9z6ueJvVbboPue//6+CIUiXBp5xuf3mcKAPFrXhoNjQBzTDsmjN2p40dx8ix4AzHd34qaW+QQdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "e9ed8fc4c92f033ffe5bb7e0ae48e322"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    
    
    
#ここからはWEBページ関連

   
#「/home1」へアクセスがあった場合に、「home1.html」を返す
@app.route("/home1")
def home1():
    title = "友達診断"
    return render_template("home1.html", title=title)

#以下同様

@app.route("/home2")
def home2():
    title = "恋人診断"
    return render_template("home2.html", title=title)

@app.route("/home3")
def home3():
    title = "脈あり診断"
    return render_template("home3.html", title=title) 


#それぞれの結果表示用view 
   
@app.route("/result11")
def result11():
    title = "友達結果"
    return render_template("result11.html", title=title) 

@app.route("/result12")
def result12():
    title = "友達結果"
    return render_template("result12.html", title=title) 

@app.route("/result13")
def result13():
    title = "友達結果"
    return render_template("result13.html", title=title) 

@app.route("/result14")
def result14():
    title = "友達結果"
    return render_template("result14.html", title=title) 

@app.route("/result21")
def result21():
    title = "恋人結果"
    return render_template("result21.html", title=title) 

@app.route("/result22")
def result22():
    title = "恋人結果"
    return render_template("result22.html", title=title) 

@app.route("/result23")
def result23():
    title = "恋人結果"
    return render_template("result23.html", title=title) 

@app.route("/result24")
def result24():
    title = "恋人結果"
    return render_template("result24.html", title=title) 

@app.route("/result31")
def result31():
    title = "脈あり度結果"
    return render_template("result31.html", title=title) 

@app.route("/result32")
def result32():
    title = "脈あり度結果"
    return render_template("result32.html", title=title) 

@app.route("/result33")
def result33():
    title = "脈あり度結果"
    return render_template("result33.html", title=title) 

@app.route("/result34")
def result34():
    title = "脈あり度結果"
    return render_template("result34.html", title=title)



#アップロード読み込み用
UPLOAD_FOLDER = './tmp'
ALLOWED_EXTENSIONS = set(['txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

#拡張子判定
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/send1', methods=['GET', 'POST']) #友達診断結果
def send1():
    if request.method == 'POST':
        txt_file = request.files['txt_file']
        if txt_file and allowed_file(txt_file.filename):
               file_name = secure_filename(txt_file.filename)
               txt_file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
               x = dv.split(file_name)
               y1=co.count(x[0])
               y2=co.count(x[1])
               z =an.analysis(file_name,x[2],x[3])
               friend_keisu=int(z[5][:-1])/(int(z[6][:-1])+1)
               if friend_keisu==0: #相手の即レスカウントと総メッセージ数の商が
                   friend_keisu=1
               if y2[0]>400*friend_keisu or float(z[0][:-1])<0: 
                  return render_template('result11.html',uname1=x[0],uname2=x[1], re11=y1[0], re12=y1[1], re13=y1[2], re14=y1[3], re15=y1[4], re16=y1[5], re17=y1[6], re18=y1[7], re21=y2[0], re22=y2[1], re23=y2[2], re24=y2[3], re25=y2[4], re26=y2[5], re27=y2[6], re28=y2[7], re31=z[0], re32=z[1], re33=z[2], re34=z[3], re35=z[4], re36=z[5], re37=z[6], re38=z[7], re39=z[8])
               elif 401*friend_keisu>y2[0]>300*friend_keisu: 
                   return render_template('result12.html',uname1=x[0],uname2=x[1], re11=y1[0], re12=y1[1], re13=y1[2], re14=y1[3], re15=y1[4], re16=y1[5], re17=y1[6], re18=y1[7], re21=y2[0], re22=y2[1], re23=y2[2], re24=y2[3], re25=y2[4], re26=y2[5], re27=y2[6], re28=y2[7], re31=z[0], re32=z[1], re33=z[2], re34=z[3], re35=z[4], re36=z[5], re37=z[6], re38=z[7], re39=z[8])
               elif 301*friend_keisu>y2[0]>200*friend_keisu: 
                   return render_template('result13.html',uname1=x[0],uname2=x[1], re11=y1[0], re12=y1[1], re13=y1[2], re14=y1[3], re15=y1[4], re16=y1[5], re17=y1[6], re18=y1[7], re21=y2[0], re22=y2[1], re23=y2[2], re24=y2[3], re25=y2[4], re26=y2[5], re27=y2[6], re28=y2[7], re31=z[0], re32=z[1], re33=z[2], re34=z[3], re35=z[4], re36=z[5], re37=z[6], re38=z[7], re39=z[8])
               else:
                   return render_template('result14.html',uname1=x[0],uname2=x[1], re11=y1[0], re12=y1[1], re13=y1[2], re14=y1[3], re15=y1[4], re16=y1[5], re17=y1[6], re18=y1[7], re21=y2[0], re22=y2[1], re23=y2[2], re24=y2[3], re25=y2[4], re26=y2[5], re27=y2[6], re28=y2[7], re31=z[0], re32=z[1], re33=z[2], re34=z[3], re35=z[4], re36=z[5], re37=z[6], re38=z[7], re39=z[8])
        else:
            return ''' <p>許可されていない拡張子です</p> '''
    else:
        return redirect(url_for('home1'))

@app.route('/send2', methods=['GET', 'POST']) #恋人診断
def send2():
        if request.method == 'POST':
            txt_file = request.files['txt_file']
            if txt_file and allowed_file(txt_file.filename):
                file_name = secure_filename(txt_file.filename)
                txt_file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                q1_y=int(request.form["q1_y"]) #記念日:年
                q1_m=int(request.form["q1_m"]) #記念日:月
                q1_d=int(request.form["q1_d"]) #記念日:日
                q2=request.form["q2"] #関係性どのくらい
                q3=request.form["q3"] #あなたが何を求めているか
                q4=request.form["q4"] #相手が何を求めているかを考えた
                koibito_list=[[q1_y,q1_m,q1_d],q2,q3,q4]
                
                return render_template('result21.html',q1_y=q1_y,q1_m=q1_m,q1_d=q1_d,q2=q2,q3=q3,q4=q4)
            else:
                return ''' <p>許可されていない拡張子です</p> '''
        else:
            return redirect(url_for('home2'))

@app.route('/send3', methods=['GET', 'POST']) #脈あり診断
def send3():
        if request.method == 'POST':
            txt_file = request.files['txt_file']
            if txt_file and allowed_file(txt_file.filename):
                file_name = secure_filename(txt_file.filename)
                txt_file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                q1=request.form["q1"] #関係は何か？
                q2_y=int(request.form["q2_y"]) #関係年
                q2_m=int(request.form["q2_m"]) #関係月
                q3=int(request.form["q3"]) #共通点個数
                q4=int(request.form["q4"]) #自分が思う好感度
                myakuari_list=[q1,[q2_y,q2_m],q3,q4]
                
                return render_template('result31.html',q1=q1,q2_y=q2_y,q2_m=q2_m,q3=q3,q4=q4)
            else:
                return ''' <p>許可されていない拡張子です</p> '''
        else:
            return redirect(url_for('home3'))



if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)