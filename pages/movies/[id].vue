<template>
    <div>
        <transition name="fade">
            <div v-if="showNotification" class="fixed top-20 right-5 bg-green-500 text-white py-2 px-4 rounded-lg shadow-lg z-50">
                {{ notificationMessage }}
            </div>
        </transition>
        
        <div class="sticky top-0 z-10 px-4 py-2 bg-white/80 backdrop-blur-md dark:bg-dim-900/80 border-b dark:border-gray-700">
            <div class="flex items-center">
                <button @click="router.back()" class="p-2 mr-4 rounded-full hover:bg-gray-100 dark:hover:bg-dim-800">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                </button>
                <h2 class="text-lg font-bold truncate">{{ movie?.title }}</h2>
            </div>
        </div>

        <div v-if="pending" class="flex items-center justify-center p-8">
            <UISpinner />
        </div>

        <div v-else-if="error || !movie" class="p-4 text-center text-red-500">
            <p>Could not load movie details.</p>
        </div>

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

                    <div class="flex items-center mt-6 space-x-6">
                        <div class="flex items-center">
                            <span class="text-yellow-400 text-2xl font-bold">★</span>
                            <span class="ml-2 text-2xl font-bold text-gray-800 dark:text-white">{{ movie.rating }}</span>
                            <span class="ml-1 text-sm text-gray-500">/ 10 IMDb</span>
                        </div>
                        <div v-if="averageRating > 0" class="flex items-center">
                            <span class="text-blue-400 text-2xl font-bold">♥</span>
                            <span class="ml-2 text-2xl font-bold text-gray-800 dark:text-white">{{ averageRating }}</span>
                            <span class="ml-1 text-sm text-gray-500">/ 10 CineTogether</span>
                        </div>
                    </div>

                    <div class="mt-6">
                        <h2 class="text-xl font-semibold dark:text-white mb-2">Plot Summary</h2>
                        <p class="text-gray-700 dark:text-gray-300 leading-relaxed">{{ movie.description }}</p>
                    </div>

                    <div class="flex flex-wrap gap-4 mt-8">
                        <button @click="handleToggleFavorite" :disabled="isActionLoading" class="flex items-center px-5 py-3 text-sm font-semibold rounded-lg transition-colors disabled:opacity-50"
                            :class="isFavorited ? 'bg-pink-600 text-white hover:bg-pink-700' : 'bg-blue-600 text-white hover:bg-blue-700'">
                            <BookmarkIconSolid v-if="isFavorited" class="w-5 h-5 mr-2" />
                            <BookmarkIconOutline v-else class="w-5 h-5 mr-2" />
                            {{ isFavorited ? 'In Favorites' : 'Add to Favorites' }}
                        </button>
                        
                        <button @click="handleToggleWatchlist" :disabled="isActionLoading" class="flex items-center px-5 py-3 text-sm font-semibold rounded-lg transition-colors disabled:opacity-50"
                            :class="isOnWatchlist ? 'bg-gray-600 text-white hover:bg-gray-700' : 'bg-gray-200 text-gray-800 hover:bg-gray-300 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600'">
                            <EyeIcon v-if="isOnWatchlist" class="w-5 h-5 mr-2" />
                            <PlusIcon v-else class="w-5 h-5 mr-2" />
                            {{ isOnWatchlist ? 'On Watchlist' : 'Add to Watchlist' }}
                        </button>

                        <a :href="movie.imdb_link" target="_blank" rel="noopener noreferrer" class="inline-block px-5 py-3 text-sm font-semibold text-gray-800 bg-yellow-400 rounded-lg hover:bg-yellow-500">
                            View on IMDb
                        </a>
                    </div>
                </div>
            </div>

            <MovieRating v-if="user" :movieId="movieId" :currentUserRating="currentUserRating" @onSuccess="refresh" />
        </div>
    </div>
</template>

<script setup>
import UISpinner from '~/components/UI/Spinner.vue';
import MovieRating from '~/components/Movie/Rating.vue';
import { BookmarkIcon as BookmarkIconOutline } from '@heroicons/vue/outline';
import { BookmarkIcon as BookmarkIconSolid,EyeIcon,PlusIcon } from '@heroicons/vue/solid';
import { useFavorites } from '~/composables/useFavorites.js';
import { useWatchlist } from '~/composables/useWatchlist.js';

const route = useRoute();
const router = useRouter();
const movieId = route.params.id;
const { useAuthUser } = useAuth();
const { addFavorite, removeFavorite } = useFavorites();
const { addToWatchlist, removeFromWatchlist } = useWatchlist(); // Yeni fonksiyonları al
const user = useAuthUser();

const isActionLoading = ref(false);
const notificationMessage = ref('');
const showNotification = ref(false);
let notificationTimer = null;

// Gerekli tüm verileri tek seferde ve güvenli bir şekilde çekiyoruz
const { data, pending, error, refresh } = await useAsyncData(
    `movie-data-${movieId}`,
    async () => {
        try {
            const movieRes = await $fetch(`/api/movies/${movieId}`, { baseURL: 'http://127.0.0.1:5000' });
            if (!movieRes.movie) throw new Error("Movie not found");

            // Fetch average rating for the movie
            const avgRatingRes = await $fetch(`/api/ratings/movie/${movieId}/average`, { baseURL: 'http://127.0.0.1:5000' });

            // If user is not logged in, return public data
            if (!user.value) {
                return { 
                    movie: movieRes.movie, 
                    favorites: [], 
                    userRatings: [], 
                    watchlist: [],
                    averageRating: avgRatingRes.average_rating || 0
                };
            }

            // If user is logged in, fetch their specific data
            const [favoritesRes, ratingsRes, watchlistRes] = await Promise.all([
                $fetch(`/api/favorites/user/${user.value.id}`, { baseURL: 'http://127.0.0.1:5000' }),
                $fetch(`/api/ratings/user/${user.value.id}`, { baseURL: 'http://127.0.0.1:5000' }),
                $fetch(`/api/watchlists/user/${user.value.id}`, { baseURL: 'http://127.0.0.1:5000' })
            ]);

            return {
                movie: movieRes.movie,
                favorites: favoritesRes.favorites || [],
                userRatings: ratingsRes.watch_history || [],
                watchlist: watchlistRes.watchlist || [],
                averageRating: avgRatingRes.average_rating || 0
            };
        } catch (e) {
            console.error(e);
            return { movie: null, favorites: [], userRatings: [], watchlist: [], averageRating: 0 };
        }
    }
);

// Verileri güvenli bir şekilde kullanmak için computed değişkenler
const movie = computed(() => data.value?.movie);
const favorites = ref(data.value?.favorites || []);
const watchlist = ref(data.value?.watchlist || []); // watchlist verisini reaktif yap
const averageRating = computed(() => data.value?.averageRating);
const genres = computed(() => movie.value?.genre ? movie.value.genre.split(',').map(g => g.trim()) : []);

const currentUserRating = computed(() => {
    if (!data.value?.userRatings) return null;
    return data.value.userRatings.find(r => r.movie_id === parseInt(movieId));
});

const isFavorited = computed(() => {
    if (!movie.value) return false;
    return favorites.value.some(fav => fav.movie_id === movie.value.id);
});

// YENİ: Filmin izleme listesinde olup olmadığını kontrol et
const isOnWatchlist = computed(() => {
    if (!movie.value) return false;
    return watchlist.value.some(item => item.movie_id === movie.value.id);
});


// Favori ekleme/çıkarma fonksiyonu
async function handleToggleFavorite() {
    isActionLoading.value = true;
    try {
        if (isFavorited.value) {
            await removeFavorite(movie.value.id);
            const index = favorites.value.findIndex(fav => fav.movie_id === movie.value.id);
            if (index !== -1) favorites.value.splice(index, 1);
            triggerNotification(`'${movie.value.title}' removed from favorites.`);
        } else {
            await addFavorite(movie.value.id);
            favorites.value.push({ movie_id: movie.value.id });
            triggerNotification(`'${movie.value.title}' added to favorites!`);
        }
    } catch (e) { console.error(e); } finally {
        isActionLoading.value = false;
    }
}

// YENİ: İzleme listesi butonunun fonksiyonu
async function handleToggleWatchlist() {
    isActionLoading.value = true;
    try {
        if (isOnWatchlist.value) {
            await removeFromWatchlist(movie.value.id);
            const index = watchlist.value.findIndex(item => item.movie_id === movie.value.id);
            if (index !== -1) watchlist.value.splice(index, 1);
            triggerNotification(`'${movie.value.title}' removed from watchlist.`);
        } else {
            await addToWatchlist(movie.value.id);
            watchlist.value.push({ movie_id: movie.value.id });
            triggerNotification(`'${movie.value.title}' added to watchlist!`);
        }
    } catch (e) { console.error(e); }
    finally { isActionLoading.value = false; }
}

// Bildirim gösterme fonksiyonu
function triggerNotification(message) {
    notificationMessage.value = message;
    showNotification.value = true;
    if (notificationTimer) clearTimeout(notificationTimer);
    notificationTimer = setTimeout(() => {
        showNotification.value = false;
    }, 3000);
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: all 0.5s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-20px); }
</style>