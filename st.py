import streamlit as st
import random
import pandas as pd

st.title("クロスワード自動作成アプリ")
st.caption("単語を入れるだけで自動でクロスワードを作成します。")

size = st.slider('クロスワードのサイズ', 8, 10, 8)
st.caption("宿題で出されたクロスワードのマス目は８マスです。")
st.write("サイズ:", size, 'マス')

txt = st.text_area('クロスワードの問題にする単語', '''スポーツ
オリンピック
フェアプレイ
マンシップ
ショウギョウ
メディア
ルール
ボランティア
キョウギタイカイ
クーベルタン
オリンピズム
ムーブメント
グットマン
キョウセイ
ウソウケン
ケイザイハキュウ
ショウリシジョウ
ドーピング
カンキョウ
ホゴカツドウ''',height=500)



tryTimes = 10
cheeze = 1
none = ""

def conformData():	
    element = txt
    elements = element.split("\n")

    dictionary = {}

    for i in elements:
        for j in i:
            dictionary.update({j:element.count(j)})

    dictionary = sorted(dictionary.items(), key=lambda x:x[1], reverse=True)

    chars = {}

    for i in elements:
        score = 0
        for j in dictionary:
            if j[0] in i:
                score += j[1]
        chars.update({i:score})

    chars = sorted(chars.items(), key=lambda x:x[1], reverse=True)

    return chars


tile = []
def makeTiles():
    for i in range(size):
        part = []
        for j in range(size):
            part.append("  ")
        tile.append(part)
        
def paintTiles():
    df = pd.DataFrame(tile
    ,
    columns=('%d' % i for i in range(size)))

    st.table(df)
    
        

def findCommon(char):
    rightPlaces = []
    for y,ti in enumerate(tile):
        for x,u in enumerate(ti):
            if char == u:
                rightPlaces.append([x,y])
    if(len(rightPlaces) == 0):
        return "None","None"
    else:
        rightPlace = random.choice(rightPlaces)
        return rightPlace[0],rightPlace[1]

def checkDouble(char,x,y,num,tilt):
    global none
    if tilt == "line":
        for times,ch in enumerate(char):
            if tile[y-num+times][x] == "  " or tile[y-num+times][x] == ch:
                none = ""
            else:
                return False
        return True
    else:
        for times,ch in enumerate(char):
            if tile[y][x-num+times] == "  " or tile[y][x-num+times] == ch:
                none = ""
            else:
                return False
        return True


def reload(list):
    global cheeze
    cheeze += 1
    if list[4] == "line":
        for times,ch in enumerate(list[0]):
            tile[list[2]-list[3]+times][list[1]] = ch
    else:
        for times,ch in enumerate(list[0]):
            tile[list[2]][list[1]-list[3]+times] = ch

leftWords = []
def moreThan2(char,tilt):
    global none
    ava = []
    for num,ch in enumerate(char):
        x,y = findCommon(ch)
        if x == "None":
            none = ""
        elif tilt == "line":
            
            if size >= y + len(char) - num and y - num >= 0 and checkDouble(char,x,y,num,"line"):
                ava.append([char,x,y,num,"line"])
        elif tilt == "row":
            if size >= x + len(char) - num and x - num >= 0 and checkDouble(char,x,y,num,"row"):
                ava.append([char,x,y,num,"row"])

    av = []
    if ava == []:
        leftWords.append(char)
    else:
        av = random.choice(ava)
        reload(av)

def extra2(char,tilt,flag):
    global none
    ava = []
    for num,ch in enumerate(char):
        x,y = findCommon(ch)
        if x == "None":
            none = ""
        elif tilt == "line":
            if size >= y + len(char) - num and y - num >= 0 and checkDouble(char,x,y,num,"line"):
                ava.append([char,x,y,num,"line"])
        elif tilt == "row":
            if size >= x + len(char) - num and x - num >= 0 and checkDouble(char,x,y,num,"row"):
                ava.append([char,x,y,num,"row"])
        
        
    
    av = []
    if ava == []:
        none = ""
    else:
        if flag:
            leftWords.remove(char)
        av = random.choice(ava)
        reload(av)
        

            
def theOne(i):
    int = random.randint(0,3)
    if int == 0:		
        for j in range(len(i[0])):
            tile[j][3] = i[0][j]
        tilt = "line"
    if int == 1:
        for j in range(len(i[0])):
            tile[j][4] = i[0][j]
        tilt = "line"
    if int == 2:
        for j in range(len(i[0])):
            tile[3][j] = i[0][j]
    if int == 3:
        for j in range(len(i[0])):
            tile[4][j] = i[0][j]
    
def exe():
    times = 0
    tilt = "row"
    for i in chars:
        if times == 0:
            theOne(i)
        else:
            moreThan2(i[0],tilt)
            
        if tilt == "row":
            tilt = "line"
        elif tilt == "line":
            tilt = "row"
        
        if times != 0:
            moreThan2(i[0],tilt)

        times += 1

    tilt = "row"

    for _ in range(tryTimes):
        for word in leftWords:
            extra2(word,tilt,False)

            if tilt == "row":
                tilt = "line"
            elif tilt == "line":
                tilt = "row"
                        
            extra2(word,tilt,True)

data = []
tiles = []
if st.button('作成'):
    for i in range(100):
        tile = []
        leftWords = []
        cheeze = 1
        chars = conformData()
        makeTiles()
        exe()

        data.append(cheeze)
        tiles.append(tile)
    
    st.caption("もう一度作成ボタンを押すと新しいパターンのクロスワードが作成されます。")
    st.header(max(data))
    th = data.index(max(data))
    tile = tiles[th]
    paintTiles()
