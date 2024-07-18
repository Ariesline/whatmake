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

<script>
import axios from 'axios';
import { useUserStore } from '@/store/index';

const userStore = useUserStore();
export default {
  data() {
    return {
      avatarUrl: '', // 用户头像URL
      username: userStore.username, // 用户名
      gender: 'male', // 用户性别
      identify: 0, // 是否绑定账号
      editing: false, // 是否处于编辑模式
      currentSection: 'profile', // 当前显示的部分
      apiKey: '',
      secretKey: '',
      binding: false, // 是否正在绑定账号
    };
  },
  computed: {
    identifyStatus() {
      return this.identify ? '已绑定' : '未绑定';
    }
  },
  mounted() {
    // 从后端获取用户信息并初始化数据
    this.fetchUserProfile();
  },
  methods: {
    fetchUserProfile() {
    axios.post('http://127.0.0.1:5000/userinfo', {
        username: this.username
    }).then(response => {
        const data = response.data;
        this.avatarUrl = data.avatarUrl;
        this.username = data.username;
        this.gender = data.gender;
        this.identify = data.identify;
    }).catch(error => {
        console.error('Error fetching user profile:', error);
    });
    },

    handleAvatarChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.avatarUrl = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    goToEdit(){
      this.$router.push('/Edit');
    },
    startEdit() {
      // 进入编辑模式
      this.editing = true;
    },
    cancelEdit() {
      // 取消编辑，恢复到非编辑状态
      this.editing = false;
      // 重新获取用户信息，恢复原始状态
      this.fetchUserProfile();
    },
    updateProfile(event) {
      // 构造表单数据
      let formData = new FormData();
      formData.append("avatar", event.target.files[0]); // 添加头像文件到表单数据中
      formData.append("gender", this.gender);

      // 发送请求到服务器，上传用户信息和头像
      axios.post('http://127.0.0.1:5000/updateProfile', formData)
        .then(response => {
          console.log(response.data);
          // 更新成功后，退出编辑模式
          this.editing = false;
        })
        .catch(error => {
          console.error(error);
          // 处理错误响应
        });
    },
    startBinding() {
      // 开始绑定账号
      this.binding = true;
    },
    cancelBinding() {
      // 取消绑定账号
      this.binding = false;
      this.apiKey = '';
      this.secretKey = '';
    },
    bindAccount() {
      // 发送绑定账号请求
      axios.post('http://127.0.0.1:5000/bindAccount', {
        username:this.username,
        apiKey: this.apiKey,
        secretKey: this.secretKey
      })
      .then(response => {
        console.log(response.data);
        this.identify = 1; // 更新为已绑定
        this.binding = false;
        this.apiKey = '';
        this.secretKey = '';
      })
      .catch(error => {
        console.error(error);
        // 处理错误响应
      });
    },
    showSection(section) {
      this.currentSection = section;
    },
    fetchRecommendations() {
        // 假设后端API返回推荐结果
        axios.get('http://127.0.0.1:5000/recommendations', {
          params: {
            username: this.$store.state.username,
          },
        })
        .then(response => {
          this.recommendations = response.data;
        })
        .catch(error => {
          console.error('Error fetching recommendations:', error);
        });
      },
  }
};
</script>

<style scoped>
.container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 200px;
  background-color: #f9cbdb; /* 粉色侧边栏背景 */
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar h2 {
  margin-top: 0;
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
}

.sidebar li {
  margin: 10px 0;
  cursor: pointer;
}

.content {
  flex: 1;
  padding: 20px;
  background-color: #fffafa; /* 淡粉色背景 */
}

.user-settings {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-container {
  width: 300px;
}

.form-group {
  margin-bottom: 15px;
}

.avatar-preview {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-top: 10px;
  border: 2px solid #f48fb1; /* 粉色边框 */
}

.button-primary {
  background-color: #f48fb1; /* 粉色按钮背景 */
  border-color: #f48fb1; /* 粉色按钮边框 */
  color: #fff;
  padding: 8px 16px;
  cursor: pointer;
}

.button-primary:hover {
  background-color: #ff77a9; /* 深粉色悬停背景 */
}

.button-secondary {
  background-color: transparent;
  border: 1px solid #ccc;
  color: #333;
  padding: 8px 16px;
  cursor: pointer;
  margin-left: 10px;
}

.history-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.recommendations {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
