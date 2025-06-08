<template>
    <div>
        <div class="sticky top-0 z-10 px-4 py-2 bg-white/80 backdrop-blur-md dark:bg-dim-900/80 border-b dark:border-gray-700">
            <div class="flex items-center">
                <button @click="router.back()" class="p-2 mr-4 rounded-full hover:bg-gray-100 dark:hover:bg-dim-800">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                </button>
                <h2 class="text-lg font-bold truncate">{{ movie?.title }}</h2>
            </div>
        </div>

        <div v-if="pending" class="flex items-center justify-center p-8"> <UISpinner /> </div>
        <div v-else-if="error || !movie" class="p-4 text-center text-red-500"> <p>Could not load movie details.</p> </div>

        <div v-else class="p-4 sm:p-6 lg:p-8">
            <div class="flex flex-col md:flex-row gap-8">
                <div class="w-full md:w-1/3 lg:w-1/4">
                    <img :src="movie.image" :alt="movie.title" class="rounded-lg shadow-2xl w-full">
                </div>
                <div class="w-full md:w-2/3 lg:w-3/4">
                    <h1 class="text-4xl font-extrabold tracking-tight text-gray-900 dark:text-white">{{ movie.title }} <span class="font-light text-2xl text-gray-400">({{ movie.year }})</span></h1>
                    <div class="flex flex-wrap gap-2 mt-4">
                        <span v-for="genre in genres" :key="genre" class="px-3 py-1 text-xs font-medium text-blue-800 bg-blue-100 rounded-full dark:bg-blue-900 dark:text-blue-200">
                            {{ genre }}
                        </span>
                    </div>
                    <div class="flex items-center mt-6">
                        <span class="text-yellow-400 text-2xl font-bold">★</span>
                        <span class="ml-2 text-2xl font-bold text-gray-800 dark:text-white">{{ movie.rating }}</span>
                        <span class="ml-1 text-sm text-gray-500">/ 10 IMDb</span>
                    </div>
                    <div class="mt-6">
                        <h2 class="text-xl font-semibold dark:text-white mb-2">Plot Summary</h2>
                        <p class="text-gray-700 dark:text-gray-300 leading-relaxed">{{ movie.description }}</p>
                    </div>
                    <div class="flex flex-wrap gap-4 mt-8">
                        <button class="px-5 py-3 text-sm font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700">Add to Favorites</button>
                        <button class="px-5 py-3 text-sm font-semibold text-gray-800 bg-gray-200 rounded-lg hover:bg-gray-300 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600">Add to Watchlist</button>
                        <a :href="movie.imdb_link" target="_blank" rel="noopener noreferrer" class="px-5 py-3 text-sm font-semibold text-gray-800 bg-yellow-400 rounded-lg hover:bg-yellow-500">
                            View on IMDb
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import UISpinner from '~/components/UI/Spinner.vue';

const route = useRoute();
const router = useRouter();
const movieId = route.params.id;

const { data: movie, pending, error } = await useAsyncData(
    `movie-${movieId}`,
    () => $fetch(`/api/movies/${movieId}`, { baseURL: 'http://127.0.0.1:5000' }).then(res => res.movie)
);

const genres = computed(() => {
    if (movie.value?.genre) {
        return movie.value.genre.split(',').map(g => g.trim());
    }
    return [];
});
</script>