<!-- components/AuthModal.vue -->
<template>
  <div>
    <button 
      v-if="!auth.isAuthenticated"
      @click="isOpen = true" 
      class="bg-primary-600 hover:bg-primary-700 text-white p-2 rounded-lg transition-colors"
      aria-label="Войти"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    </button>

    <div 
      v-if="isOpen" 
      class="fixed inset-0 z-50 overflow-y-auto"
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
    >
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div 
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          @click="closeModal"
          aria-hidden="true"
        ></div>

        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        
        <div class="relative inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="flex justify-between items-center px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">
              {{ currentForm === 'login' ? 'Вход' : currentForm === 'register' ? 'Регистрация' : 'Восстановление пароля' }}
            </h3>
            <button 
              @click="closeModal"
              class="text-gray-400 hover:text-gray-500 focus:outline-none"
              aria-label="Закрыть"
            >
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div v-if="currentForm === 'login'" class="p-6">
            <form @submit.prevent="handleLogin">
              <div class="mb-4">
                <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input 
                  id="email" 
                  type="email" 
                  v-model="loginForm.email"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="example@email.com"
                  required
                >
              </div>
              
              <div class="mb-6">
                <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
                <input 
                  id="password" 
                  type="password" 
                  v-model="loginForm.password"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  required
                >
              </div>
              
              <button 
                type="submit"
                class="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
              >
                Войти
              </button>
            </form>
            
            <div class="mt-6 text-center">
              <span class="text-gray-600">Нет аккаунта? </span>
              <button 
                @click="switchForm('register')"
                class="font-medium text-primary-600 hover:text-primary-500"
              >
                Зарегистрироваться
              </button>
            </div>
            
            <div class="mt-2 text-center">
              <button 
                @click="switchForm('forgot')"
                class="font-medium text-primary-600 hover:text-primary-500 text-sm"
              >
                Забыли пароль?
              </button>
            </div>
          </div>

          <div v-if="currentForm === 'register'" class="p-6">
            <form @submit.prevent="handleRegister">
              <div class="mb-4">
                <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input 
                  id="email" 
                  type="email" 
                  v-model="registerForm.email"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="example@email.com"
                  required
                >
              </div>
              
              <div class="mb-4">
                <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
                <input 
                  id="password" 
                  type="password" 
                  v-model="registerForm.password"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  minlength="8"
                  required
                >
              </div>
              
              <div class="mb-4">
                <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">Подтвердите пароль</label>
                <input 
                  id="confirmPassword" 
                  type="password" 
                  v-model="registerForm.confirmPassword"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  minlength="8"
                  required
                >
              </div>
              
              <div class="mb-4">
                <label for="city" class="block text-sm font-medium text-gray-700 mb-1">Город</label>
                <select 
                  id="city" 
                  v-model="registerForm.city"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  required
                >
                  <option value="">Выберите город</option>
                  <option v-for="city in cities" :key="city" :value="city">
                    {{ city }}
                  </option>
                </select>
              </div>
              
              <div class="mb-4">
                <label for="institutionName" class="block text-sm font-medium text-gray-700 mb-1">Название учреждения</label>
                <input 
                  id="institutionName" 
                  type="text" 
                  v-model="registerForm.institutionName"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  required
                >
              </div>
              
              <div class="mb-6">
                <label class="block text-sm font-medium text-gray-700 mb-1">Тип учреждения</label>
                <div class="flex space-x-4">
                  <label class="inline-flex items-center">
                    <input 
                      type="radio" 
                      v-model="registerForm.institutionType" 
                      value="school"
                      class="text-primary-600 focus:ring-primary-500"
                      required
                    >
                    <span class="ml-2 text-sm text-gray-700">Школа</span>
                  </label>
                  <label class="inline-flex items-center">
                    <input 
                      type="radio" 
                      v-model="registerForm.institutionType" 
                      value="municipality"
                      class="text-primary-600 focus:ring-primary-500"
                      required
                    >
                    <span class="ml-2 text-sm text-gray-700">Муниципалитет</span>
                  </label>
                </div>
              </div>
              
              <button 
                type="submit"
                class="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
              >
                Зарегистрироваться
              </button>
            </form>
            
            <div class="mt-6 text-center">
              <span class="text-gray-600">Уже есть аккаунт? </span>
              <button 
                @click="switchForm('login')"
                class="font-medium text-primary-600 hover:text-primary-500"
              >
                Войти
              </button>
            </div>
          </div>

          <div v-if="currentForm === 'forgot'" class="p-6">
            <form @submit.prevent="handleForgotPassword">
              <div class="mb-4">
                <label for="forgotEmail" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input 
                  id="forgotEmail" 
                  type="email" 
                  v-model="forgotForm.email"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="example@email.com"
                  required
                >
              </div>
              
              <div class="mb-4">
                <label for="oldPassword" class="block text-sm font-medium text-gray-700 mb-1">Старый пароль</label>
                <input 
                  id="oldPassword" 
                  type="password" 
                  v-model="forgotForm.oldPassword"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  required
                >
              </div>
              
              <div class="mb-6">
                <label for="newPassword" class="block text-sm font-medium text-gray-700 mb-1">Новый пароль</label>
                <input 
                  id="newPassword" 
                  type="password" 
                  v-model="forgotForm.newPassword"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  minlength="8"
                  required
                >
              </div>
              
              <button 
                type="submit"
                class="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
              >
                Изменить пароль
              </button>
            </form>
            
            <div class="mt-6 text-center">
              <button 
                @click="switchForm('login')"
                class="font-medium text-primary-600 hover:text-primary-500"
              >
                Вернуться ко входу
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useNuxtApp, navigateTo, useRuntimeConfig, useState } from '#app';
import cities from '~/utils/cities';

const auth = useState('auth', () => ({
  token: null,
  user: null,
  isAuthenticated: false
}));

const isAuthenticated = computed(() => auth.value.isAuthenticated);

const isOpen = ref(false);
const currentForm = ref('login');

const loginForm = ref({
  email: '',
  password: ''
});

const registerForm = ref({
  email: '',
  password: '',
  confirmPassword: '',
  city: '',
  institutionName: '',
  institutionType: null
});

const forgotForm = ref({
  email: '',
  oldPassword: '',
  newPassword: ''
});

const apiUrl = useRuntimeConfig().public.apiUrl;

const buildUrl = (baseUrl, path) => {
  if (!baseUrl) {
    throw new Error('API URL не настроен. Проверьте NUXT_PUBLIC_API_URL в .env файле');
  }
  
  const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${cleanBaseUrl}${cleanPath}`;
};

const closeModal = () => {
  isOpen.value = false;
  currentForm.value = 'login';
  resetForms();
};

const switchForm = (formName) => {
  currentForm.value = formName;
};

const handleLogin = async () => {
  try {
    const url = buildUrl(apiUrl, '/auth/login');
    const response = await $fetch(url, {
      method: 'POST',
      body: {
        email: loginForm.value.email,
        password: loginForm.value.password
      }
    });
    
        if (!response.access_token) {
      throw new Error('Неверный ответ от сервера');
    }
    
        auth.value = {
      token: response.access_token,
      user: null,
      isAuthenticated: true
    };
    
        if (process.client) {
      localStorage.setItem('auth_token', response.access_token);
      localStorage.setItem('auth_user', JSON.stringify(null));
    }
    
        closeModal();
    
        navigateTo('/admin/dashboard');
  } catch (err) {
    let errorMessage = 'Ошибка входа: ';
    
    try {
            if (err.data && err.data.detail) {
        errorMessage += err.data.detail;
      } else if (err.response && err.response._data && err.response._data.detail) {
        errorMessage += err.response._data.detail;
      } else if (typeof err === 'string' && err.includes('detail')) {
                try {
          const errorObj = JSON.parse(err);
          errorMessage += errorObj.detail;
        } catch (e) {
          errorMessage += 'Неверный email или пароль';
        }
      } else {
        errorMessage += 'Неверный email или пароль';
      }
    } catch (parseError) {
      errorMessage += 'Неверный email или пароль';
    }
    
    alert(errorMessage);
    console.error('Ошибка при входе:', err);
  }
};

const handleRegister = async () => {
  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    alert('Пароли не совпадают');
    return;
  }
  
  if (!registerForm.value.institutionType) {
    alert('Пожалуйста, выберите тип учреждения');
    return;
  }
  
  if (!registerForm.value.city) {
    alert('Пожалуйста, выберите город');
    return;
  }
  
  try {
    const url = buildUrl(apiUrl, '/auth/register');
    const response = await $fetch(url, {
      method: 'POST',
      body: {
        email: registerForm.value.email,
        password: registerForm.value.password,
        city: registerForm.value.city,
        name: registerForm.value.institutionName,
        role: registerForm.value.institutionType === 'school' ? 'school' : 'mun'
      }
    });

        if (!response.access_token) {
      throw new Error('Неверный ответ от сервера');
    }
    
        auth.value = {
      token: response.access_token,
      user: null,
      isAuthenticated: true
    };
    
        if (process.client) {
      localStorage.setItem('auth_token', response.access_token);
      localStorage.setItem('auth_user', JSON.stringify(null));
    }
    
    alert('Регистрация прошла успешно!');
    
        closeModal();
    
        navigateTo('/admin/dashboard');
  } catch (err) {
    let errorMessage = 'Ошибка регистрации: ';
    
    try {
            if (err.data && err.data.detail) {
        errorMessage += err.data.detail;
      } else if (err.response && err.response._data && err.response._data.detail) {
        errorMessage += err.response._data.detail;
      } else if (typeof err === 'string' && err.includes('detail')) {
                try {
          const errorObj = JSON.parse(err);
          errorMessage += errorObj.detail;
        } catch (e) {
          errorMessage += 'Произошла ошибка при регистрации';
        }
      } else {
        errorMessage += 'Произошла ошибка при регистрации';
      }
    } catch (parseError) {
      errorMessage += 'Произошла ошибка при регистрации';
    }
    
    alert(errorMessage);
    console.error('Ошибка при регистрации:', err);
  }
};

const handleForgotPassword = async () => {
  try {
    const url = buildUrl(apiUrl, '/auth/change-password');
    await $fetch(url, {
      method: 'POST',
      body: {
        email: forgotForm.value.email,
        old_password: forgotForm.value.oldPassword,
        new_password: forgotForm.value.newPassword
      }
    });
    
    alert('Пароль успешно изменен!');
    switchForm('login');
  } catch (err) {
    let errorMessage = 'Ошибка изменения пароля: ';
    
    try {
            if (err.data && err.data.detail) {
        errorMessage += err.data.detail;
      } else if (err.response && err.response._data && err.response._data.detail) {
        errorMessage += err.response._data.detail;
      } else {
        errorMessage += 'Произошла ошибка';
      }
    } catch (parseError) {
      errorMessage += 'Произошла ошибка';
    }
    
    alert(errorMessage);
    console.error('Ошибка при изменении пароля:', err);
  }
};

const resetForms = () => {
  loginForm.value = {
    email: '',
    password: ''
  };
  
  registerForm.value = {
    email: '',
    password: '',
    confirmPassword: '',
    city: '',
    institutionName: '',
    institutionType: null
  };
  
  forgotForm.value = {
    email: '',
    oldPassword: '',
    newPassword: ''
  };
};

const handleEsc = (e) => {
  if (e.key === 'Escape' && isOpen.value) {
    closeModal();
  }
};

const handleOutsideClick = (e) => {
  if (isOpen.value && e.target.classList.contains('fixed')) {
    closeModal();
  }
};

onMounted(() => {
  if (process.client) {
    const token = localStorage.getItem('auth_token');
    
    if (token) {
      auth.value = {
        token: token,
        user: localStorage.getItem('auth_user') ? JSON.parse(localStorage.getItem('auth_user')) : null,
        isAuthenticated: true
      };
    }
    
    document.addEventListener('keydown', handleEsc);
    document.addEventListener('click', handleOutsideClick);
  }
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleEsc);
  document.removeEventListener('click', handleOutsideClick);
});
</script>