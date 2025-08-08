<template>
  <div>
    <h1>Список предметов</h1>

    <ul>
      <li v-for="item in items" :key="item.id">
        <b>{{ item.name }}</b><br>
        Цена: {{ item.price }}<br>
        Есть? {{ item.is_stock }}
      </li>
    </ul>

    <button @click="showForm = true">Добавить предмет</button>

    <div v-if="showForm" style="margin-top: 1em;">
      <input v-model="newItemName" placeholder="Название предмета" />
      <input type="number" step="0.01" min="0.01" v-model="newItemPrice" placeholder="Цена предмета" />
      <button @click="addItem" :disabled="!newItemName.trim()">Добавить</button>
      <button @click="cancel">Отмена</button>
    </div>

    <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const config = useRuntimeConfig()

const items = ref([])
const error = ref('')
const showForm = ref(false)
const newItemName = ref('')
const newItemPrice = ref('')

async function loadItems() {
  error.value = ''
  try {
    const res = await $fetch(`${config.public.apiUrl}/items`)
    items.value = res
  } catch (e) {
    error.value = 'Ошибка запроса списка '
    console.error(e)
  }
}

async function addItem() {
  if (!newItemName.value.trim()) return

  error.value = ''
  try {
    await $fetch(`${config.public.apiUrl}/items`, {
      method: 'POST',
        body: {
            name: newItemName.value.trim(),
            price: newItemPrice.value,
            is_stock: true
        },
    })
    newItemName.value = ''
    showForm.value = false
    await loadItems()
  } catch (e) {
    error.value = 'Ошибка при добавлении предмета'
    console.error(e)
  }
}

function cancel() {
  newItemName.value = ''
  showForm.value = false
}

onMounted(loadItems)
</script>