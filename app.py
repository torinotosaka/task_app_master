# flaskモジュールからFlaskクラスをインポート
from flask import Flask, render_template, request, redirect, session
# sqlite3をインポート
import sqlite3
# 課題4
import datetime
# 課題8
import os
# Flaskクラスをインスタンス化してapp変数に代入
app = Flask(__name__)

# secret_keyでセッション情報を暗号化
app.secret_key = "SUNABACO2023"

# ここにコードを書いてく
# @app.route("/")
# def hello():
#     return "Hello World!"

@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/list")
    else:
        return render_template("index.html")

# @app.route("/<name>")
# def greet(name):
#     return name + "さん、こんばんは！"

@app.route("/add")
def add_get():
    if "user_id" in session:
        # 課題6
        login_status = "active"
        # 課題6
        return render_template("add.html", login_status = login_status)
    else:
        return redirect("/")

@app.route("/add", methods=["POST"])
def add_post():
    if "user_id" in session:
        user_id = session["user_id"][0]
        # HTMLの入力フォームからデータをDBに保存する
        # 1.入力フォームからデータを取得する
        task = request.form.get("task")
        print(task)
        # 課題4
        dt_now = datetime.datetime.now()
        dt_now = dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
        # 2.データベースに接続する
        conn = sqlite3.connect("myTask.db")
        # 3.データベースを操作するための準備
        c = conn.cursor()
        # 4.SQLを実行してDBにデータを送る
        # 課題1・課題4
        c.execute("insert into task values (null, ?, ?, 0, ?)", (task, user_id, dt_now))
        # 5.データベースを更新（保存）する
        conn.commit()
        # 6.データベースの接続を終了する
        c.close()
        # リダイレクトでルーティングに飛ばす
        return redirect("/list")
    else:
        return redirect("/")

@app.route("/list")
def list_get():
    # セッションが保持されていればリストページを返す
    if "user_id" in session:
        user_id = session["user_id"][0]
        # 課題6
        login_status = "active"
        conn = sqlite3.connect("myTask.db")
        c = conn.cursor()
        # 課題8
        c.execute("select name, prof_img from users where id = ?",(user_id,))
        # user_name = c.fetchone()[0]
        user_data = c.fetchone()
        # 課題1・課題4
        c.execute("select id, task, datetime from task where user_id = ? and flug = 0",(user_id,))
        # データを格納する配列を準備
        task_list = []
        # c.fetchall()で指定したDBのレコードを全件取得する
        for row in c.fetchall():
            # 取得したレコードを辞書型に変換して、task_listに追加する
            # 課題4
            task_list.append({"id":row[0],"task":row[1],"datetime":row[2]})
        c.close()
        print(task_list)
        # 課題6・課題8
        return render_template("list.html", task_list = task_list, user_data = user_data, login_status = login_status)
    else:
        return redirect("/")

@app.route("/edit/<int:task_id>")
def edit_get(task_id):
    if "user_id" in session:
        # 課題2
        user_id = session["user_id"][0]
        conn = sqlite3.connect("myTask.db")
        c = conn.cursor()
        # 課題2
        c.execute("select task from task where id = ? and user_id = ?", (task_id,user_id))
        # c.fetchone()でレコードの1行を取得（配列で取得される）
        task = c.fetchone()
        print(task)
        c.close()
        # 課題2
        if task is None:
            return redirect("/")
        else:
            task = task[0]
            return render_template("edit.html", task = task, task_id = task_id)
    else:
        return redirect("/")

@app.route("/edit", methods=["POST"])
def edit_post():
    if "user_id" in session:
        # フォームからtaskのidを取得
        task_id = request.form.get("task_id")
        # フォームから修正後の入力内容を取得
        task = request.form.get("task")
        # DBに接続
        conn = sqlite3.connect("myTask.db")
        # DBを操作できるようにする
        c = conn.cursor()
        # SQLを実行
        c.execute("update task set task = ? where id = ?", (task, task_id))
        # DBを更新（保存）する
        conn.commit()
        # DBの接続を終了する
        c.close()
        # リストページにリダイレクト
        return redirect("/list")
    else:
        return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    if "user_id" in session:
        # 課題3
        user_id = session["user_id"][0]
        # DBに接続
        conn = sqlite3.connect("myTask.db")
        # DBを操作できるようにする
        c = conn.cursor()
        # SQLを実行する
        # 課題1・課題3
        c.execute("update task set flug = 1  where id = ? and user_id = ?", (task_id, user_id))
        # DBを更新（保存）する
        conn.commit()
        # DBの接続を終了
        c.close()
        # listページにリダイレクトする
        return redirect("/list")
    else:
        return redirect("/")

@app.route("/regist")
def regist_get():
    if "user_id" in session:
        return redirect("/list")
    else:
        return render_template("regist.html")

@app.route("/regist", methods=["POST"])
def regist_post():
    # フォームから名前を取得
    name = request.form.get("name")
    # フォームからパスワードを取得
    password = request.form.get("password")
    print("名前："+name+"パスワード："+password)

    conn = sqlite3.connect("myTask.db")
    c = conn.cursor()
    c.execute("insert into users values(null, ?, ?, ?)",(name, password, "default.png"))
    conn.commit()
    c.close()
    return redirect("/login")

@app.route("/login")
def login_get():
    if "user_id" in session:
        return redirect("/list")
    else:
        return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    name = request.form.get("name")
    password = request.form.get("password")
    conn = sqlite3.connect("myTask.db")
    c = conn.cursor()
    c.execute("select id from users where name = ? and password = ?",(name, password))
    id = c.fetchone()
    c.close()
    if id is None:
        # idがなければログインページにリダイレクト
        return redirect("/login")
    else:
        # セッションを発行してidを格納
        session["user_id"] = id
        # idがあればリストページにリダイレクト
        return redirect("/list")
    
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")

# 課題7
@app.route("/delete-account", methods=["POST"])
def delete_account():
    if "user_id" in session:
        user_id = session["user_id"][0]
        conn = sqlite3.connect("myTask.db")
        c = conn.cursor()
        c.execute("delete from task where user_id = ?",(user_id,))
        c.execute("delete from users where id = ?",(user_id,))
        conn.commit()
        c.close()
        session.pop("user_id", None)
        return redirect("/")
    else:
        return redirect("/")
    
# 課題8
@app.route('/upload', methods=["POST"])
def do_upload():
    # type="file"から画像データを取得
    upload = request.files['upload']
    # .filenameで画像のファイル名を取得し、拡張子を判定
    if not upload.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return 'png,jpg,jpeg形式のファイルを選択してください'
    # imgディレクトリまでの相対パスを取得
    save_path = get_save_path()
    print(save_path)
    # 画像データからファイル名を取得
    filename = upload.filename
    # imgディレクトリまでの相対パスと画像のファイル名を結合して保存先を指定。画像ファイルを保存
    upload.save(os.path.join(save_path,filename))
    print(filename)
    user_id = session['user_id'][0]
    conn = sqlite3.connect('myTask.db')
    c = conn.cursor()
    c.execute("update users set prof_img = ? where id=?", (filename,user_id))
    conn.commit()
    conn.close()
    return redirect('/list')

def get_save_path():
    path_dir = "./static/img"
    return path_dir
# 課題8ここまで----------------

@app.errorhandler(404)
def page_not_found(error):
  return render_template('page_not_found.html'), 404



# スクリプトとして直接実行した場合
if __name__ == "__main__":
    # FlaskのWEBアプリケーションを起動
    app.run(debug=True)