# -*- coding: utf-8 -*-
from pathlib import Path
from janome.charfilter import *
from janome.analyzer import Analyzer
from janome.tokenizer import Tokenizer
from janome.tokenfilter import *




# janomeのAnalyzerを使うことで、文の分割と単語の正規化をまとめて行うことができる
# 文に対する処理のまとめ
char_filters = [UnicodeNormalizeCharFilter(),         # UnicodeをNFKC(デフォルト)で正規化
                RegexReplaceCharFilter('\(', ''),     # (を削除
                RegexReplaceCharFilter('\)', '')      # )を削除
                ]

# 単語に分割
tokenizer = Tokenizer()


#
# 名詞中の数(漢数字を含む)を全て0に置き換えるTokenFilterの実装
#
class NumericReplaceFilter(TokenFilter):

    def apply(self, tokens):
        for token in tokens:
            parts = token.part_of_speech.split(',')
            if (parts[0] == '名詞' and parts[1] == '数'):
                token.surface = '0'
                token.base_form = '0'
                token.reading = 'ゼロ'
                token.phonetic = 'ゼロ'
            yield token


#
#  ひらがな・カタガナ・英数字の一文字しか無い単語は削除
#
class OneCharacterReplaceFilter(TokenFilter):

    def apply(self, tokens):
        for token in tokens:
            # 上記のルールの一文字制限で引っかかった場合、その単語を無視
            if re.match('^[あ-んア-ンa-zA-Z0-9ー]$', token.surface):
                continue

            yield token

def count(user):

    file_path = Path('./tmp')

    file_name= user+'.txt'
    with open(file_path.joinpath(file_name), 'r', encoding='utf-8') as file:
        texts = file.readlines()
        texts = [text_.replace('\n', '') for text_ in texts]

    # 単語に対する処理のまとめ
    token_filters = [NumericReplaceFilter(),                         # 名詞中の漢数字を含む数字を0に置換
                     CompoundNounFilter(),                           # 名詞が連続する場合は複合名詞にする
                     POSKeepFilter(['名詞', '動詞', '形容詞', '副詞']),# 名詞・動詞・形容詞・副詞のみを取得する
                     LowerCaseFilter(),                              # 英字は小文字にする
                     OneCharacterReplaceFilter()                     # 一文字しか無いひらがなとカタガナと英数字は削除
                     ]

    analyzer = Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)


    tokens_list = []
    raw_texts = []
    for text in texts:
        # 文を分割し、単語をそれぞれ正規化する
        text_ = [token.base_form for token in analyzer.analyze(text)]
        if len(text_) > 0:
            tokens_list.append([token.base_form for token in analyzer.analyze(text)])
            raw_texts.append(text)

    # 正規化された際に一文字もない文の削除後の元テキストデータ
    raw_texts = [text_+'\n' for text_ in raw_texts]
    with open(file_path.joinpath(file_name.replace('.txt', '_cut.txt')), 'w', encoding='utf-8') as file:
        file.writelines(raw_texts)


    # 単語リストの作成
    words = []
    for text in tokens_list:
        words.extend([word for word in text if word != ''])

    list_f=["笑","笑笑","ご飯","飯","電話","相談","おいしい","好き","うれしい","やった","好きな人","彼女","彼氏","彼","いい","楽しい","強い","さすが","食べる","おやすみ","おやすみなさい","おっは～","ありがとう","ごはん","お昼","おひる","店","みせ","行く","いく","待ち合わせ","作る","よい","不安","がんばる","頑張る","しんどい","できる","こわい","つらい","のめる","飲む","楽しい","たのしい","もてる","飲める","食べれる","いく","行く"]
    list_p=["お風呂","おふろ","シャワー","幸せ","うれしい","行こう","おいしい","美味しい","やった","相談","痛い","いたい","すき","好き","頼もしい","たのもしい","店","お店","ごはん","ご飯","寝る","よろしく","付き合う","つきあう","調子","体調","大丈夫","だいじょうぶ","平気","へいき","まつ","なでる","かわいい","可愛い","これから","あした","明日","励ます","泣く","まだ","生理","過ごす","髪"]
    list_l=["会う","電話","好き","美味しい","おいしい","また","うれしい","おつかれ","頑張る","聞く","好きな人"]
    list_anger=["腹立つ","なんだよ","おかしい","違う","だめ","もう","ちゃう","また","まだ","それだけ","そんだけ","ヤダ","なんで","はあ","どうして","ふざけるな","おい","くそ","クソ","無理","むり","ムリ"]
    list_sadness=["悲しい","かなしい","残念","ざんねん","そうか","そっか","また","馬鹿","ばか","バカ","下がる","さがる","しんみり","寂しい","さみしい","むなしい","虚しい","しくしく","泣く"]
    list_pleasure=["楽しい","やる","神","ノリ","のり","いい","天才","てんさい","やた","やった","すごい","凄い","よい","良い","上がる","面白い","おもしろい","たのしい","おもろい"]
    list_fear=["不安","ふあん","ハード","ダメ","だめ","怖い","こわい","恐い","やだ","ヤダ","ダメ","だめ","駄目","心配","しんぱい","しんどい","つらい","無理","ムリ"]
    list_love=["大丈夫","だいじょうぶ","気を付ける","きをつける","頼もしい","お疲れ","おつかれ","頑張る","かんばる","おつ","だよ","落ち着く","ほっと","元気","面白い","おもしろい","ほっ","明日","あした"]
    
    
    resultA = 0 #friend 友情関係
    resultB = 0 #parner 診断
    resultC = 0 #like 脈あり診断
    resultD = 0 #怒り　
    resultE = 0 #悲しみ
    resultF = 0 #喜び
    resultG = 0 #恐れる
    resultH = 0 #好き
    

    for x in range(0,49):
        resultA = resultA + words.count(list_f[x])
    
    for x in range(0,43):    
        resultB = resultB + words.count(list_p[x])
    
    for x in range(0,11):    
        resultC = resultC + words.count(list_l[x])
        
    for x in range(0,22):
        resultD = resultD + words.count(list_anger[x])
    
    for x in range(0,18):    
        resultE = resultE + words.count(list_sadness[x])
    
    for x in range(0,19):    
        resultF = resultF + words.count(list_pleasure[x])    
   
    for x in range(0,19):
        resultG = resultG + words.count(list_fear[x])
    
    for x in range(0,19):    
        resultH = resultH + words.count(list_love[x])
    
    
        
    return(resultA,resultB,resultC,resultD,resultE,resultF,resultG,resultH)