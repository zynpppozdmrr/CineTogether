<template>
  <div class="flex flex-col">

    <div class="relative m-2">
      <div class="absolute flex items-center h-full pl-4 text-gray-600 cursor-pointer">
        <div class="w-6 h-6">
          <IconSearch />
        </div>
      </div>
      <input 
        v-model="search"
        class="flex items-center w-full pl-12 text-sm font-normal text-black bg-gray-200 border border-gray-200 rounded-full shadow dark:text-gray-100 dark:bg-dim-400 dark:border-dim-400 focus:bg-gray-100 dark:focus:bg-dim-900 focus:outline-none focus:border focus:border-blue-200 h-9"
        placeholder="Search Movies..." 
        type="text"
      >
      
      <div v-if="search" class="absolute z-10 w-full mt-1 bg-white dark:bg-dim-700 rounded-2xl shadow-lg border dark:border-gray-600 max-h-96 overflow-y-auto">
        <div v-if="loading" class="p-4 text-center"><UISpinner /></div>
        <div v-else-if="searchResults.length === 0 && search.length > 1" class="p-3 text-sm text-center text-gray-500">No results found for "{{ search }}"</div>
        <div v-else>
          <div v-for="movie in searchResults" :key="movie.id" class="p-3 border-b border-gray-200 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-dim-300">
            <NuxtLink :to="`/movies/${movie.id}`" @click="clearSearch" class="flex items-center">
              <img :src="movie.image" :alt="movie.title" class="w-10 h-14 object-cover rounded-md">
              <div class="ml-3">
                <p class="font-bold text-sm text-gray-800 dark:text-white">{{ movie.title }}</p>
                <p class="text-xs text-gray-500">{{ movie.year }}</p>
              </div>
            </NuxtLink>
          </div>
        </div>
      </div>
      
    </div>

    
    <div class="mt-4 bg-gray-50 dark:bg-dim-700 rounded-2xl">
        <h1 class="p-3 text-xl font-extrabold text-gray-900 border-b border-gray-200 dark:text-white dark:border-dim-200">
            You might like
        </h1>

        <div v-if="pending" class="p-4 flex justify-center"><UISpinner /></div>

        <div v-else-if="error" class="p-3 text-sm text-center text-gray-400">
            Could not load recommendations.
        </div>
        
        <div v-else-if="recommendations && recommendations.length > 0">
            <div v-for="rec in displayedRecommendations" :key="rec.movie_id" class="p-3 border-b border-gray-200 dark:border-gray-600 last:border-b-0">
                <NuxtLink :to="`/movies/${rec.movie_id}`" class="flex items-start space-x-3 hover:bg-gray-100 dark:hover:bg-dim-300 rounded-lg p-2 -m-2">
                    <div class="flex-shrink-0">
                        <img :src="rec.image" :alt="rec.title" class="w-12 h-16 object-cover rounded-md">
                    </div>
                    <div class="flex-1">
                        <p class="font-bold text-sm text-gray-800 dark:text-white line-clamp-2">{{ rec.title }}</p>
                        <p class="text-xs text-gray-500">{{ rec.year }}</p>
                       
                    </div>
                </NuxtLink>
            </div>
        </div>

        <div v-else class="p-3 text-sm text-center text-gray-400">
            Add movies to your favorites to get personalized recommendations.
        </div>
        
         <div v-if="recommendations && recommendations.length > 3" @click="showAllRecommendations = !showAllRecommendations" class="p-3 text-sm text-blue-400 cursor-pointer hover:bg-gray-100 dark:hover:bg-dim-300 rounded-b-2xl text-center">
            {{ showAllRecommendations ? 'Show less' : 'Show more' }}
        </div>
    </div>
    
    
  </div>
</template>

<script setup>
import IconSearch from '~/components/Icon/Search.vue';
import UISpinner from '~/components/UI/Spinner.vue';

const search = ref('');
const searchResults = ref([]);
const loading = ref(false);
let debounceTimer = null;

// 'search' ref'ini izliyoruz
watch(search, (newValue) => {
  // Her tuşa basıldığında önceki zamanlayıcıyı temizle
  clearTimeout(debounceTimer);

  // Eğer arama kutusu boşsa, sonuçları temizle ve bitir
  if (!newValue) {
    searchResults.value = [];
    return;
  }
  
  // Kullanıcı yazmayı bıraktıktan 300ms sonra arama yap
  debounceTimer = setTimeout(() => {
    performSearch(newValue);
  }, 300);
});

// Backend'e arama isteği gönderen fonksiyon
async function performSearch(query) {
  if (query.length < 2) {
    searchResults.value = [];
    return;
  }

  loading.value = true;
  try {
    const response = await $fetch(`/api/movies/search?title=${query}`, {
      baseURL: 'http://127.0.0.1:5000'
    });
    searchResults.value = response.movies;
  } catch (error) {
    console.error("Search failed:", error);
    searchResults.value = [];
  } finally {
    loading.value = false;
  }
}


function clearSearch() {
  search.value = '';
  searchResults.value = [];
}

// ================== ÖNERİ MANTIĞI GÜNCELLENDİ ==================

// 1. API'den veriyi çekiyoruz (bu kısım aynı)
const { data: recommendations, pending, error } = await useAsyncData(
    'user-recommendations',
    () => useApiFetch('/api/recommendations/').then(res => res.data.value.recommendations)
);

// 2. Diziyi karıştırmak için bir fonksiyon yazıyoruz (Fisher-Yates shuffle)
const shuffleArray = (array) => {
    if (!array || array.length === 0) return [];
    const newArr = [...array]; // Orijinal diziyi bozmamak için kopyasını oluştur
    for (let i = newArr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [newArr[i], newArr[j]] = [newArr[j], newArr[i]];
    }
    return newArr;
};

// 3. Karıştırılmış listeyi tutan bir computed değişkeni oluşturuyoruz
const shuffledRecommendations = computed(() => shuffleArray(recommendations.value));


// 4. Gösterilecek listeyi, bu karıştırılmış listeye göre ayarlıyoruz
const showAllRecommendations = ref(false);

const displayedRecommendations = computed(() => {
    if (!shuffledRecommendations.value) {
        return [];
    }
    if (showAllRecommendations.value) {
        return shuffledRecommendations.value; // Hepsini göster
    }
    return shuffledRecommendations.value.slice(0, 3); // Sadece ilk 3'ü göster
});
// ==========================================================

</script>