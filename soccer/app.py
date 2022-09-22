from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://3.39.233.29', 27017, username="test", password="test")
db = client.EPL_onetouch

SECRET_KEY = 'SPARTA'

import jwt

import datetime
from datetime import datetime, timedelta

import hashlib

@app.route('/')
def welcome():
    return render_template('welcome.html')


#epl순위
@app.route('/record', methods=['GET'])
def ranking_get():
    ranking_list = list(db.eplRank.find({}, {'_id':False}))
    # return jsonify({'eplRank':ranking_list})
    return render_template('index.html', ranking_list= ranking_list)


    # jinja2를 이용한 데이터 관리

@app.route('/news1')
def news1():
    return render_template('news1.html')

@app.route('/news2')
def news2():
    return render_template('news2.html')

@app.route('/news3')
def news3():
    return render_template('news3.html')


# 로그인 페이지
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

# 아이디 중복확인
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

# 회원가입
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,
        "password": password_hash
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

# 로그인
@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# 토큰 발급
@app.route('/log_in')
def log_in():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html')

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))




#DB에 순위 저장(주석해제하고 실행하면 데이터가 계속 쌓이니 랭킹 갱신할때 DB정리하고 주석해제해서 한번만 실행하세요.)
# url = "https://www.goal.com/kr/%ED%94%84%EB%A6%AC%EB%AF%B8%EC%96%B4%EB%A6%AC%EA%B7%B8/%EC%88%9C%EC%9C%84/2kwbbcootiqqgmrzs6o5inle5"
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(url, headers=headers)
#
# req = data.text
# soup = BeautifulSoup(req, 'html.parser')
#
# wfootball = soup.select("body > div.page-container > div.page-container-bg > div.mr-gutters.main-container.clearfix > div > div > div.widget-match-standings > div.widget-match-standings__table-container > table > tbody > tr")
#
# for ranking in wfootball:
#     rank = ranking.select_one("td:nth-child(1)").text
#     team = ranking.select_one("td.widget-match-standings__team > a.widget-match-standings__link > abbr").text
#     played = ranking.select_one("td.widget-match-standings__matches-played").text
#     won = ranking.select_one("td.widget-match-standings__matches-won").text
#     drawn = ranking.select_one("td.widget-match-standings__matches-drawn").text
#     lost = ranking.select_one("td.widget-match-standings__matches-lost").text
#     pts = ranking.select_one("td.widget-match-standings__pts").text
#     doc = {
#         'rank': rank,
#         'team': team,
#         'played': played,
#         'won': won,
#         'drawn': drawn,
#         'lost': lost,
#         'pts': pts,
#     }
#     db.eplRank.insert_one(doc)

if __name__=="__main__":
    app.run('0.0.0.0', port=5000, debug=True)