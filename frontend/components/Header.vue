<!-- components/Header.vue -->
<template>
  <header class="bg-white shadow-sm sticky top-0 z-50">
    <div class="container mx-auto px-4 py-3 flex justify-between items-center">
      <NuxtLink to="/" class="flex items-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
        </svg>
        <span class="text-xl font-bold text-gray-800">Портал достижений</span>
      </NuxtLink>
      
      <nav class="hidden md:flex justify-center flex-1">
        <div class="flex space-x-6">
          <NuxtLink 
            to="/" 
            class="text-gray-700 hover:text-primary-600 font-medium transition-colors"
            active-class="text-primary-600 font-semibold"
          >
            Достижения
          </NuxtLink>
          <NuxtLink 
            to="/ratings" 
            class="text-gray-700 hover:text-primary-600 font-medium transition-colors"
            active-class="text-primary-600 font-semibold"
          >
            Рейтинги
          </NuxtLink>
          <NuxtLink 
            to="/faq" 
            class="text-gray-700 hover:text-primary-600 font-medium transition-colors"
            active-class="text-primary-600 font-semibold"
          >
            ЧаВО
          </NuxtLink>
        </div>
      </nav>
      
      <div class="flex items-center space-x-4">
        <!-- Кнопка мобильного меню -->
        <button 
          v-if="!isMobileMenuOpen" 
          @click="isMobileMenuOpen = true"
          class="md:hidden text-gray-700 hover:text-gray-900"
          aria-label="Открыть меню"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        
        <!-- Кнопка закрытия мобильного меню -->
        <button 
          v-else
          @click="isMobileMenuOpen = false"
          class="md:hidden text-gray-700 hover:text-gray-900"
          aria-label="Закрыть меню"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        
        <!-- Кнопка аутентификации -->
        <div v-if="isAuthenticated">
          <NuxtLink 
            to="/admin/dashboard" 
            class="bg-primary-100 hover:bg-primary-200 text-primary-700 font-medium py-2 px-4 rounded-lg transition-colors mr-2"
          >
            Личный кабинет
          </NuxtLink>
          <button 
            @click="logout"
            class="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium p-2 rounded-lg transition-colors"
            aria-label="Выйти"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        <AuthModal v-else />
      </div>
    </div>
    
    <!-- Мобильное меню -->
    <transition name="slide">
      <div v-if="isMobileMenuOpen" class="md:hidden bg-white border-t border-gray-100">
        <div class="container mx-auto px-4 py-3 flex flex-col space-y-4">
          <NuxtLink 
            to="/" 
            class="text-gray-700 hover:text-primary-600 font-medium py-1"
            active-class="text-primary-600 font-semibold"
            @click="isMobileMenuOpen = false"
          >
            Достижения
          </NuxtLink>
          <NuxtLink 
            to="/ratings" 
            class="text-gray-700 hover:text-primary-600 font-medium py-1"
            active-class="text-primary-600 font-semibold"
            @click="isMobileMenuOpen = false"
          >
            Рейтинги
          </NuxtLink>
          <NuxtLink 
            to="/faq" 
            class="text-gray-700 hover:text-primary-600 font-medium py-1"
            active-class="text-primary-600 font-semibold"
            @click="isMobileMenuOpen = false"
          >
            ЧаВО
          </NuxtLink>
          
          <div v-if="isAuthenticated" class="pt-2 border-t border-gray-100">
            <NuxtLink 
              to="/admin/dashboard" 
              class="block w-full text-left bg-primary-100 hover:bg-primary-200 text-primary-700 font-medium py-2 px-4 rounded-lg mb-2"
              @click="isMobileMenuOpen = false"
            >
              Личный кабинет
            </NuxtLink>
            <button 
              @click="logout; isMobileMenuOpen = false"
              class="w-full text-left bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd" />
              </svg>
              Выйти
            </button>
          </div>
          <AuthModal v-else />
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useNuxtApp, navigateTo, useState } from '#app';

// Состояние аутентификации
const auth = useState('auth', () => ({
  token: null,
  user: null
}));
// Вычисляемое свойство для проверки аутентификации
const isAuthenticated = computed(() => !!auth.value.token);

// Состояние мобильного меню
const isMobileMenuOpen = ref(false);

// Функция выхода
const logout = () => {
  // Очистка состояния аутентификации
  auth.value = {
    token: null,
    user: null
  };
  
  // Очистка токена из localStorage
  if (process.client) {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
  }
  
  // Перенаправление на главную страницу
  navigateTo('/');
};

// Закрытие мобильного меню при изменении маршрута
const nuxtApp = useNuxtApp();
nuxtApp.hooks.hook('page:start', () => {
  isMobileMenuOpen.value = false;
});

// Закрытие мобильного меню при клике вне его области
const handleOutsideClick = (e) => {
  const header = e.target.closest('header');
  if (!header && isMobileMenuOpen.value) {
    isMobileMenuOpen.value = false;
  }
};

// Закрытие мобильного меню при нажатии Escape
const handleEsc = (e) => {
  if (e.key === 'Escape' && isMobileMenuOpen.value) {
    isMobileMenuOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleOutsideClick);
  document.addEventListener('keydown', handleEsc);
  
  // Проверяем, есть ли токен в localStorage при загрузке компонента
  if (process.client) {
    const token = localStorage.getItem('auth_token');
    const user = localStorage.getItem('auth_user');
    
    if (token) {
      auth.value = {
        token: token,
        user: user ? JSON.parse(user) : null
      };
    }
  }
});

onUnmounted(() => {
  document.removeEventListener('click', handleOutsideClick);
  document.removeEventListener('keydown', handleEsc);
});
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}
</style>