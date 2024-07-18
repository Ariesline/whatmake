<!-- Recommendations.vue -->
<template>
    <div>
      <h3>推荐教程</h3>
      <ul>
        <li v-for="(tutorial, index) in recommendations" :key="index">
          {{ tutorial }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        recommendations: [],
      };
    },
    mounted() {
      this.fetchRecommendations();
    },
    methods: {
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
    },
  };
  </script>
  