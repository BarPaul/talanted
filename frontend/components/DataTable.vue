<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th
            v-for="col in columns"
            :key="col"
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
          >
            {{ columnLabels[col] || col }}
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="(row, idx) in data" :key="idx">
          <td
            v-for="col in columns"
            :key="col"
            class="px-6 py-4 whitespace-nowrap text-sm text-gray-700"
          >
            {{ formatValue(row[col], col) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const props = defineProps({
  data: { type: Array, required: true },
  columns: { type: Array, required: true }
});

const columnLabels = {
  place: 'Место',
  city: 'Город',
  school: 'Школа',
  total_ratio: 'Сумма коэффициентов',
  name: 'Название',
  email: 'Email',
  role: 'Роль',
  is_active: 'Активен'
};

const formatValue = (value, key) => {
  if (key === 'is_active') return value ? 'Да' : 'Нет';
  if (key === 'date') return new Date(value).toLocaleDateString();
  if (typeof value === 'number') return value.toFixed(2);
  return value || '—';
};
</script>