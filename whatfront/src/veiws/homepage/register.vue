<template>
    <div class="container">
      <div id="maxbox">
        <h1>注册</h1>
        <h2>Please register</h2>
        <div class="inputbox">
          <form @submit.prevent="register" name="frm">
            <div class="inputText">
              <i class="iconfont icon-mine"></i>
              <input type="text" v-model="username" placeholder="用户名" />
            </div>
            <div class="inputText">
              <i class="iconfont icon-lock"></i>
              <input type="password" v-model="password" placeholder="密码" />
            </div>
            <div class="inputText">
              <i class="iconfont icon-lock"></i>
              <input type="password" v-model="confirmPassword" placeholder="确认密码" />
            </div>
            <button class="inputButton btn-primary" type="submit">注册</button>
          </form>
          <div v-if="msg" class="error-msg">{{ msg }}</div>
        </div>
        <router-link to="/" id="sign_in">去登录</router-link>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  const username = ref('');
  const password = ref('');
  const confirmPassword = ref('');
  const msg = ref('');
  
  const router = useRouter();
  
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
  </script>
  
  <style scoped>
  body {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    background-color: #ffe4e1; /* 浅粉色背景 */
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* 充满整个视口 */
    font-family: Arial, sans-serif; /* 设置字体 */
  }
  
  .container {
    display: flex;
    height: 100%;
    width: 100%;
  }
  
  #maxbox {
    padding: 20px 50px;
    text-align: center;
    max-width: 400px; /* 最大宽度 */
    width: 100%; /* 宽度充满父容器 */
    border-radius: 10px;
    background-color: rgba(0, 0, 0, 0.56); /* 半透明黑色背景 */
    margin: auto; /* 居中 */
  }
  
  #maxbox h1 {
    color: white;
    font-size: 30px;
    margin-top: 40px; /* 调整标题与顶部的距离 */
    margin-bottom: 10px; /* 调整标题与输入框的距离 */
    border-bottom: solid 1px white;
  }
  
  #maxbox h2 {
    font-weight: 700;
    color: white;
    margin-bottom: 20px; /* 调整副标题与输入框的距离 */
  }
  
  #maxbox .inputbox {
    margin-top: 20px;
  }
  
  #maxbox .inputText {
    margin-top: 15px; /* 调整输入框组件之间的距离 */
  }
  
  #maxbox .inputText i {
    color: white;
    font-size: 18px;
    margin-right: 10px;
  }
  
  #maxbox .inputText input {
    border: 0;
    padding: 6px;
    border-bottom: 1px solid white;
    background-color: rgba(255, 192, 203, 0.5); /* 粉色半透明 */
    color: white;
  }
  
  #maxbox .inputbox .inputButton {
    margin-top: 20px;
    width: 100%; /* 按钮宽度充满父容器 */
    height: 40px; /* 调整按钮高度 */
    border-radius: 25px;
    color: white;
    background-color: #ffdced;
    cursor: pointer;
  }
  
  #maxbox .inputbox .inputButton:hover {
    background-color: #ffd8ed; 
  }
  
  .error-msg {
    color: white;
    margin-top: 10px; /* 调整错误信息与输入框的距离 */
  }
  
  #sign_in {
    margin-top: 20px; /* 调整注册链接与输入框的距离 */
    display: block; /* 确保链接单独占据一行 */
    color: #f1b6d4; 
    font-size: 17px;
    text-decoration: none;
  }
  
  #sign_in:hover {
    text-decoration: underline;
    color: #fcc7e4; 
  }
  </style>
  