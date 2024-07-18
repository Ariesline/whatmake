import requests
import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import pymysql
import cv2
import numpy as np
import os
import re
import pymysql

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
dbhost = '127.0.0.1'
dbuser = 'root'
dbpass = '123456'
dbname = 'editwhat'
app.secret_key = 'iloveeazin'

@app.route('/adduser', methods=['get', 'post'])
def adduser():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username)
    print(password)
    return "已接收用户信息"

# @app.route('/uploadimages', methods=['get', 'post'])
# def uploadimages():
#     username = request.form.get("username")
#     img = request.files['file']
#     picname = img.filename
#     file = img.read()
#
#     file = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
#     imgfile1_path = "./statics/images/" + username + "/"
#     if not os.path.exists(imgfile1_path):
#         os.makedirs(imgfile1_path)
#     img1_path = os.path.join(imgfile1_path, picname)
#     cv2.imwrite(filename=img1_path, img=file)
#     url = "http://127.0.0.1:5000/statics/images/" + username + "/" + picname
#     print(url)
#     conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', charset='utf8')
#     cursor = conn.cursor()
#     conn.commit()
#     cursor.execute('use editwhat')
#     sql = "INSERT INTO `imgpath` (`username`,`url`,`picname`) VALUES('" + str(username) + "','" + str(url) + "','" + str(picname) + "');"
#     print(sql)
#     count = cursor.execute(sql)
#     conn.commit()
#     cursor.close()
#     conn.close()
#
#     tempmap = {"url": url}
#     return jsonify(tempmap)

#API_Key = 'mhfKtcstIBmsnJg0mN7ehmZY'
#Secret_Key = 'rZN7UMnz8zIsWUDKxpjAxWKrdvAsVVPA'

def get_access_token(username):
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor()
    sql = "SELECT api_key, secret_key FROM secret WHERE username = %s"

    try:
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        db.close()

        if result:
            api_key = result[0]
            secret_key = result[1]
            url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
            response = requests.get(url)

            if response.status_code == 200:
                return response.json().get("access_token")
            else:
                print(f"Error {response.status_code}: {response.text}")
                return None
        else:
            print(f"User '{username}' not found in database.")
            return None

    except Exception as e:
        print(f"Error fetching data from database: {str(e)}")
        return None

def call_baidu_api(content, option,username):
    access_token = get_access_token(username)
    if access_token is None:
        return "Failed to get access token."

    option_map = {
        'continuation': "帮我续写下面这段话:",
        'polish': "帮我美化下面这段话:",
        'python': "帮我把下面这个代码转化为python语言:",
        'c': "帮我把下面这个代码转化为c语言:",
        'cpp': "帮我把下面这个代码转化为cpp语言:",
        'java': "帮我把下面这个代码转化为java语言:"
    }

    if option in option_map:
        askcont = option_map[option] + content
    else:
        return "Invalid option."

    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-8k-0329?access_token={access_token}"
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": askcont
            }
        ],
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        result = response.json().get("result")
        if result and (option == 'python' or option == 'c' or option == 'cpp' or option == 'java'):
            # 提取代码部分
            code = extract_code(result)
            return code
        else:
            return result
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


@app.route('/interact', methods=['POST'])
def interact():
    data = request.json
    content = data.get('content')
    username = data.get("username")
    if not content:
        return jsonify({"error": "Content is required"}), 400

    access_token = get_access_token(username)
    if access_token is None:
        return jsonify({"error": "Failed to get access token"}), 500

    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-8k-0329?access_token={access_token}"
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        response_data = response.json()
        result = response_data.get("result")
        if result:
            return jsonify({"response": result}), 200
        else:
            return jsonify({"error": "No result found"}), 500
    else:
        return jsonify({"error": "Failed to get response from Baidu API"}), 500

def extract_code(result):
    # 代码部分被 ``` 包围
    code_match = re.search(r'```(.*?)```', result, re.DOTALL)
    if code_match:
        return code_match.group(1).strip()
    else:
        return "No code found."

def get_identify_status(username):
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor()
    sql = "SELECT identify FROM info WHERE username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    db.close()

    if result:
        return result[0]
    else:
        return None

@app.route('/language-switch', methods=['POST'])
def language_switch():
    data = request.get_json()
    username = data.get("username")
    content = data.get('content')
    option = data.get('option')

    identify_status = get_identify_status(username)
    if identify_status is None:
        return jsonify({'error': '用户不存在'}), 404  # 404 Not Found
    elif identify_status == 0:
        return render_template('popup.html', message='请去设置处绑定 API 账户')

    result = call_baidu_api(content, option,username)

    return jsonify({'result': result})


@app.route('/language-polish', methods=['POST'])
def language_polish():
    data = request.get_json()
    username = data.get("username")
    content = data.get('content')
    option = data.get('option')

    identify_status = get_identify_status(username)
    if identify_status is None:
        return jsonify({'error': '用户不存在'}), 404  # 404 Not Found
    elif identify_status == 0:
        return render_template('popup.html', message='请去设置处绑定 API 账户')

    result = call_baidu_api(content, option,username)

    return jsonify({'result': result})

#从查询用户姓名是否在user表中
def get_user_by_username(username):
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM user WHERE username = %s"
    cursor.execute(sql, (username,))
    user = cursor.fetchone()
    db.close()
    return user

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # 查询数据库中是否存在该用户
    user = get_user_by_username(username)
    if user:
        # 用户存在，检查密码是否匹配
        if user['password'] == password:  # 使用字典方式访问密码字段
            # 密码匹配
            # 保存用户信息到会话
            # session['user_id'] = user['id']
            session['username'] = username
            return jsonify(message="Login successful", username=username)
        else:
            # 密码不匹配
            return jsonify(message="Incorrect password"), 401
    else:
        # 用户不存在
        return jsonify(message="User not found"), 404

def create_user(username, password):
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor()

    try:
        # 插入 user 表
        sql_user = "INSERT INTO user (username, password) VALUES (%s, %s)"
        cursor.execute(sql_user, (username, password))

        # 插入 info 表的默认数据
        default_avatar = "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
        default_gender = "男"
        default_identify = 0

        sql_info = """
        INSERT INTO info (username,uphoto, usex, identify)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_info, (username,  default_avatar, default_gender, default_identify))

        # 提交事务
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        # 关闭数据库连接
        db.close()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "请输入账号、密码！"}), 400

    user = get_user_by_username(username)
    if user:
        return jsonify({"msg": "用户已存在！"}), 400
    else:
        try:
            create_user(username, password)
            return jsonify({"msg": "注册成功！"}), 200
        except Exception as e:
            return jsonify({"msg": f"注册失败：{str(e)}"}), 500


# 设置上传文件目录和允许的文件类型
UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 允许的文件类型检查
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/userinfo', methods=['POST'])
def get_user_info():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'message': 'Username is required'}), 400

    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT username, uphoto, usex, identify FROM info WHERE username = %s", (username,))
    user_info = cursor.fetchone()

    if user_info:
        response = {
            'avatarUrl': user_info['uphoto'],
            'username': user_info['username'],
            'gender': user_info['usex'],
            'identify': user_info['identify']
        }
        return jsonify(response), 200
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/updateProfile', methods=['POST'])
def update_profile():
    username = request.form.get('username')
    gender = request.form.get('gender')
    avatar = request.files.get('avatar')

    if not username or not gender:
        return jsonify({'message': '用户名和性别不能为空'}), 400

    try:
        conn = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname, charset='utf8')
        with conn.cursor() as cursor:
            if avatar:
                # Create directory if not exists
                avatar_path = f"./statics/images/{username}/"
                if not os.path.exists(avatar_path):
                    os.makedirs(avatar_path)

                # Save the uploaded file
                avatar_filename = os.path.join(avatar_path, avatar.filename)
                avatar.save(avatar_filename)

                # Update database with gender and avatar path
                sql = "UPDATE info SET usex = %s, uphoto = %s WHERE username = %s"
                cursor.execute(sql, (gender, avatar_filename, username))
            else:
                # Update database with only gender
                sql = "UPDATE info SET usex = %s WHERE username = %s"
                cursor.execute(sql, (gender, username))

            conn.commit()

        return jsonify({'message': 'Profile updated successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'Error updating profile', 'error': str(e)}), 500

    finally:
        conn.close()

@app.route('/bindAccount', methods=['POST'])
def bind_account():
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    data = request.get_json()
    username = data.get('username')
    api_key = data.get('apiKey')
    secret_key = data.get('secretKey')

    cursor = db.cursor()
    cursor.execute("INSERT INTO secret (username, api_key, secret_key) VALUES (%s, %s, %s)", (username, api_key, secret_key ))
    cursor.execute("UPDATE info SET identify = 1 WHERE username = %s", (username,))
    db.commit()
    return jsonify({'message': 'Account bound successfully'}), 200


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
