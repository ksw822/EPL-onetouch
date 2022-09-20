from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/main')
def index():
  return render_template('index.html')

#로그인 페이지
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

#토큰 발급
# @app.route('/log_in')
# def log_in():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

#         return render_template('index.html')

#     except jwt.ExpiredSignatureError:
#         return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#     except jwt.exceptions.DecodeError:
#         return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

# #comment 저장
# @app.route('/comment', methods=['POST'])
# def comment_write():
#     comment_receive = request.form['comment_give']
#     params_receive = request.form['params_give']
#     db.comment.insert_one({"comment" : comment_receive, "modelCommentID" : params_receive})
#     return jsonify({'msg': '등록완료!!'})



if __name__=="__main__":
    app.run('0.0.0.0', port=5000, debug=True)