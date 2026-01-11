<template>
  <div class="bg-white rounded-xl shadow-sm p-6 mb-8">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">Фильтры</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Название</label>
        <input v-model="filters.name" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500" placeholder="Название">
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">ID участника</label>
        <input v-model="filters.child_id" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500" placeholder="ID">
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Город</label>
        <select v-model="filters.city" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500">
          <option value="">Все города</option>
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Направление</label>
        <select v-model="filters.achieve_type" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500">
          <option value="">Все</option>
          <option value="Наука">Наука</option>
          <option value="Искусство">Искусство</option>
          <option value="Спорт">Спорт</option>
        </select>
      </div>
    </div>
    <div class="mt-4 flex justify-end">
      <button @click="applyFilters" class="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">Применить</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import cities from '~/utils/cities';

const filters = ref({
  achieve_type: ''
});
const emit = defineEmits(['apply']);

const applyFilters = () => {
  const processedFilters = { ...filters.value };
  if (!processedFilters.child_id || processedFilters.child_id.trim() === '') {
    delete processedFilters.child_id;
  }
  if (!processedFilters.name || processedFilters.name.trim() === '') {
    delete processedFilters.name;
  }
  if (processedFilters.city === '') {
    delete processedFilters.city;
  }
  if (processedFilters.achieve_type === '') {
    delete processedFilters.achieve_type;
  }

  emit('apply', processedFilters);
};
</script>