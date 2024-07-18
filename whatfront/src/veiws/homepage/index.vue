<template>
  <div class="container">
    <el-carousel class="carousel" :interval="4000" type="card" height="100vh" direction="vertical">
      <el-carousel-item v-for="(item, index) in images" :key="index">
        <img :src="item" alt="carousel-image" class="carousel-image"/>
      </el-carousel-item>
    </el-carousel>
    <div id="maxbox">
      <h1>超超超简单编辑器</h1>
      <h2>Please sign in</h2>
      <div class="inputbox">
        <form @submit.prevent="login" name="frm">
          <div class="inputText">
            <i class="iconfont icon-mine"></i>
            <input type="text" v-model="username" placeholder="用户名" />
          </div>
          <div class="inputText">
            <i class="iconfont icon-lock"></i>
            <input type="password" v-model="password" placeholder="密码" />
            <br />
            <input class="remember" name="remember" type="checkbox" v-model="rememberMe" />
            <span>记住我</span>
          </div>
          <button class="inputButton btn-primary" type="submit">登录</button>
        </form>
        <div v-if="msg" class="error-msg">{{ msg }}</div>
      </div>
      <a href="/register" id="sign_up">去注册</a>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/store/index';
import { storeToRefs } from 'pinia';

// 导入图片
import image1 from '@/assets/images/1.png';
import image2 from '@/assets/images/2.png';
import image3 from '@/assets/images/3.png';
import image4 from '@/assets/images/4.png';
import image5 from '@/assets/images/5.png';
import image6 from '@/assets/images/6.png';

const userStore = useUserStore();

export default {
  data() {
    return {
      username: '',
      password: '',
      rememberMe: true,
      msg: '',
      images: [image1, image2, image3, image4, image5, image6] // 图片数组
    };
  },
  methods: {
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
  }
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

.carousel {
  flex: 1;
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

#sign_up {
  margin-top: 20px; /* 调整注册链接与输入框的距离 */
  display: block; /* 确保链接单独占据一行 */
  color: #f1b6d4; 
  font-size: 17px;
  text-decoration: none;
}

#sign_up:hover {
  text-decoration: underline;
  color: #fcc7e4; 
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持图片纵横比并裁剪以填充容器 */
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
