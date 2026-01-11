<template>
  <Header />
  <div class="container mx-auto px-4 py-8">
    <h2 class="text-xl font-semibold text-gray-800 mb-6">Часто задаваемые вопросы</h2>
    
    <FaqAccordion question="Как добавлять достижения?">
      Достижения могут добавлять только администрация школы или муниципалитета. 
    </FaqAccordion>
    
    <FaqAccordion question="Как рассчитывается коэффициент?">
      Коэффициент рассчитывается по формуле: базовый × тип × уровень × формат × команда × место × давность.
      <p class="mt-2 text-gray-600">Пример: Научное достижение (1.4) Всероссийского уровня (3.25) в очном формате (1.5), одиночное (1.75), занявшее 1 место (1.25), будет иметь коэффициент: 1.4 × 3.25 × 1.5 × 1.75 × 1.25 = 14.95</p>
    </FaqAccordion>

    <FaqAccordion question="Как подключиться к системе?">
      Администрация школы или муниципалитета отправляет заявку на регистрацию на сайт.
    </FaqAccordion>
  
    <FaqAccordion question="Как узнать свой код?">
      Обратитесь к администрации своей школы или же к классному руководителю
    </FaqAccordion>

    <!-- Блок с несколькими таблицами в одной строке -->
    <h3 class="text-lg font-medium mt-10 mb-4">Коэффициенты по различным категориям</h3>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Таблица типов достижений -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-4 py-3 bg-gray-50 border-b border-gray-200">
          <h4 class="text-sm font-medium text-gray-900">Типы достижений</h4>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Тип</th>
                <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Коэф.</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(item, index) in typeFactors" :key="index" class="hover:bg-gray-50">
                <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.type }}</td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-center text-gray-500">{{ item.value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-4 py-3 bg-gray-50 border-b border-gray-200">
          <h4 class="text-sm font-medium text-gray-900">Уровни достижений</h4>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Уровень</th>
                <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Коэф.</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(item, index) in levelFactors" :key="index" class="hover:bg-gray-50">
                <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.level }}</td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-center text-gray-500">{{ item.value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-4 py-3 bg-gray-50 border-b border-gray-200">
          <h4 class="text-sm font-medium text-gray-900">Форматы достижений</h4>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Формат</th>
                <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Коэф.</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(item, index) in formatFactors" :key="index" class="hover:bg-gray-50">
                <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.format }}</td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-center text-gray-500">{{ item.value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-4 py-3 bg-gray-50 border-b border-gray-200">
          <h4 class="text-sm font-medium text-gray-900">Командная работа</h4>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Тип</th>
                <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Коэф.</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(item, index) in teamFactors" :key="index" class="hover:bg-gray-50">
                <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.team }}</td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-center text-gray-500">{{ item.value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-4 py-3 bg-gray-50 border-b border-gray-200">
          <h4 class="text-sm font-medium text-gray-900">Места</h4>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Место</th>
                <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Коэф.</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(item, index) in placeFactors" :key="index" class="hover:bg-gray-50">
                <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.place }}</td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-center text-gray-500">{{ item.value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-4 py-3 bg-gray-50 border-b border-gray-200">
          <h4 class="text-sm font-medium text-gray-900">Давность</h4>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Давность</th>
                <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Коэф.</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(item, index) in timeFactors" :key="index" class="hover:bg-gray-50">
                <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.time }}</td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-center text-gray-500">{{ item.value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
useHead({ title: 'ЧаВО' });

const typeFactors = [
  { type: 'Наука', value: 1.4 },
  { type: 'Искусство', value: 1.4 },
  { type: 'Спорт', value: 1.4 }
];

const levelFactors = [
  { level: 'Городской', value: 1.25 },
  { level: 'Межгородской', value: 1.5 },
  { level: 'Региональный', value: 2.25 },
  { level: 'Межрегиональный', value: 3.75 },
  { level: 'Всероссийский', value: 4.5 }
];

const formatFactors = [
  { format: 'Очное', value: 1.5 },
  { format: 'Дистанционное', value: 0.5 }
];

const teamFactors = [
  { team: 'Одиночное', value: 1.75 },
  { team: 'Командное', value: 1.25 }
];

const placeFactors = [
  { place: 'Гран-при', value: 1.3 },
  { place: '1-е место', value: 1.25 },
  { place: '2-е место', value: 0.75 },
  { place: '3-е место', value: 0.5 },
  { place: 'Участник', value: 0.25 }
];

const timeFactors = [
  { time: 'Более 3-х лет', value: 0 },
  { time: 'Более 2-х лет', value: 0.25 },
  { time: 'Более 1 года', value: 0.75 },
  { time: 'Более месяца', value: 1.25 },
  { time: 'Меньше месяца', value: 1.5 }
];

</script>