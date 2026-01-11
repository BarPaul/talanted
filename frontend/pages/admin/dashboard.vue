<template>
  <div class="flex h-screen w-screen">
    <AdminSidebar />
    <div class="p-6 w-full overflow-y-auto">
      <h1 class="text-2xl font-bold text-gray-800 mb-8">Дашборд</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-gradient-to-r from-primary-500 to-primary-700 text-white rounded-xl p-6">
          <p class="text-sm opacity-80">Достижений</p>
          <p class="text-3xl font-bold mt-2">{{ stats.achievements }}</p>
        </div>
        <div class="bg-gradient-to-r from-secondary-500 to-secondary-700 text-white rounded-xl p-6">
          <p class="text-sm opacity-80">Учителей</p>
          <p class="text-3xl font-bold mt-2">{{ stats.teacher }}</p>
        </div>
        <div class="bg-gradient-to-r from-purple-500 to-purple-700 text-white rounded-xl p-6">
          <p class="text-sm opacity-80">Учеников</p>
          <p class="text-3xl font-bold mt-2">{{ stats.child }}</p>
        </div>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow-sm p-6 h-[300px]">
          <h2 class="text-lg font-medium text-gray-800 mb-4">Достижения по направлениям</h2>
          <div class="w-full h-full">
            <canvas id="achievementsByTypeChart" class="w-full h-full"></canvas>
          </div>
        </div>
        
        <div class="bg-white rounded-xl shadow-sm p-6 h-[300px]">
          <h2 class="text-lg font-medium text-gray-800 mb-4">Количество объектов</h2>
          <div class="w-full h-full">
            <canvas id="objectsCountChart" class="w-full h-full"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
useHead({ 
  title: 'Админ: Дашборд'
});

const apiUrl = useRuntimeConfig().public.apiUrl;
const stats = ref({ achievements: 0, teacher: 0, child: 0 });
const chartInstances = ref({});
const chartLoading = ref(true);
const chartError = ref(null);

const buildUrl = (baseUrl, path) => {
  if (!baseUrl) {
    throw new Error('API URL не настроен. Проверьте NUXT_PUBLIC_API_URL в .env файле');
  }
  
  const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${cleanBaseUrl}${cleanPath}`;
};

const achievementsData = {
  labels: ['Неделя 1', 'Неделя 2', 'Неделя 3', 'Неделя 4'],
  datasets: [
    {
      label: 'Наука',
      data: [15, 25, 30, 35],
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      tension: 0.4,
      fill: true
    },
    {
      label: 'Искусство',
      data: [10, 15, 20, 25],
      borderColor: '#8b5cf6',
      backgroundColor: 'rgba(139, 92, 246, 0.1)',
      tension: 0.4,
      fill: true
    },
    {
      label: 'Спорт',
      data: [20, 18, 25, 30],
      borderColor: '#10b981',
      backgroundColor: 'rgba(16, 185, 129, 0.1)',
      tension: 0.4,
      fill: true
    }
  ]
};

const objectsCountData = {
  labels: ['Неделя 1', 'Неделя 2', 'Неделя 3', 'Неделя 4'],
  datasets: [
    {
      label: 'Достижения',
      data: [45, 65, 80, 90],
      borderColor: '#ef4444',
      backgroundColor: 'rgba(239, 68, 68, 0.1)',
      tension: 0.4,
      fill: true
    },
    {
      label: 'Учителя',
      data: [5, 8, 10, 12],
      borderColor: '#f59e0b',
      backgroundColor: 'rgba(245, 158, 11, 0.1)',
      tension: 0.4,
      fill: true
    },
    {
      label: 'Школы',
      data: [3, 5, 7, 8],
      borderColor: '#14b8a6',
      backgroundColor: 'rgba(20, 184, 166, 0.1)',
      tension: 0.4,
      fill: true
    }
  ]
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    tooltip: {
      mode: 'index',
      intersect: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(0, 0, 0, 0.05)'
      }
    },
    x: {
      grid: {
        color: 'rgba(0, 0, 0, 0.05)'
      }
    }
  }
};

const loadChartJs = () => {
  return new Promise((resolve, reject) => {
    if (typeof window.Chart !== 'undefined') {
      resolve();
      return;
    }
    
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
    script.onload = () => resolve();
    script.onerror = (err) => {
      console.error('Ошибка загрузки Chart.js:', err);
      reject(new Error(`Failed to load Chart.js: ${err.message || 'unknown error'}`));
    };
    document.head.appendChild(script);
  });
};

const waitForChartJs = (maxAttempts = 30, interval = 100) => {
  return new Promise((resolve, reject) => {
    let attempts = 0;
    
    const checkChart = () => {
      if (typeof window.Chart !== 'undefined') {
        resolve();
      } else if (attempts >= maxAttempts) {
        reject(new Error('Chart.js failed to load within expected time'));
      } else {
        attempts++;
        setTimeout(checkChart, interval);
      }
    };
    
    checkChart();
  });
};

const initCharts = () => {
  const achievementsCtx = document.getElementById('achievementsByTypeChart');
  if (achievementsCtx && typeof window.Chart !== 'undefined') {
    if (chartInstances.value.achievements) {
      chartInstances.value.achievements.destroy();
    }
    
    chartInstances.value.achievements = new Chart(achievementsCtx, {
      type: 'line',
      data: achievementsData,
      options: chartOptions
    });
  }
  
  const objectsCtx = document.getElementById('objectsCountChart');
  if (objectsCtx && typeof window.Chart !== 'undefined') {
    if (chartInstances.value.objects) {
      chartInstances.value.objects.destroy();
    }
    
    chartInstances.value.objects = new Chart(objectsCtx, {
      type: 'line',
      data: objectsCountData,
      options: chartOptions
    });
  }
};

onMounted(async () => {
  try {
    stats.value = await $fetch(buildUrl(apiUrl, '/stats/counts'));
    await loadChartJs();
    await waitForChartJs();
    initCharts();
  } catch (err) {
    chartError.value = `Ошибка при загрузке графиков: ${err.message}`;
    console.error('Ошибка при загрузке данных:', err);
  } finally {
    chartLoading.value = false;
  }
});

onUnmounted(() => {
  Object.values(chartInstances.value).forEach(chart => {
    if (chart && typeof chart.destroy === 'function') {
      chart.destroy();
    }
  });
});
</script>