<template>
  <div class="EditMain">
    <div class="editor-container" @mouseup="handleMouseUp">
      <div class="editor">
        <div class="editorcard">
          <div class="toptools">
            <EditorMenu :editor="editor" />
          </div>
          <div class="editcont">
            <EditorContent
              @scroll="hasscroll"
              @mousedown="notsee"
              @mousemove="mousemove"
              style="padding: 8px; overflow-y: auto;"
              :editor="editor"
            />
            <div v-if="showSelectionBox" class="selection-box" :style="selectionBoxStyle">
              <button @click="handleSelection">选择</button>
            </div>
          </div>
          <div class="bottomcount">
            字数统计: {{ editor?.storage.characterCount.characters() }}
          </div>
        </div>
      </div>
    </div>
    <div class="response-container">
      <div class="response">
        <div class="tools">
          <div class="select-tools">
            <select v-model="selectedFunction">
              <option value="language-switch">语言切换</option>
              <option value="language-polish">语言润色</option>
            </select>
            <select v-model="selectedOption">
              <option v-if="selectedFunction === 'language-switch'" value="python">Python</option>
              <option v-if="selectedFunction === 'language-switch'" value="c">C</option>
              <option v-if="selectedFunction === 'language-switch'" value="cpp">C++</option>
              <option v-if="selectedFunction === 'language-switch'" value="java">Java</option>
              <option v-if="selectedFunction === 'language-polish'" value="continuation">续写</option>
              <option v-if="selectedFunction === 'language-polish'" value="polish">美化</option>
            </select>
            <button @click="submit">提交</button>
          </div>
          <div class="avatar-container">
            <el-avatar :size="50" :src="avatarUrl" class="avatar" @click="toggleMenu" />
            <div v-if="showMenu" class="menu">
              <div @click="goToSettings">设置</div>
              <div @click="logout">退出</div>
            </div>
          </div>
        </div>
        <div class="response-content">
          <pre>{{ aiResponse }}</pre>
        </div>
      </div>
    </div>
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router'; // 引入 useRouter
import axios from 'axios';
import { useEditor, EditorContent } from '@tiptap/vue-3';
import StarterKit from '@tiptap/starter-kit';
import CharacterCount from '@tiptap/extension-character-count';
import EditorMenu from './EditorMenu/index.vue';

import userAvatar from '@/assets/images/user.png';
import agentAvatar from '@/assets/images/avatar.png';
import { useUserStore } from '@/store/index';

const userStore = useUserStore();
const router = useRouter(); // 获取 router 对象

const editor = useEditor({
  content: '',
  extensions: [
    StarterKit,
    CharacterCount.configure({ limit: 10000 })
  ]
});

const aiResponse = ref('');
const selectedFunction = ref('language-switch');
const selectedOption = ref('python');
const selectedText = ref('');

const showSelectionBox = ref(false);
const selectionBoxStyle = reactive({ top: '0px', left: '0px' });
const showMenu = ref(false);
const showAgent = ref(false);
const avatarUrl = ref('https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png');


const messages = ref([
  { id: 1, role: 'agent', text: '欢迎使用交互式助手！请问有什么可以帮您的吗？', avatar: agentAvatar }
]);
const userInput = ref('');

const handleMouseUp = (event) => {
  const selection = window.getSelection();
  if (selection && selection.toString().length > 0) {
    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    selectionBoxStyle.top = rect.top + window.scrollY + 'px';
    selectionBoxStyle.left = rect.left + window.scrollX + 'px';
    showSelectionBox.value = true;
  } else {
    showSelectionBox.value = false;
  }
};

const handleSelection = () => {
  const selection = window.getSelection();
  if (selection) {
    selectedText.value = selection.toString();
    aiResponse.value = selectedText.value;
    showSelectionBox.value = false;
  }
};

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

const toggleMenu = () => {
  showMenu.value = !showMenu.value;
};

const toggleAgent = () => {
  showAgent.value = !showAgent.value;
};

const closeAgent = () => {
  showAgent.value = false;
};

let startX = 0;
let startY = 0;
let agentTop = ref(20);
let agentLeft = ref(20);

const startDrag = (event) => {
  startX = event.clientX - event.target.getBoundingClientRect().left;
  startY = event.clientY - event.target.getBoundingClientRect().top;

  const moveHandler = (e) => {
    agentTop.value = e.clientY - startY;
    agentLeft.value = e.clientX - startX;
  };

  const upHandler = () => {
    document.removeEventListener('mousemove', moveHandler);
    document.removeEventListener('mouseup', upHandler);
  };

  document.addEventListener('mousemove', moveHandler);
  document.addEventListener('mouseup', upHandler);
};

const sendMessage = async () => {
  if (userInput.value.trim() !== '') {
    const userMessage = { id: Date.now(), role: 'user', text: userInput.value, avatar: userAvatar };
    messages.value.push(userMessage);

    try {
      const response = await axios.post('http://127.0.0.1:5000/interact', {
        content: userInput.value,
        username: userStore.username,
      });
      const agentMessage = { id: Date.now() + 1, role: 'agent', text: response.data.response, avatar: agentAvatar };
      messages.value.push(agentMessage);
    } catch (error) {
      console.error('Error:', error);
    }
    
    userInput.value = '';
  }
};

const goToSettings = () => {
  // 使用 router 对象进行路由跳转
  router.push('/settings');
};

const logout = () => {
  // 退出登录的逻辑
  router.push('/');
  console.log('退出登录');
};
</script>

<style scoped>
.EditMain {
  display: flex;
  height: 100vh;
  max-width: 100vw;
  overflow: hidden;
}

.editor-container {
  background-color: #ffcccb;
  width: 50%;
  padding: 10px;
  box-sizing: border-box;
  position: relative;
  overflow: hidden;
}

.response-container {
  background-color: #ffffcc;
  width: 50%;
  padding: 10px;
  box-sizing: border-box;
  overflow: hidden;
}

.editor {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.editorcard {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  border: 1px solid #ccc;
}

.toptools {
  padding: 10px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #ccc;
}

.bottomcount {
  position: absolute; /* 绝对定位 */
  bottom: 0; /* 定位到底部 */
  padding: 10px;
  width: 93.5%; 
  background-color: #f9f9f9;
  border-top: 1px solid #ccc;
  text-align: center;
}

.response {
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid #ccc;
}

.tools {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #ccc;
}

.select-tools {
  display: flex;
  align-items: center;
}

.avatar-container {
  position: relative;
}

.avatar {
  cursor: pointer;
  border-radius: 50%; /* 将头像裁剪为圆形 */
  object-fit: cover; /* 确保头像内容不会被拉伸 */
}

.menu {
  position: absolute;
  top: 60px;
  right: 0;
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 10px;
  display: flex;
  flex-direction: row;
  z-index: 1000;
}

.menu div {
  padding: 10px;
  cursor: pointer;
}

.menu div:hover {
  background-color: #f0f0f0;
}

.agent-icon {
  position: fixed;
  top: 20px;
  left: 20px;
  width: 50px;
  height: 50px;
  cursor: move;
  z-index: 1000;
}

.agent-dialog {
  position: fixed;
  top: 50px;
  left: 50px;
  width: 300px;
  background-color: white;
  border: 1px solid #ccc;
  padding: 20px;
  z-index: 1000;
}

.chat {
  max-height: 200px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.agent, .user {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.agent p, .user p {
  margin: 0 10px;
  padding: 10px;
  border-radius: 10px;
  background-color: #f0f0f0;
  flex-grow: 1; /* 确保消息文本不会影响头像大小 */
}
.input-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.input-container input {
  flex: 1;
  margin-right: 10px;
  padding: 5px;
}

.input-container button {
  padding: 5px 10px;
}

.close-button {
  display: block;
  width: 100%;
  margin-top: 10px;
  padding: 10px;
  text-align: center;
  background-color: #f0f0f0;
  border: none;
  cursor: pointer;
}

.close-button:hover {
  background-color: #e0e0e0;
}
</style>