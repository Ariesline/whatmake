# 任务 3：基于大模型 API 的智能应用开发

## 目录

[TOC]

## 一、实验任务

> 子任务 1:思考需要使用大模型 API 的地方，拟定开发应用所针对的场景。 
>
> （举一个例子，同学们可以不限于这个场景，大胆地发挥自己的想象：利用大
>
> 模型 API 完成虚拟法律顾问的功能，开发一款法律咨询的应用） 
>
> 后端功能需要完整，不限开发语言，开发框架，但必须使用到大模型 API， 
>
> 并基于此为应用提供一些智能的服务。 
>
> 需要有一个能够展示的前端页面，能够演示同学们所开发的智能应用的主 
>
> 体功能，需要体现出自己使用到大模型 API 能力的地方。 
>
> 子任务 2:往大模型开发技术方向深入，可以考虑利用大模型开发框架（如 
>
> langchain）进行大模型 API 的开发，同时可以考虑使用上 RAG，Agent 这些技 
>
> 术激发大模型的潜能，使得应用更加智能化。 
>
> 往后端开发深入，设计更加复杂的后端架构，可以考虑采取微服务，DDD 
>
> （Domain-Driven Design）等开发方法，并针对实际场景需求增添一些中间件， 
>
> 丰富后端功能。 
>
> 往前端开发深入，可以考虑为应用开发跨平台的前端（支持 Win，IOS， 
>
> Android，Mac 等），也可考虑优化前端页面，使得前端更加炫酷，优美。 



## 二、实验环境

开发环境：windows11

前端：vscode+nodejs+vue+element-plus+tiptap`（Visual Studio Code）`

后端：python+flask`（Pycharm）`

数据库：mysql`（Navicat）`



## 三、实验设计

### 1.智能应用名称

 超超超简单编辑器

### 2.实验设计部分

1.基于数据库的登录注册

2.用户个人信息以及api绑定

3.编辑器界面设计以及基础工具栏

4.编辑器选择内容实现快速的文本美化以及语言转换功能

5.Agent技术实现交互式助手



## 四、实验实现

### 1.前端实现

#### (1)登录页面

登录页面为`/src/veiws/homepage/index.vue`

采用常用的轮播图（Carousel）组件

前端登录请求发送到后端，后端查询数据库中是否有对应的用户名以及密码，满足则登录

并存储用户名到`/src/store/index.ts`中

```vue
login() {
      if (!this.username.trim() || !this.password.trim()) {
        this.msg = '请输入用户名和密码';
        return;
      }

      const url = 'http://127.0.0.1:5000//login';
      axios.post(url, {
        username: this.username,
        password: this.password
      })
      .then(response => {
        console.log('登录成功');
        console.log(response.data);
        localStorage.setItem('username', this.username);
        userStore.setUsername(this.username);
        this.$router.push('/Edit');
      })
      .catch(error => {
        console.error('登录失败', error);
        this.msg = '用户名或密码错误';
      });
    }
```

#### (2)注册页面

注册页面为`/src/veiws/homepage/register.vue`

实现简单注册功能

```vue
const register = () => {
    if (!username.value.trim() || !password.value.trim() || !confirmPassword.value.trim()) {
      msg.value = '请填写所有字段';
      return;
    }
  
    if (password.value !== confirmPassword.value) {
      msg.value = '密码不匹配';
      return;
    }
  
    const data = {
      username: username.value,
      password: password.value,
    };
    axios.post('http://127.0.0.1:5000//register', data)
      .then(response => {
        console.log('注册成功');
        console.log(response.data);
        router.push('/');
      })
      .catch(error => {
        console.error('注册失败', error);
        msg.value = '注册失败，请重试';
      });
  };
```

#### (3)编辑界面

编辑页面为`/src/veiws/edit/index.vue`

包含编辑器界面设计以及基础工具栏，编辑器选择内容实现快速的文本美化以及语言转换功能，Agent技术实现交互式助手三大功能

![1](E:\api\whatmake\whatfront\photo\1.png)

基础工具栏的设计利用的是`tiptap`模块

在`/src/veiws/edit/MenuItem/index.vue`实现顶部加一个功能菜单，设置基本样式

在`/src/veiws/edit/EditorMenu/index.vue`编写图标

文本美化以及语言转换功能

使用大模型 API 进行文本美化和语言转换功能

调用后端有关的路由

```vue
const submit = async () => {
  if (selectedText.value) {
    try {
      const response = await axios.post(`http://127.0.0.1:5000/${selectedFunction.value}`, {
        username: userStore.username,
        content: selectedText.value,
        option: selectedOption.value
      });
      aiResponse.value = response.data.result.split('\n').join('\n'); // 将大模型的响应结果显示在右边，保持换行
    } catch (error) {
      console.error('Error:', error);
    }
  }
};
```

Agent技术实现交互式助手

设计了一个悬浮的小助手，双击可以打开对话框，可以进行智能交流

```vue
<!-- 悬浮式交互式助手 -->
       <div class="agent-icon" @dblclick="toggleAgent" @mousedown="startDrag" :style="{ top: agentTop + 'px', left: agentLeft + 'px' }">
      <img src="../../components/images/1111.gif" alt="悬浮图标" />
    </div>
    <div class="agent-dialog" v-if="showAgent" @mousedown.stop>
      <h3>交互式助手</h3>
      <div class="chat">
        <div v-for="message in messages" :key="message.id" :class="message.role">
          <el-avatar :size="30" :src="message.avatar" />
          <p>{{ message.text }}</p>
        </div>
      </div>
      <div class="input-container">
        <input type="text" v-model="userInput" @keyup.enter="sendMessage" placeholder="请输入您的问题..." />
        <button @click="sendMessage">提交</button>
      </div>
      <button class="close-button" @click="closeAgent">关闭</button>
    </div>
```

#### (4)设置界面

位于`/src/veiws/UserSettings/index.vue`

进行api账号绑定和个人信息更改操作

一个简单的侧边栏设计，包含个人信息模块，要在此处进行api账号的绑定

```vue
<template>
  <div class="container">
    <aside class="sidebar">
      <h2>菜单</h2>
      <ul>
        <li @click="showSection('profile')">个人信息</li>
        <li @click="showSection('history')">历史记录</li>
        <li @click="showSection('recommendations')">推荐</li>
        <li @click="goToEdit">返回</li>
      </ul>
    </aside>
    <main class="content">
      <div v-if="currentSection === 'profile'" class="user-settings">
        <h2>个人信息</h2>
        <div class="form-container">
          <form @submit.prevent="updateProfile" class="form">
            <div class="form-group">
              <label for="avatar">头像</label>
              <input type="file" @change="handleAvatarChange" />
              <img :src="avatarUrl" alt="avatar" class="avatar-preview" />
            </div>
            <div class="form-group">
              <label for="username">用户名</label>
              <input type="text" v-model="username" disabled />
            </div>
            <div class="form-group">
              <label for="gender">性别</label>
              <select v-model="gender" :disabled="!editing">
                <option value="male">男</option>
                <option value="female">女</option>
                <option value="other">其他</option>
              </select>
            </div>
            <div class="form-group">
              <label for="identify">账号绑定</label>
              <input type="text" v-model="identifyStatus" disabled />
              <button v-if="!identify && !binding" @click="startBinding" class="button-primary" type="button">绑定账号</button>
              <div v-if="binding">
                <input type="text" v-model="apiKey" placeholder="API Key" class="input-text" />
                <input type="text" v-model="secretKey" placeholder="Secret Key" class="input-text" />
                <button @click="bindAccount" class="button-primary" type="button">确认绑定</button>
                <button @click="cancelBinding" class="button-secondary" type="button">取消</button>
              </div>
            </div>
            <div v-if="editing">
              <button type="submit" class="button-primary">保存</button>
              <button type="button" @click="cancelEdit" class="button-secondary">取消</button>
            </div>
            <div v-else>
              <button type="button" @click="startEdit" class="button-primary">编辑</button>
            </div>
          </form>
        </div>
      </div>
      <div v-if="currentSection === 'history'" class="history">
        <h2>历史记录</h2>
        <!-- 显示历史记录的内容 -->
        <div class="history-content">
          <p>显示历史记录的文本内容或其他数据。</p>
        </div>
      </div>
      <div v-if="currentSection === 'recommendations'" class="recommendations">
        <h3>推荐教程</h3>
        <ul>
          <li v-for="(tutorial, index) in recommendations" :key="index">
            {{ tutorial }}
          </li>
        </ul>
        <Recommendations />
      </div>
    </main>
  </div>
</template>
```

### 2.后端实现

后端采用的是flask框架

#### 登录

```python
@app.route('/login', methods=['POST'])
def login():
	...
```

#### 注册

```python
@app.route('/register', methods=['POST'])
def register():
	...
```

#### 账号绑定

```python
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
```

#### 调用api大模型实现文本润色和语言切换

由`api_key`和`secret_key`获得`access_token`

```python
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
```

调用百度千帆大模型

![2](E:\api\whatmake\whatfront\photo\2.png)

```python
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
```

对于代码内容进行提取

```python
def extract_code(result):
    # 代码部分被 ``` 包围
    code_match = re.search(r'```(.*?)```', result, re.DOTALL)
    if code_match:
        return code_match.group(1).strip()
    else:
        return "No code found."
```

调用函数

```python
@app.route('/language-switch', methods=['POST'])
def language_switch():
	...
@app.route('/language-polish', methods=['POST'])
def language_polish():
	...
```

#### 调用api大模型实现交互小助手对话

```python
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
```

### 3.数据库实现

![3](E:\api\whatmake\whatfront\photo\3.png)

```mysql
/*
 Navicat MySQL Data Transfer

 Source Server         : test
 Source Server Type    : MySQL
 Source Server Version : 80028
 Source Host           : localhost:3306
 Source Schema         : editwhat

 Target Server Type    : MySQL
 Target Server Version : 80028
 File Encoding         : 65001

 Date: 18/07/2024 09:46:15
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------

-- Table structure for info

-- ----------------------------

DROP TABLE IF EXISTS `info`;
CREATE TABLE `info`  (
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `uphoto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `usex` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `identify` int(1) UNSIGNED ZEROFILL NOT NULL,
  PRIMARY KEY (`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------

-- Table structure for secret

-- ----------------------------

DROP TABLE IF EXISTS `secret`;
CREATE TABLE `secret`  (
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `api_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `secret_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------

-- Table structure for user

-- ----------------------------

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------

-- Triggers structure for table secret

-- ----------------------------

DROP TRIGGER IF EXISTS `update_identify_on_insert`;
delimiter ;;
CREATE TRIGGER `update_identify_on_insert` AFTER INSERT ON `secret` FOR EACH ROW BEGIN
    UPDATE info
    SET identify = 1
    WHERE username = NEW.username;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
```

## 五、实验测试

开启前后端

![4](E:\api\whatmake\whatfront\photo\4.png)

![5](E:\api\whatmake\whatfront\photo\5.png)

进入注册页面进行注册

![6](E:\api\whatmake\whatfront\photo\6.png)

注册完成后登录

![7](E:\api\whatmake\whatfront\photo\7.png)

进入编辑界面，左侧为编辑区，右侧为api响应区。
左侧编辑区可以利用上方工具栏进行文本编辑处理

![8](E:\api\whatmake\whatfront\photo\8.png)

右上方头像点击后进入设置界面
![9](E:\api\whatmake\whatfront\photo\9.png)

设置个人基本信息并绑定api账号![image-20240718105921191]

![10](E:\api\whatmake\whatfront\photo\10.png)
![11](E:\api\whatmake\whatfront\photo\11.png)

选中效果

![12](E:\api\whatmake\whatfront\photo\12.png)

![13](E:\api\whatmake\whatfront\photo\13.png)

提交可以得到语言美化结果
![14](E:\api\whatmake\whatfront\photo\14.png)

提交可以得到语言转换的结果
![15](E:\api\whatmake\whatfront\photo\15.png)

双击悬浮图标可以打开交互式助手，进行询问

![16](E:\api\whatmake\whatfront\photo\16.png)



## 六、实现心得

​	基于我比较熟悉的flask框架搭建了这一个“ 超超超简单编辑器”，实现了利用大模型api方便编辑做笔记。还设计了一个可爱的悬浮图标做小助手。同时，这个简单的智能应用也有很多优化的空间，比如

​	数据库可以部署在云服务器端；

​	历史记录功能和推荐功能可以可以使用基于用户行为的协同过滤（Collaborative Filtering）算法，结合用户的历史转换记录和相似用户的转换记录，推荐相关教程。
