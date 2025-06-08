<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-8 text-center text-gray-900 dark:text-gray-100">Top 100 IMDb Movies</h1>
    
    <div v-if="pending" class="flex justify-center items-center py-10">
      <UISpinner />
    </div>
    
    <div v-else-if="error" class="text-center text-red-500">
      <p>Could not load movies. Please try again later.</p>
    </div>
    
    <div v-else-if="movies && movies.length"  class="grid grid-cols-3 gap-3 sm:gap-4 md:gap-6"> 
      <MovieCard v-for="movie in movies" :key="movie.id" :movie="movie" />
    </div>
    
    <div v-else class="text-center text-gray-700 dark:text-gray-300">
      <p>No movies found.</p>
    </div>
  </div>
</template>

<script setup>
import MovieCard from '~/components/Movie/Card.vue';
import UISpinner from '~/components/UI/Spinner.vue';

// `useAsyncData` ile veriyi güvenli bir şekilde çekiyoruz
const { data: movies, pending, error } = await useAsyncData(
    'movies-list',
    // Backend'den gelen yanıtın içindeki 'movies' dizisini alıyoruz
    () => $fetch('/api/movies/', { baseURL: 'http://127.0.0.1:5000' }).then(res => res.movies)
);
</script>