<!-- pages/index.vue -->
<template>
  <Header></Header>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Достижения</h1>
    </div>
    <Filters @apply="loadAchievements" />
    
    <div v-if="loading" class="flex justify-center py-8">
      <div class="loader border-t-2 border-blue-500 rounded-full w-8 h-8 animate-spin"></div>
    </div>
    
    <div v-if="error" class="text-red-500 text-center py-4">
      {{ error }}
    </div>
    
    <div v-if="!loading && !error && achievements.length === 0" class="text-center py-4">
      Достижения не найдены
    </div>
    
    <div v-if="!loading && !error && achievements.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <AchievementCard v-for="a in achievements" :key="a.id" :achievement="a" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRuntimeConfig } from '#app';

useHead({ title: 'Достижения' });

const achievements = ref([]);
const filters = ref({});
const loading = ref(false);
const error = ref(null);

const loadAchievements = async (newFilters) => {
  loading.value = true;
  error.value = null;
  filters.value = newFilters;
  
  try {
    const apiUrl = useRuntimeConfig().public.apiUrl;
    
    if (!apiUrl) {
      throw new Error('API URL не настроен. Проверьте NUXT_PUBLIC_API_URL в .env файле');
    }
    
    const params = {};
    
    if (filters.value.child_id !== null && filters.value.child_id !== undefined && filters.value.child_id !== '') {
      params.child_id = filters.value.child_id;
    }
    
    if (filters.value.city && filters.value.city !== 'all') {
      params.city = filters.value.city;
    }
    
    if (filters.value.name && filters.value.name.trim() !== '') {
      params.name = filters.value.name;
    }
    
    if (filters.value.achieve_type && filters.value.achieve_type !== 'all') {
      params.achieve_type = filters.value.achieve_type;
    }
    
    const url = `${apiUrl}achievement/all`;
    
    const data = await $fetch(url, { 
      params,
      onResponseError: ({ response }) => {
        error.value = `Ошибка ${response.status}: ${response.statusText}`;
      }
    });
    
    if (!Array.isArray(data)) {
      throw new Error('Получены некорректные данные от сервера');
    }
    
    achievements.value = data;
  } catch (err) {
    error.value = `Не удалось загрузить достижения: ${err.message}`;
    console.error('Ошибка при загрузке достижений:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadAchievements({});
});
</script>

<style scoped>
.loader {
  border-top-color: theme('colors.primary.500');
}
</style>