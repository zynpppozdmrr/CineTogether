<template>
  <div class="flex flex-col">
    <div class="relative m-2">
      <div class="absolute flex items-center h-full pl-4 text-gray-600 cursor-pointer">
        <div class="w-6 h-6">
          <IconSearch @click="handleSearch" />
        </div>
      </div>
      <input v-model="search"
        class="flex items-center w-full pl-12 text-sm font-normal text-black bg-gray-200 border border-gray-200 rounded-full shadow dark:text-gray-100 dark:bg-dim-400 dark:border-dim-400 focus:bg-gray-100 dark:focus:bg-dim-900 focus:outline-none focus:border focus:border-blue-200 h-9"
        placeholder="Search..." type="text">
    </div>

    <div class="mt-4 bg-gray-50 dark:bg-dim-700 rounded-2xl">
        <h1 class="p-3 text-xl font-extrabold text-gray-900 border-b border-gray-200 dark:text-white dark:border-dim-200">
            For Your Interest
        </h1>

        <div class="p-3 hover:bg-gray-100 dark:hover:bg-dim-300 cursor-pointer">
            <h2 class="text-md font-bold text-gray-800 dark:text-white">#CineTogether</h2>
            <p class="text-xs text-gray-400">1.2k posts</p>
        </div>
         <div class="p-3 hover:bg-gray-100 dark:hover:bg-dim-300 cursor-pointer">
            <h2 class="text-md font-bold text-gray-800 dark:text-white">#YeniFilm</h2>
            <p class="text-xs text-gray-400">987 posts</p>
        </div>
        
    </div>

  </div>
</template>
<script setup>
const search = ref('')
function handleSearch() {
    // Arama işlemleri burada yapılacak
    console.log('Searching for:', search.value)
}
</script>