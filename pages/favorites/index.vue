<template>
    <div>
        <div class="sticky top-0 z-10 px-4 py-2 bg-white/80 backdrop-blur-md dark:bg-dim-900/80 border-b dark:border-gray-700">
            <h2 class="text-xl font-bold text-gray-800 dark:text-white">My Favorite Movies</h2>
        </div>

        <div v-if="pending" class="flex items-center justify-center p-8">
            <UISpinner />
        </div>

        <div v-else-if="error" class="p-4 text-center text-red-500">
            <p>Could not load your favorites. Please try again later.</p>
        </div>

        <div v-else-if="favoriteMovies && favoriteMovies.length > 0" class="p-4">
            <div class="grid grid-cols-3 gap-4">
                <MovieCard v-for="movie in favoriteMovies" :key="movie.id" :movie="movie" />
            </div>
        </div>
        <div v-else class="p-4 text-center text-gray-500">
            <p>You haven't added any movies to your favorites yet.</p>
        </div>
    </div>
</template>

<script setup>
import MovieCard from '~/components/Movie/Card.vue';
import UISpinner from '~/components/UI/Spinner.vue';

const { useAuthUser } = useAuth();
const user = useAuthUser();

// Fetch the logged-in user's favorite movies
const { data: favoriteMovies, pending, error } = await useAsyncData(
    'user-favorites',
    () => {
        if (!user.value) {
            return [];
        }
        return $fetch(`/api/favorites/user/${user.value.id}`, { baseURL: 'http://127.0.0.1:5000' })
               .then(res => {
                    // Match the data structure expected by the MovieCard component
                    return res.favorites.map(fav => ({
                        ...fav,
                        id: fav.movie_id 
                    }));
               });
    }
);
</script>