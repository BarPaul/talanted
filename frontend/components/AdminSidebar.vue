<!-- components/AdminSidebar.vue -->
<template>
  <div class="sidebar bg-primary-800 text-white w-64 flex-shrink-0 h-full flex flex-col">
    <div class="p-5 border-b border-primary-700">
      <h2 class="text-xl font-bold flex items-center">
        <i class="fas fa-cog mr-2"></i> Админ-панель
      </h2>
    </div>
    <nav class="p-4 flex-grow">
      <ul class="space-y-2">
        <NuxtLink
          to="/admin/dashboard"
          class="flex items-center p-3 rounded-lg hover:bg-primary-700 text-white"
          active-class="bg-primary-700"
        >
          <i class="fas fa-chart-line mr-3"></i> Дашборд
        </NuxtLink>
        <NuxtLink
          to="/admin/accounts"
          class="flex items-center p-3 rounded-lg hover:bg-primary-700 text-white"
          active-class="bg-primary-700"
        >
          <i class="fas fa-users mr-3"></i> Аккаунты
        </NuxtLink>
        <NuxtLink
          to="/admin/table"
          class="flex items-center p-3 rounded-lg hover:bg-primary-700 text-white"
          active-class="bg-primary-700"
        >
          <i class="fas fa-table mr-3"></i> Отчет
        </NuxtLink>
      </ul>
    </nav>
    
    <!-- Кнопка "Вернуться в сайт" -->
    <div class="p-4 border-t border-primary-700">
      <NuxtLink
        to="/"
        class="flex items-center p-3 rounded-lg hover:bg-primary-700 text-white w-full transition-colors"
      >
        <i class="fas fa-home mr-3"></i> Вернуться в сайт
      </NuxtLink>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>