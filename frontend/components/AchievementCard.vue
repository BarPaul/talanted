<template>
  <div class="achievement-card bg-white rounded-xl shadow-sm overflow-hidden cursor-pointer">
    <div class="p-5">
      <h3 class="text-lg font-semibold text-gray-800">{{ achievement.name }}</h3>
      <p class="text-gray-500 text-sm mt-1">Ученик #{{ achievement.child_id }}, {{ achievement.place }}</p>
      <div class="mt-4 flex justify-between items-end">
        <span class="text-gray-600 text-xs">{{ formatDate(achievement.date) }}</span>
        <div class="flex justify-between items-end">
          <p class="text-xs text-gray-500 mr-2 mb-1">коэф</p>
          <span class="font-bold text-primary-700 text-2xl">{{ achievement.ratio.toFixed(2) }}</span>
        </div>
      </div>
    </div>
    <div class="bg-gray-50 px-5 py-3 border-t border-gray-100 flex justify-between">
      <span class="text-xs text-gray-500">{{ achievement.type }}</span>
      <span class="text-xs text-gray-500">{{ achievement.level }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  achievement: {
    type: Object,
    required: true
  }
});

const formatDate = (dateString) => {
  try {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  } catch (e) {
    return dateString;
  }
};
</script>