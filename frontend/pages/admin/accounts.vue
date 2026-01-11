<template>
  <div class="flex h-screen w-screen">
    <AdminSidebar />
    <div class="p-6 w-full">
    
      <div v-if="loading" class="flex justify-center py-8">
        <div class="loader border-t-2 border-blue-500 rounded-full w-8 h-8 animate-spin"></div>
      </div>
      
      <div v-else-if="error" class="text-red-500 text-center py-4">
        {{ error }}
      </div>
      
      <div v-else-if="!user" class="text-center py-8 bg-gray-50 rounded-xl">
        <p class="text-gray-600">Не удалось загрузить информацию о пользователе</p>
      </div>
      
      <div v-else>
        <h1 class="text-2xl font-semibold text-gray-800 mb-6" v-if="user.role === 'school'">Управление классами</h1>
        <h1 class="text-2xl font-semibold text-gray-800 mb-6" v-else-if="user.role === 'mun'">Управление школами</h1>
        <h1 class="text-2xl font-semibold text-gray-800 mb-6" v-else>Управление муниципалитетами</h1>

        <div v-if="user.role === 'school'" class="mb-8">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-gray-800">Мои классы</h2>
            <button @click="openAddGradeModal" class="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
              Добавить класс
            </button>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="grade in grades" :key="grade.id" class="border border-gray-200 rounded-xl p-5">
              <div class="flex justify-between">
                <div>
                  <h3 class="font-semibold">{{ grade.grade }}{{ grade.parallel }}</h3>
                  <p class="text-sm mt-2">Коэффициент: <span class="font-bold text-primary-700">{{ grade.ratio }}</span></p>
                </div>
                <div class="flex space-x-1">
                  <button @click="openEditGradeModal(grade)" class="text-blue-600 hover:text-blue-800">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button @click="confirmDeleteGrade(grade.id)" class="text-red-600 hover:text-red-800">
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
              </div>
              <div class="mt-4">
                <button @click="showGradeStudents(grade.id)" class="w-full bg-primary-600 text-white py-1 px-3 rounded-md text-sm">
                  Просмотреть учеников
                </button>
              </div>
            </div>
          </div>
          
          <div v-if="grades.length === 0" class="text-center py-8 bg-gray-50 rounded-xl mt-6">
            <p class="text-gray-600">У вашей школы пока нет классов</p>
          </div>
          
          <div v-if="selectedGrade" class="mt-10">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-xl font-semibold">Ученики в {{ selectedGrade.grade }}{{ selectedGrade.parallel }}</h3>
              <div class="flex space-x-2">
                <button @click="openAddChildModal" class="bg-primary-600 text-white px-3 py-1 rounded-md text-sm">
                  Добавить ученика
                </button>
                <button @click="selectedGrade = null" class="text-gray-600 hover:text-gray-800 flex items-center">
                  <i class="fas fa-arrow-left mr-1"></i>
                  Вернуться к классам
                </button>
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="student in gradeStudents" :key="student.id" class="border border-gray-200 rounded-xl p-5">
                <div class="flex justify-between">
                  <div>
                    <h3 class="font-semibold">{{ student.name }}</h3>
                    <p class="text-sm text-gray-600">ID: {{ student.id }}</p>
                  </div>
                  <div class="flex space-x-1">
                    <button @click="openEditChildModal(student)" class="text-blue-600 hover:text-blue-800">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="confirmDeleteChild(student.id)" class="text-red-600 hover:text-red-800">
                      <i class="fas fa-trash"></i>
                    </button>
                    <button @click="showStudentAchievements(student.id)" class="text-green-600 hover:text-green-800">
                      <i class="fas fa-trophy"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="gradeStudents.length === 0" class="text-center py-8 bg-gray-50 rounded-xl mt-6">
              <p class="text-gray-600">В этом классе пока нет учеников</p>
            </div>
          </div>
        </div>
        
        <div v-else-if="user.role === 'mun'" class="mb-8">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Школы в {{ user.city }}</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="school in schools" :key="school.id" class="border border-gray-200 rounded-xl p-5">
              <div class="flex justify-between">
                <div>
                  <h3 class="font-semibold">{{ school.name }}</h3>
                  <p class="text-sm text-gray-600">{{ school.city }}</p>
                  <p class="text-sm mt-2">Коэффициент: <span class="font-bold text-primary-700">{{ school.total_ratio }}</span></p>
                </div>
                <span v-if="!school.is_active" class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs">Неподтверждён</span>
              </div>
              <div class="flex space-x-3 mt-4">
                <button v-if="!school.is_active" @click="confirmSchool(school.id)" class="flex-1 bg-green-600 text-white py-1 px-3 rounded-md text-sm">Подтвердить</button>
                <button @click="showSchoolDetails(school.id)" class="flex-1 bg-primary-600 text-white py-1 px-3 rounded-md text-sm">Просмотреть</button>
              </div>
            </div>
          </div>
          
          <div v-if="schools.length === 0" class="text-center py-8 bg-gray-50 rounded-xl mt-6">
            <p class="text-gray-600">В вашем муниципалитете пока нет школ</p>
          </div>
          
          <div v-if="selectedSchool" class="mt-10">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-xl font-semibold">{{ selectedSchool.name }}</h3>
              <button @click="backToSchools" class="text-gray-600 hover:text-gray-800 flex items-center">
                <i class="fas fa-arrow-left mr-1"></i>
                Вернуться к списку школ
              </button>
            </div>
            
            <div class="flex flex-wrap gap-2 mb-6">
              <button @click="openAddTeacherModal" class="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
                Добавить учителя
              </button>
              <button @click="openAddGradeModal" class="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
                Добавить класс
              </button>
              <button @click="openAddAchievementModal" class="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
                Добавить достижение
              </button>
            </div>
            <div class="border-b border-gray-200 mb-6">
              <nav class="-mb-px flex space-x-8">
                <button
                  @click="activeTab = 'classes'"
                  :class="['py-2 px-1 border-b-2 font-medium text-sm', activeTab === 'classes' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700']"
                >
                  Классы
                </button>
                <button
                  @click="activeTab = 'teachers'"
                  :class="['py-2 px-1 border-b-2 font-medium text-sm', activeTab === 'teachers' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700']"
                >
                  Учителя
                </button>
              </nav>
            </div>
            <div v-if="activeTab === 'classes'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="grade in schoolClasses" :key="grade.id" class="border border-gray-200 rounded-xl p-5">
                <div class="flex justify-between">
                  <div>
                    <h3 class="font-semibold">{{ grade.grade }}{{ grade.parallel }}</h3>
                    <p class="text-sm mt-2">Коэффициент: <span class="font-bold text-primary-700">{{ grade.ratio }}</span></p>
                  </div>
                  <div class="flex space-x-1">
                    <button @click="openEditGradeModal(grade)" class="text-blue-600 hover:text-blue-800">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="confirmDeleteGrade(grade.id)" class="text-red-600 hover:text-red-800">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
                <div class="mt-4">
                  <button @click="showClassStudents(grade.id)" class="w-full bg-primary-600 text-white py-1 px-3 rounded-md text-sm">
                    Просмотреть учеников
                  </button>
                </div>
              </div>
            </div>
            
            <div v-else-if="activeTab === 'teachers'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="teacher in schoolTeachers" :key="teacher.id" class="border border-gray-200 rounded-xl p-5">
                <div class="flex justify-between">
                  <div>
                    <h3 class="font-semibold">{{ teacher.name }}</h3>
                    <p class="text-sm text-gray-600">ID: {{ teacher.id }}</p>
                  </div>
                  <div class="flex space-x-1">
                    <button @click="openEditTeacherModal(teacher)" class="text-blue-600 hover:text-blue-800">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="confirmDeleteTeacher(teacher.id)" class="text-red-600 hover:text-red-800">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="selectedClass" class="mt-10">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-semibold">Ученики в {{ selectedClass.grade }}{{ selectedClass.parallel }}</h3>
                <div class="flex space-x-2">
                  <button @click="openAddChildModal" class="bg-primary-600 text-white px-3 py-1 rounded-md text-sm">
                    Добавить ученика
                  </button>
                  <button @click="selectedClass = null" class="text-gray-600 hover:text-gray-800 flex items-center">
                    <i class="fas fa-arrow-left mr-1"></i>
                    Вернуться к классам
                  </button>
                </div>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="student in classStudents" :key="student.id" class="border border-gray-200 rounded-xl p-5">
                  <div class="flex justify-between">
                    <div>
                      <h3 class="font-semibold">{{ student.name }}</h3>
                      <p class="text-sm text-gray-600">ID: {{ student.id }}</p>
                    </div>
                    <div class="flex space-x-1">
                      <button @click="openEditChildModal(student)" class="text-blue-600 hover:text-blue-800">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button @click="confirmDeleteChild(student.id)" class="text-red-600 hover:text-red-800">
                        <i class="fas fa-trash"></i>
                      </button>
                      <button @click="showStudentAchievements(student.id)" class="text-green-600 hover:text-green-800">
                        <i class="fas fa-trophy"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="classStudents.length === 0" class="text-center py-8 bg-gray-50 rounded-xl mt-6">
                <p class="text-gray-600">В этом классе пока нет учеников</p>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else-if="user.role === 'owner'" class="mb-8">
          <div v-if="!selectedMunicipality">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Муниципалитеты</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="municipality in municipalities" :key="municipality.city" class="border border-gray-200 rounded-xl p-5">
                <div class="flex justify-between">
                  <div>
                    <h3 class="font-semibold">{{ municipality.city }}</h3>
                    <p class="text-sm mt-2">Коэффициент: <span class="font-bold text-primary-700">{{ municipality.total_ratio }}</span></p>
                    <p class="text-sm mt-1">Школ: <span class="font-medium">{{ municipality.schools.length }}</span></p>
                  </div>
                </div>
                <div class="mt-4">
                  <button @click="showMunicipalitySchools(municipality.city)" class="w-full bg-primary-600 text-white py-1 px-3 rounded-md text-sm">
                    Посмотреть школы
                  </button>
                </div>
              </div>
            </div>
            
            <div v-if="municipalities.length === 0" class="text-center py-8 bg-gray-50 rounded-xl mt-6">
              <p class="text-gray-600">Нет доступных муниципалитетов</p>
            </div>
          </div>
          <div v-else>
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-xl font-semibold">Школы в {{ selectedMunicipality }}</h3>
              <button @click="backToMunicipalities" class="text-gray-600 hover:text-gray-800 flex items-center">
                <i class="fas fa-arrow-left mr-1"></i>
                Вернуться к списку муниципалитетов
              </button>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="school in municipalitySchools" :key="school.id" class="border border-gray-200 rounded-xl p-5">
                <div class="flex justify-between">
                  <div>
                    <h3 class="font-semibold">{{ school.name }}</h3>
                    <p class="text-sm text-gray-600">{{ school.city }}</p>
                    <p class="text-sm mt-2">Коэффициент: <span class="font-bold text-primary-700">{{ school.total_ratio }}</span></p>
                  </div>
                  <span v-if="!school.is_active" class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs">Неподтверждён</span>
                </div>
                <div class="flex space-x-3 mt-4">
                  <button v-if="!school.is_active" @click="confirmSchool(school.id)" class="flex-1 bg-green-600 text-white py-1 px-3 rounded-md text-sm">Подтвердить</button>
                  <button @click="showSchoolDetails(school.id)" class="flex-1 bg-primary-600 text-white py-1 px-3 rounded-md text-sm">Просмотреть</button>
                </div>
              </div>
            </div>
            
            <div v-if="municipalities.length === 0" class="text-center py-8 bg-gray-50 rounded-xl mt-6">
              <p class="text-gray-600">В этом муниципалитете пока нет школ</p>
            </div>
          </div>
          <div v-if="selectedSchool" class="mt-10">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-xl font-semibold">{{ selectedSchool.name }}</h3>
              <button @click="selectedSchool = null" class="text-gray-600 hover:text-gray-800 flex items-center">
                <i class="fas fa-arrow-left mr-1"></i>
                Вернуться к списку школ
              </button>
            </div>
            <div class="flex flex-wrap gap-2 mb-6">
              <button @click="openAddTeacherModal" class="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
                Добавить учителя
              </button>
              <button @click="openAddGradeModal" class="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
                Добавить класс
              </button>
              <button @click="openAddAchievementModal" class="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
                Добавить достижение
              </button>
            </div>
            <div class="border-b border-gray-200 mb-6">
              <nav class="-mb-px flex space-x-8">
                <button
                  @click="activeTab = 'classes'"
                  :class="['py-2 px-1 border-b-2 font-medium text-sm', activeTab === 'classes' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700']"
                >
                  Классы
                </button>
                <button
                  @click="activeTab = 'teachers'"
                  :class="['py-2 px-1 border-b-2 font-medium text-sm', activeTab === 'teachers' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700']"
                >
                  Учителя
                </button>
              </nav>
            </div>
            <div v-if="activeTab === 'classes'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="grade in schoolClasses" :key="grade.id" class="border border-gray-200 rounded-xl p-5">
                <div class="flex justify-between">
                  <div>
                    <h3 class="font-semibold">{{ grade.grade }}{{ grade.parallel }}</h3>
                    <p class="text-sm mt-2">Коэффициент: <span class="font-bold text-primary-700">{{ grade.ratio }}</span></p>
                  </div>
                  <div class="flex space-x-1">
                    <button @click="openEditGradeModal(grade)" class="text-blue-600 hover:text-blue-800">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="confirmDeleteGrade(grade.id)" class="text-red-600 hover:text-red-800">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
                <div class="mt-4">
                  <button @click="showClassStudents(grade.id)" class="w-full bg-primary-600 text-white py-1 px-3 rounded-md text-sm">
                    Просмотреть учеников
                  </button>
                </div>
              </div>
            </div>
            
            <div v-else-if="activeTab === 'teachers'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="teacher in schoolTeachers" :key="teacher.id" class="border border-gray-200 rounded-xl p-5">
                <div class="flex justify-between">
                  <div>
                    <h3 class="font-semibold">{{ teacher.name }}</h3>
                    <p class="text-sm text-gray-600">ID: {{ teacher.id }}</p>
                  </div>
                  <div class="flex space-x-1">
                    <button @click="openEditTeacherModal(teacher)" class="text-blue-600 hover:text-blue-800">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="confirmDeleteTeacher(teacher.id)" class="text-red-600 hover:text-red-800">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="selectedClass" class="mt-10">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-semibold">Ученики в {{ selectedClass.grade }}{{ selectedClass.parallel }}</h3>
                <div class="flex space-x-2">
                  <button @click="openAddChildModal" class="bg-primary-600 text-white px-3 py-1 rounded-md text-sm">
                    Добавить ученика
                  </button>
                  <button @click="selectedClass = null" class="text-gray-600 hover:text-gray-800 flex items-center">
                    <i class="fas fa-arrow-left mr-1"></i>
                    Вернуться к классам
                  </button>
                </div>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="student in classStudents" :key="student.id" class="border border-gray-200 rounded-xl p-5">
                  <div class="flex justify-between">
                    <div>
                      <h3 class="font-semibold">{{ student.name }}</h3>
                      <p class="text-sm text-gray-600">ID: {{ student.id }}</p>
                    </div>
                    <div class="flex space-x-1">
                      <button @click="openEditChildModal(student)" class="text-blue-600 hover:text-blue-800">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button @click="confirmDeleteChild(student.id)" class="text-red-600 hover:text-red-800">
                        <i class="fas fa-trash"></i>
                      </button>
                      <button @click="showStudentAchievements(student.id)" class="text-green-600 hover:text-green-800">
                        <i class="fas fa-trophy"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="classStudents.length === 0" class="text-center py-8 bg-gray-50 rounded-xl mt-6">
                <p class="text-gray-600">В этом классе пока нет учеников</p>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="text-center py-8 bg-gray-50 rounded-xl">
          <p class="text-gray-600">У вас нет прав для управления аккаунтами</p>
        </div>
      </div>
    </div>
    <Modal v-if="showDeleteModal" @close="showDeleteModal = false">
      <div class="p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Вы уверены?</h3>
        <p class="text-gray-600 mb-6">Вы действительно хотите удалить этот элемент? Это действие нельзя отменить.</p>
        <div class="flex justify-end space-x-3">
          <button @click="showDeleteModal = false" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
            Отмена
          </button>
          <button @click="deleteItem" class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700">
            Удалить
          </button>
        </div>
      </div>
    </Modal>
    <Modal v-if="showGradeModal" @close="closeGradeModal">
      <div class="p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">{{ gradeModalTitle }}</h3>
        <form @submit.prevent="saveGrade">
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Класс</label>
              <input v-model="gradeForm.grade" type="number" min="1" max="11" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500" required>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Параллель</label>
              <input v-model="gradeForm.parallel" type="text" maxlength="1" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500" required>
            </div>
          </div>
          <div class="flex justify-end space-x-3">
            <button type="button" @click="closeGradeModal" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
              Отмена
            </button>
            <button type="submit" class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700">
              {{ gradeModalAction }}
            </button>
          </div>
        </form>
      </div>
    </Modal>
    <Modal v-if="showChildModal" @close="closeChildModal">
      <div class="p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">{{ childModalTitle }}</h3>
        <form @submit.prevent="saveChild">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Имя</label>
            <input v-model="childForm.name" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500" required>
          </div>
          <div class="flex justify-end space-x-3">
            <button type="button" @click="closeChildModal" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
              Отмена
            </button>
            <button type="submit" class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700">
              {{ childModalAction }}
            </button>
          </div>
        </form>
      </div>
    </Modal>
    <Modal v-if="showTeacherModal" @close="closeTeacherModal">
      <div class="p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">{{ teacherModalTitle }}</h3>
        <form @submit.prevent="saveTeacher">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Имя</label>
            <input v-model="teacherForm.name" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500" required>
          </div>
          <div class="flex justify-end space-x-3">
            <button type="button" @click="closeTeacherModal" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
              Отмена
            </button>
            <button type="submit" class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700">
              {{ teacherModalAction }}
            </button>
          </div>
        </form>
      </div>
    </Modal>
    <Modal v-if="showAchievementModal" @close="closeAchievementModal">
      <div class="p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Добавить достижение</h3>
        <form @submit.prevent="saveAchievement">
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Название</label>
              <input v-model="achievementForm.name" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500" required>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Ученик</label>
              <select v-model="achievementForm.child_id" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500" required>
                <option v-for="student in allStudents" :key="student.id" :value="student.id">{{ student.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Учитель</label>
              <select v-model="achievementForm.teacher_id" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500" required>
                <option v-for="teacher in schoolTeachers" :key="teacher.id" :value="teacher.id">{{ teacher.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Дата</label>
              <input v-model="achievementForm.date" type="date" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500" required>
            </div>
          </div>
          <div class="flex justify-end space-x-3">
            <button type="button" @click="closeAchievementModal" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
              Отмена
            </button>
            <button type="submit" class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700">
              Добавить
            </button>
          </div>
        </form>
      </div>
    </Modal>
    <Modal v-if="showAchievementsModal" @close="closeAchievementsModal">
      <div class="p-6 max-h-96 overflow-y-auto">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Достижения ученика</h3>
        <div v-if="studentAchievements.length > 0" class="space-y-4">
          <div v-for="achievement in studentAchievements" :key="achievement.id" class="border border-gray-200 rounded-lg p-4">
            <div class="flex justify-between">
              <div>
                <h4 class="font-semibold">{{ achievement.name }}</h4>
                <p class="text-sm text-gray-600">Тип: {{ achievement.type }}</p>
                <p class="text-sm text-gray-600">Уровень: {{ achievement.level }}</p>
                <p class="text-sm text-gray-600">Дата: {{ achievement.date }}</p>
              </div>
              <div class="flex space-x-1">
                <button @click="openEditAchievementModal(achievement)" class="text-blue-600 hover:text-blue-800">
                  <i class="fas fa-edit"></i>
                </button>
                <button @click="confirmDeleteAchievement(achievement.id)" class="text-red-600 hover:text-red-800">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-8">
          <p class="text-gray-600">У этого ученика пока нет достижений</p>
        </div>
        <div class="flex justify-end mt-4">
          <button @click="closeAchievementsModal" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
            Закрыть
          </button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useHead, useRuntimeConfig } from '#app';
import Modal from '~/components/Modal.vue';

useHead({ title: 'Админ: Управление аккаунтами' });

const apiUrl = useRuntimeConfig().public.apiUrl;
const user = ref(null);
const schools = ref([]);
const grades = ref([]);
const municipalities = ref([]);
const loading = ref(true);
const error = ref(null);
const selectedMunicipality = ref(null);
const municipalitySchools = ref([]);
const selectedSchool = ref(null);
const selectedGrade = ref(null);
const selectedClass = ref(null);
const activeTab = ref('classes');
const schoolClasses = ref([]);
const schoolTeachers = ref([]);
const gradeStudents = ref([]);
const classStudents = ref([]);
const allStudents = ref([]);

const showDeleteModal = ref(false);
const showGradeModal = ref(false);
const showChildModal = ref(false);
const showTeacherModal = ref(false);
const showAchievementModal = ref(false);
const showAchievementsModal = ref(false);

const deleteType = ref('');
const deleteId = ref(null);

const gradeForm = ref({
  id: null,
  grade: 1,
  parallel: 'А'
});

const childForm = ref({
  id: null,
  name: ''
});

const teacherForm = ref({
  id: null,
  name: ''
});

const achievementForm = ref({
  name: '',
  child_id: null,
  teacher_id: null,
  date: '',
  type: 'Наука',
  level: 'Городской',
  format: 'Очное',
  team: 'Одиночное',
  place: '1-е место'
});

const studentAchievements = ref([]);

const gradeModalTitle = computed(() => {
  return gradeForm.value.id ? 'Редактировать класс' : 'Добавить класс';
});

const gradeModalAction = computed(() => {
  return gradeForm.value.id ? 'Сохранить' : 'Добавить';
});

const childModalTitle = computed(() => {
  return childForm.value.id ? 'Редактировать ученика' : 'Добавить ученика';
});

const childModalAction = computed(() => {
  return childForm.value.id ? 'Сохранить' : 'Добавить';
});

const teacherModalTitle = computed(() => {
  return teacherForm.value.id ? 'Редактировать учителя' : 'Добавить учителя';
});

const teacherModalAction = computed(() => {
  return teacherForm.value.id ? 'Сохранить' : 'Добавить';
});

const buildUrl = (baseUrl, path) => {
  if (!baseUrl) {
    throw new Error('API URL не настроен. Проверьте NUXT_PUBLIC_API_URL в .env файле');
  }
  
  const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${cleanBaseUrl}${cleanPath}`;
};

const loadUserData = async () => {
  try {
        const userData = await $fetch(buildUrl(apiUrl, '/auth/me'), {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      }
    });
    
    console.log('Данные пользователя:', userData);
    user.value = userData;
    
        if (user.value.role === 'school') {
      await loadSchoolGrades();
    } else if (user.value.role === 'mun') {
      await loadMunicipalitySchools();
    } else if (user.value.role === 'owner') {
      await loadAllMunicipalities();
    } else {
      error.value = 'У вас нет прав для управления аккаунтами';
    }
  } catch (err) {
    error.value = 'Ошибка при загрузке данных пользователя';
    console.error('Ошибка при загрузке данных пользователя:', err);
  } finally {
    loading.value = false;
  }
};

const loadSchoolGrades = async () => {
  try {
    console.log('Загрузка классов для школы');
    const data = await $fetch(buildUrl(apiUrl, '/grade/all'), {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      }
    });
    
    console.log('Данные классов:', data);
    grades.value = data.grades || [];
  } catch (err) {
    error.value = 'Ошибка при загрузке классов';
    console.error('Ошибка при загрузке классов:', err);
  }
};

const loadMunicipalitySchools = async () => {
  try {
    console.log('Загрузка школ для муниципалитета');
    const data = await $fetch(buildUrl(apiUrl, '/stats/ratings/municipalities'), {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      }
    });
    
    console.log('Данные рейтингов муниципалитетов:', data);
    
        const municipality = data.municipalities.find(m => m.city === user.value.city);
    if (municipality) {
      schools.value = municipality.schools.map(school => ({
        ...school,
        is_active: true
      }));
      console.log('Школы в муниципалитете:', schools.value);
    } else {
      console.log(`Муниципалитет для города ${user.value.city} не найден`);
      schools.value = [];
    }
  } catch (err) {
    error.value = 'Ошибка при загрузке школ';
    console.error('Ошибка при загрузке школ:', err);
  }
};

const loadAllMunicipalities = async () => {
  try {
    console.log('Загрузка всех муниципалитетов');
    const data = await $fetch(buildUrl(apiUrl, '/stats/ratings/municipalities'), {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      }
    });
    
    console.log('Данные всех муниципалитетов:', data);
    municipalities.value = data.municipalities || [];
  } catch (err) {
    error.value = 'Ошибка при загрузке муниципалитетов';
    console.error('Ошибка при загрузке муниципалитетов:', err);
  }
};

const showMunicipalitySchools = async (city) => {
  try {
    console.log(`Загрузка школ для муниципалитета: ${city}`);
    selectedMunicipality.value = city;
    
    const response = await $fetch(buildUrl(apiUrl, `/stats/ratings/municipalities`), {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      },
      params: { city }
    });
    
    console.log('Ответ от сервера:', response);
    
    if (response && Array.isArray(response.municipalities) && response.municipalities.length > 0) {
      const municipality = response.municipalities.find(m => m.city === city);
      if (municipality && Array.isArray(municipality.schools)) {
        municipalitySchools.value = municipality.schools.map(school => ({
          ...school,
          is_active: true
        }));
      } else {
        municipalitySchools.value = [];
      }
    } else {
      municipalitySchools.value = [];
      console.error('Неожиданная структура ответа:', response);
    }
  } catch (err) {
    error.value = `Ошибка при загрузке школ в муниципалитете ${city}`;
    console.error('Ошибка при загрузке школ в муниципалитете:', err);
  }
};

const backToMunicipalities = () => {
  selectedMunicipality.value = null;
  municipalitySchools.value = [];
};

const showSchoolDetails = async (schoolId) => {
  try {
    console.log(`Загрузка деталей школы: ${schoolId}`);
    selectedSchool.value = schools.value.find(s => s.id === schoolId);
    
        await loadSchoolClasses(schoolId);
    
        await loadSchoolTeachers(schoolId);
    
        activeTab.value = 'classes';
  } catch (err) {
    error.value = `Ошибка при загрузке деталей школы ${schoolId}`;
    console.error('Ошибка при загрузке деталей школы:', err);
  }
};

const backToSchools = () => {
  selectedSchool.value = null;
  schoolClasses.value = [];
  schoolTeachers.value = [];
  selectedClass.value = null;
};

const loadSchoolClasses = async (schoolId) => {
  try {
    console.log(`Загрузка классов для школы: ${schoolId}`);
    const data = await $fetch(buildUrl(apiUrl, `/grade/all`), {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      },
      params: { school_id: schoolId }
    });
    
    console.log('Классы школы:', data);
    schoolClasses.value = data.grades || [];
  } catch (err) {
    error.value = `Ошибка при загрузке классов школы ${schoolId}`;
    console.error('Ошибка при загрузке классов школы:', err);
  }
};

const loadSchoolTeachers = async (schoolId) => {
  try {
    console.log(`Загрузка учителей для школы: ${schoolId}`);
    const data = await $fetch(buildUrl(apiUrl, `/teacher/all`), {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      },
      params: { id: schoolId }
    });
    
    console.log('Учителя школы:', data);
    schoolTeachers.value = data.teachers || [];
  } catch (err) {
    error.value = `Ошибка при загрузке учителей школы ${schoolId}`;
    console.error('Ошибка при загрузке учителей школы:', err);
  }
};

const showClassStudents = async (gradeId) => {
  try {
    console.log(`Загрузка учеников для класса: ${gradeId}`);
    selectedClass.value = schoolClasses.value.find(g => g.id === gradeId);
    
    const data = await $fetch(buildUrl(apiUrl, `/child/all/${gradeId}`), {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      }
    });
    
    console.log('Ученики класса:', data);
    classStudents.value = data.childs || [];
    allStudents.value = classStudents.value;
  } catch (err) {
    error.value = `Ошибка при загрузке учеников класса ${gradeId}`;
    console.error('Ошибка при загрузке учеников класса:', err);
  }
};

const showGradeStudents = async (gradeId) => {
  try {
    console.log(`Загрузка учеников для класса: ${gradeId}`);
    selectedGrade.value = grades.value.find(g => g.id === gradeId);
    
    const data = await $fetch(buildUrl(apiUrl, `/child/all/${gradeId}`), {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      }
    });
    
    console.log('Ученики класса:', data);
    gradeStudents.value = data.childs || [];
    allStudents.value = gradeStudents.value;
  } catch (err) {
    error.value = `Ошибка при загрузке учеников класса ${gradeId}`;
    console.error('Ошибка при загрузке учеников класса:', err);
  }
};

const confirmDeleteGrade = (id) => {
  deleteType.value = 'grade';
  deleteId.value = id;
  showDeleteModal.value = true;
};

const confirmDeleteChild = (id) => {
  deleteType.value = 'child';
  deleteId.value = id;
  showDeleteModal.value = true;
};

const confirmDeleteTeacher = (id) => {
  deleteType.value = 'teacher';
  deleteId.value = id;
  showDeleteModal.value = true;
};

const confirmDeleteAchievement = (id) => {
  deleteType.value = 'achievement';
  deleteId.value = id;
  showDeleteModal.value = true;
};

const deleteItem = async () => {
  try {
    if (deleteType.value === 'grade') {
      await $fetch(buildUrl(apiUrl, '/grade/delete'), {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: deleteId.value })
      });
      
            if (user.value.role === 'school') {
        grades.value = grades.value.filter(g => g.id !== deleteId.value);
      } else {
        schoolClasses.value = schoolClasses.value.filter(g => g.id !== deleteId.value);
      }
    } else if (deleteType.value === 'child') {
      await $fetch(buildUrl(apiUrl, '/child/delete'), {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: deleteId.value })
      });
      
            if (selectedGrade.value) {
        gradeStudents.value = gradeStudents.value.filter(c => c.id !== deleteId.value);
      } else {
        classStudents.value = classStudents.value.filter(c => c.id !== deleteId.value);
      }
    } else if (deleteType.value === 'teacher') {
      await $fetch(buildUrl(apiUrl, '/teacher/delete'), {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: deleteId.value })
      });
      
            schoolTeachers.value = schoolTeachers.value.filter(t => t.id !== deleteId.value);
    } else if (deleteType.value === 'achievement') {
      await $fetch(buildUrl(apiUrl, '/achievement/delete'), {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: deleteId.value })
      });
      
            studentAchievements.value = studentAchievements.value.filter(a => a.id !== deleteId.value);
    }
    
    showDeleteModal.value = false;
  } catch (err) {
    error.value = `Ошибка при удалении ${deleteType.value}`;
    console.error(`Ошибка при удалении ${deleteType.value}:`, err);
    showDeleteModal.value = false;
  }
};

const openAddGradeModal = () => {
  gradeForm.value = { id: null, grade: 1, parallel: 'А' };
  showGradeModal.value = true;
};

const openEditGradeModal = (grade) => {
  gradeForm.value = { ...grade };
  showGradeModal.value = true;
};

const closeGradeModal = () => {
  showGradeModal.value = false;
};

const saveGrade = async () => {
  try {
    const endpoint = gradeForm.value.id ? '/grade/change' : '/grade/create';
    const method = gradeForm.value.id ? 'PATCH' : 'POST';
    
    const payload = gradeForm.value.id ? {
      id: gradeForm.value.id,
      new_grade: gradeForm.value.grade,
      new_parallel: gradeForm.value.parallel
    } : {
      grade: gradeForm.value.grade,
      parallel: gradeForm.value.parallel,
      school_id: selectedSchool.value ? selectedSchool.value.id : user.value.id
    };
    
    const response = await $fetch(buildUrl(apiUrl, endpoint), {
      method,
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
    
    if (gradeForm.value.id) {
            if (user.value.role === 'school') {
        grades.value = grades.value.map(g => g.id === response.id ? response : g);
      } else {
        schoolClasses.value = schoolClasses.value.map(g => g.id === response.id ? response : g);
      }
    } else {
            if (user.value.role === 'school') {
        grades.value.push(response);
      } else {
        schoolClasses.value.push(response);
      }
    }
    
    closeGradeModal();
  } catch (err) {
    error.value = `Ошибка при ${gradeForm.value.id ? 'редактировании' : 'добавлении'} класса`;
    console.error(`Ошибка при ${gradeForm.value.id ? 'редактировании' : 'добавлении'} класса:`, err);
  }
};

const openAddChildModal = () => {
  childForm.value = { id: null, name: '' };
  showChildModal.value = true;
};

const openEditChildModal = (child) => {
  childForm.value = { ...child };
  showChildModal.value = true;
};

const closeChildModal = () => {
  showChildModal.value = false;
};

const saveChild = async () => {
  try {
    const endpoint = childForm.value.id ? '/child/change' : '/child/create';
    const method = childForm.value.id ? 'PATCH' : 'POST';
    
    const payload = childForm.value.id ? {
      id: childForm.value.id,
      new_name: childForm.value.name
    } : {
      name: childForm.value.name,
      grade_id: selectedGrade.value ? selectedGrade.value.id : selectedClass.value.id
    };
    
    const response = await $fetch(buildUrl(apiUrl, endpoint), {
      method,
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
    
    if (childForm.value.id) {
            if (selectedGrade.value) {
        gradeStudents.value = gradeStudents.value.map(c => c.id === response.id ? response : c);
      } else {
        classStudents.value = classStudents.value.map(c => c.id === response.id ? response : c);
      }
    } else {
            if (selectedGrade.value) {
        gradeStudents.value.push(response);
      } else {
        classStudents.value.push(response);
      }
    }
    
    closeChildModal();
  } catch (err) {
    error.value = `Ошибка при ${childForm.value.id ? 'редактировании' : 'добавлении'} ученика`;
    console.error(`Ошибка при ${childForm.value.id ? 'редактировании' : 'добавлении'} ученика:`, err);
  }
};

const openAddTeacherModal = () => {
  teacherForm.value = { id: null, name: '' };
  showTeacherModal.value = true;
};

const openEditTeacherModal = (teacher) => {
  teacherForm.value = { ...teacher };
  showTeacherModal.value = true;
};

const closeTeacherModal = () => {
  showTeacherModal.value = false;
};

const saveTeacher = async () => {
  try {
    const endpoint = teacherForm.value.id ? '/teacher/change' : '/teacher/create';
    const method = teacherForm.value.id ? 'PATCH' : 'POST';
    
    const payload = teacherForm.value.id ? {
      id: teacherForm.value.id,
      new_name: teacherForm.value.name
    } : {
      name: teacherForm.value.name,
      school_id: selectedSchool.value.id
    };
    
    const response = await $fetch(buildUrl(apiUrl, endpoint), {
      method,
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
    
    if (teacherForm.value.id) {
            schoolTeachers.value = schoolTeachers.value.map(t => t.id === response.id ? response : t);
    } else {
            schoolTeachers.value.push(response);
    }
    
    closeTeacherModal();
  } catch (err) {
    error.value = `Ошибка при ${teacherForm.value.id ? 'редактировании' : 'добавлении'} учителя`;
    console.error(`Ошибка при ${teacherForm.value.id ? 'редактировании' : 'добавлении'} учителя:`, err);
  }
};

const openAddAchievementModal = () => {
  achievementForm.value = {
    name: '',
    child_id: null,
    teacher_id: null,
    date: '',
    type: 'Наука',
    level: 'Городской',
    format: 'Очное',
    team: 'Одиночное',
    place: '1-е место'
  };
  showAchievementModal.value = true;
};

const closeAchievementModal = () => {
  showAchievementModal.value = false;
};

const saveAchievement = async () => {
  try {
    const response = await $fetch(buildUrl(apiUrl, '/achievement/create'), {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(achievementForm.value)
    });
    
        closeAchievementModal();
  } catch (err) {
    error.value = 'Ошибка при добавлении достижения';
    console.error('Ошибка при добавлении достижения:', err);
  }
};

const showStudentAchievements = async (childId) => {
  try {
    console.log(`Загрузка достижений для ученика: ${childId}`);
    
        const response = await $fetch(buildUrl(apiUrl, `/achievement/all/${childId}`), {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      }
    });
    
    console.log('Достижения ученика:', response);
    
        if (Array.isArray(response)) {
            studentAchievements.value = response;
    } else if (response.achievements && Array.isArray(response.achievements)) {
            studentAchievements.value = response.achievements;
    } else {
            studentAchievements.value = [];
      console.error('Неожиданная структура ответа:', response);
      error.value = 'Получены некорректные данные от сервера';
    }
    
    showAchievementsModal.value = true;
  } catch (err) {
    error.value = `Ошибка при загрузке достижений ученика ${childId}`;
    console.error('Ошибка при загрузке достижений ученика:', err);
  }
};

const closeAchievementsModal = () => {
  showAchievementsModal.value = false;
  studentAchievements.value = [];
};

const confirmSchool = async (id) => {
  try {
    console.log(`Подтверждение школы с ID: ${id}`);
    await $fetch(buildUrl(apiUrl, `/auth/accounts/${id}/confirm`), {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      }
    });
    
        if (user.value.role === 'mun') {
      schools.value = schools.value.filter(s => s.id !== id);
    } else if (user.value.role === 'owner' && selectedMunicipality.value) {
      municipalitySchools.value = municipalitySchools.value.filter(s => s.id !== id);
    }
  } catch (err) {
    error.value = 'Ошибка при подтверждении школы';
    console.error('Ошибка при подтверждении школы:', err);
  }
};

const rejectSchool = async (id) => {
  try {
    console.log(`Отклонение школы с ID: ${id}`);
    await $fetch(buildUrl(apiUrl, `/auth/accounts/${id}/reject`), {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      }
    });
    
        if (user.value.role === 'mun') {
      schools.value = schools.value.filter(s => s.id !== id);
    } else if (user.value.role === 'owner' && selectedMunicipality.value) {
      municipalitySchools.value = municipalitySchools.value.filter(s => s.id !== id);
    }
  } catch (err) {
    error.value = 'Ошибка при отклонении школы';
    console.error('Ошибка при отклонении школы:', err);
  }
};

onMounted(loadUserData);
</script>

<style scoped>
.loader {
  border-top-color: theme('colors.primary.500');
}
</style>