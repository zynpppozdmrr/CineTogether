<template>
    <div>
        
        <div class="flex border-b border-gray-200 dark:border-gray-700">
            <button @click="selectedTab = 'watchlist'" :class="tabClass('watchlist')" class="flex-1 p-3 font-semibold text-center hover:bg-gray-100 dark:hover:bg-dim-800 transition-colors">
                My Watchlist
            </button>
            <button @click="selectedTab = 'watched'" :class="tabClass('watched')" class="flex-1 p-3 font-semibold text-center hover:bg-gray-100 dark:hover:bg-dim-800 transition-colors">
                Watched Movies
            </button>
        </div>

        <div v-if="pending" class="flex items-center justify-center p-8">
            <UISpinner />
        </div>

        <div v-else-if="error" class="p-4 text-center text-red-500">
            <p>Could not load your lists. Please try again later.</p>
        </div>

        <div v-else class="p-4 sm:p-6 lg:p-8">
            <div v-if="selectedTab === 'watchlist'">
                <div v-if="watchlistMovies && watchlistMovies.length > 0" class="grid grid-cols-3 gap-4">
                    <MovieCard v-for="movie in watchlistMovies" :key="movie.id" :movie="movie" />
                </div>
                <div v-else class="text-center text-gray-500"><p>Your watchlist is empty.</p></div>
            </div>
            
            <div v-if="selectedTab === 'watched'">
                <div v-if="watchedMovies && watchedMovies.length > 0" class="grid grid-cols-3 gap-4">
                    <MovieCard v-for="movie in watchedMovies" :key="movie.id" :movie="movie" />
                </div>
                <div v-else class="text-center text-gray-500"><p>You haven't marked any movies as watched yet.</p></div>
            </div>
        </div>
    </div>
</template>

<script setup>
import MovieCard from '~/components/Movie/Card.vue';
import UISpinner from '~/components/UI/Spinner.vue';

const { useAuthUser } = useAuth();
const user = useAuthUser();

const selectedTab = ref('watchlist'); // 'watchlist' or 'watched'

// Fetch both watchlist and watched list data
const { data, pending, error } = await useAsyncData(
    'user-lists',
    () => {
        if (!user.value) {
            return { watchlist: [], watched: [] };
        }
        return Promise.all([
            $fetch(`/api/watchlists/user/${user.value.id}`, { baseURL: 'http://127.0.0.1:5000' }),
            $fetch(`/api/watched/user/${user.value.id}`, { baseURL: 'http://127.0.0.1:5000' })
        ]).then(([watchlistRes, watchedRes]) => {
            return {
                watchlist: watchlistRes.watchlist || [],
                watched: watchedRes.watched || []
            };
        });
    }
);

// Helper function to format data for MovieCard component
const formatMovies = (movieList) => {
    return movieList.map(item => ({
        ...item,
        id: item.movie_id,
        rating: item.rating || 'N/A' // Add a fallback for rating
    }));
};

const watchlistMovies = computed(() => formatMovies(data.value?.watchlist || []));
const watchedMovies = computed(() => formatMovies(data.value?.watched || []));

// Dynamic class for the active tab
const tabClass = (tabName) => {
    return selectedTab.value === tabName
        ? 'text-purple-500 border-b-2 border-purple-500'
        : 'text-gray-500';
};


</script>