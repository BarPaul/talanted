<template>
  <div class="border border-gray-200 rounded-lg overflow-hidden">
    <button
      class="w-full text-left p-4 font-medium text-gray-800 bg-gray-50 hover:bg-gray-100 flex justify-between items-center"
      @click="isOpen = !isOpen"
    >
      {{ question }}
      <i :class="`fas fa-chevron-${isOpen ? 'up' : 'down'} text-sm`"></i>
    </button>
    <div
      class="accordion-content overflow-hidden transition-all duration-300"
      :style="{ maxHeight: isOpen ? '500px' : '0' }"
    >
      <div class="p-4 text-gray-600"><slot /></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  question: { type: String, required: true }
});

const isOpen = ref(false);
</script>

<style scoped>
.accordion-content {
  will-change: max-height;
}
</style>