<template>
  <Header />
  <div class="container mx-auto px-4 py-8">
    <h2 class="text-xl font-semibold text-gray-800 mb-6">Рейтинги</h2>
    
    <div v-if="loading" class="flex justify-center py-8">
      <div class="loader border-t-2 border-blue-500 rounded-full w-8 h-8 animate-spin"></div>
    </div>
    
    <div v-if="error" class="text-red-500 text-center py-4">
      {{ error }}
    </div>
    
    <div v-if="!loading && !error" class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="bg-white rounded-xl shadow-sm p-6">
        <h3 class="text-lg font-medium mb-4">Топ-20 муниципалитетов</h3>
        <DataTable 
          :data="formattedMunicipalities" 
          :columns="['place', 'city', 'total_ratio']"
          :columnNames="{
            place: 'Место',
            city: 'Город',
            total_ratio: 'Баллы'
          }"
        />
      </div>
      
      <div class="bg-white rounded-xl shadow-sm p-6">
        <h3 class="text-lg font-medium mb-4">Топ-50 школ</h3>
        <div class="lg:col-span-2 mb-4">
        <label for="cityFilter" class="block text-sm font-medium text-gray-700 mb-1">Город</label>
        <select 
          id="cityFilter"
          v-model="selectedCity"
          class="w-full md:w-64 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        >
          <option v-for="city in cities" :key="city" :value="city">
            {{ city }}
          </option>
        </select>
      </div>
        <DataTable 
          :data="filteredTop50Schools" 
          :columns="['place', 'name', 'total_ratio']"
          :columnNames="{
            place: 'Место',
            name: 'Школа',
            total_ratio: 'Баллы'
          }"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useHead, useRuntimeConfig } from '#app';
import cities from '~/utils/cities';

useHead({ title: 'Рейтинги' });

const loading = ref(true);
const error = ref(null);
const municipalitiesData = ref([]);
const selectedCity = ref('LUGANSK');
const apiUrl = useRuntimeConfig().public.apiUrl;

const buildUrl = (baseUrl, path) => {
  if (!baseUrl) {
    throw new Error('API URL не настроен. Проверьте NUXT_PUBLIC_API_URL в .env файле');
  }
  
  const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${cleanBaseUrl}${cleanPath}`;
};

const formattedMunicipalities = computed(() => {
  return municipalitiesData.value.map(m => ({
    place: Math.floor(m.place),
    city: m.city,
    total_ratio: m.total_ratio.toFixed(2)
  })).slice(0, 20);
});

const allSchools = computed(() => {
  let schools = [];
  
  municipalitiesData.value.forEach(m => {
    schools = [...schools, ...m.schools.map(s => ({
      ...s,
      city: m.city,
      total_ratio: parseFloat(s.total_ratio.toFixed(2))
    }))];
  });
  
  schools.sort((a, b) => b.total_ratio - a.total_ratio);
  
  return schools;
});

const filteredTop50Schools = computed(() => {
  let schools = allSchools.value;
  
  if (selectedCity.value !== 'all') {
    schools = schools.filter(school => school.city === selectedCity.value);
  }
  
  return schools.slice(0, 50).map((school, index) => ({
    ...school,
    place: index + 1
  }));
});

onMounted(async () => {
  try {
    const response = await $fetch(buildUrl(apiUrl, '/stats/ratings/municipalities'));
    
    municipalitiesData.value = response.municipalities;
  } catch (err) {
    error.value = 'Не удалось загрузить рейтинги. Попробуйте позже.';
    console.error('Ошибка при загрузке рейтингов:', err);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.loader {
  border-top-color: theme('colors.primary.500');
}
</style>