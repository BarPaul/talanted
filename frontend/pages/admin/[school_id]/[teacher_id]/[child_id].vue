<template>
  <div class="p-6">
    <h2 class="text-xl font-semibold text-gray-800 mb-6">Достижения участника: {{ child?.name }}</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <AchievementCard v-for="a in achievements" :key="a.id" :achievement="a" />
    </div>
  </div>
</template>

<script setup>
const { school_id, teacher_id, child_id } = useRoute().params;
const child = ref(null);
const achievements = ref([]);

onMounted(async () => {
  child.value = await $fetch(`/api/child/${child_id}`);
  achievements.value = await $fetch(`/api/achievements?child_id=${child_id}`);
});
</script>