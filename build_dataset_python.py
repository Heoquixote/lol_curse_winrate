import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import selenium
import requests
import os

df = pd.read_csv('./raw220628.csv')

data = []
k = 1

def data_crawling(user_name):
    #DB 유저 불러오기
    url = f'https://your.gg/kr/profile/{user_name}'
    resp = requests.get(url)
    html = BeautifulSoup(resp.text, 'html.parser')
#승패 크롤링
    users = []
    for j in html.select('ul.d490eh-10 a'):
        users.append(j.text)
    for i in range(30):
        # html 내 게임 아이디 크롤링
        ingame_id = html.select('div.sc-15xrq75-3 span')[0].text.strip()
        # 티어 크롤링
        # buiiz7-0 sc-1p3os9u-3 hCTbNr zMKXD
        tier = html.select('div span.sc-1p3os9u-3')[0].text.strip()
        # 승, 패 크롤링
        # buiiz7-0 d490eh-4 hCTbML dSQenp
        Win_lose = html.select('span.d490eh-4')[i].text
        # KDA 크롤링
        # buiiz7-0 sc-1p49g2y-1 hNEJCS gLFnks
        KDA = html.select('span.sc-1p49g2y-1')[i*3].text[:-7]
        kill = KDA.split('/')[0]
        death =  KDA.split('/')[1]
        assist = KDA.split('/')[2]
        # 게임 시간 크롤링
        # buiiz7-0 d490eh-5 hNEJEN
        game_time = html.select('span.d490eh-5')[i].text
        # 챔피언 크롤링
        # sc-1xwhuw1-0 afFmu sc-1hmh1k6-4 dIKnaT
        champion =html.select('div.sc-1xwhuw1-0 img')[i*11]['alt']
        # 킬 관여율 크롤링
        kill_pati = html.select('span.sc-1p49g2y-1')[i*3].text[-5:-1]
        # 포지션 크롤링 두번째 방법
        # your.gg의 게임 결과의 우측에 닉네임이 존재하는 순서를 통해 포지션 크롤링 하기
        # d490eh-10 dkiApC
        
        if users[10*i:10*(i+1)].index(ingame_id) == 0 or users[10*i:10*(i+1)].index(ingame_id) == 1:
            position = 'top'
        elif users[10*i:10*(i+1)].index(ingame_id) == 2 or users[10*i:10*(i+1)].index(ingame_id) == 3:
            position = 'jungle'
        elif users[10*i:10*(i+1)].index(ingame_id) == 4 or users[10*i:10*(i+1)].index(ingame_id) == 5:
            position = 'mid'
        elif users[10*i:10*(i+1)].index(ingame_id) == 6 or users[10*i:10*(i+1)].index(ingame_id) == 7:
            position = 'adc'
        else:
            position = 'support'
        # 0~1 top
        # 2~3 jungle
        # 4~5 mid
        # 6~7 adc
        # 8~9 support
        data.append([ ingame_id, tier, Win_lose, champion, position, kill, death, assist, kill_pati ])
    print(f'{k}번째 유저 {ingame_id} 데이터 크롤링 중')

col_nm = ['유저명', '티어', '승패', '챔피언', '포지션', 'Kill', 'Death', 'Assist', '킬관여율']


for i in df['Column2'][501:]:
    try :
        data_crawling(i)
    except:
        pass

data = pd.DataFrame(data,columns=col_nm)
data.to_csv("dataset.csv", mode='w', header=False)