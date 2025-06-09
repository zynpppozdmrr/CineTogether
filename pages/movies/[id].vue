<template>
    <div>
        <transition name="fade">
            <div v-if="showNotification" class="fixed top-20 right-5 bg-green-500 text-white py-2 px-4 rounded-lg shadow-lg z-50">
                {{ notificationMessage }}
            </div>
        </transition>
        
        

        <div v-if="pending" class="flex items-center justify-center p-8">
            <UISpinner />
        </div>

        <div v-else-if="error || !movie" class="p-4 text-center text-red-500">
            <p>Could not load movie details.</p>
        </div>

        <div v-else class="p-4 sm:p-6">
            <div class="flex flex-row gap-4 sm:gap-6">
                
                <div class="w-1/3 flex-shrink-0">
                    <img :src="movie.image" :alt="movie.title" class="rounded-lg shadow-2xl w-full">
                </div>
                
                <div class="w-2/3">
                    <h1 class="text-xl sm:text-2xl md:text-4xl font-extrabold tracking-tight text-gray-900 dark:text-white">{{ movie.title }} <span class="font-light text-lg md:text-2xl text-gray-400">({{ movie.year }})</span></h1>
                    
                    <div class="flex flex-wrap gap-1 sm:gap-2 mt-2 sm:mt-4">
                        <span v-for="genre in genres" :key="genre" class="px-2 py-0.5 text-[10px] sm:text-xs font-medium text-purple-800 bg-purple-100 rounded-full dark:bg-purple-900 dark:text-purple-200">
                          {{ genre }}
                        </span>

                    </div>

                    <div class="flex flex-col sm:flex-row items-start sm:items-center mt-3 sm:mt-6 sm:space-x-4">
                        <div class="flex items-center">
                            <span class="text-yellow-400 text-lg sm:text-2xl font-bold">★</span>
                            <span class="ml-2 text-lg sm:text-2xl font-bold text-gray-800 dark:text-white">{{ movie.rating }}</span>
                            <span class="ml-1 text-xs sm:text-sm text-gray-500">/ 10 IMDb</span>
                        </div>
                        <div v-if="averageRating > 0" class="flex items-center mt-1 sm:mt-0">
    <span class="text-purple-400 text-lg sm:text-2xl font-bold">♥</span>
    <span class="ml-2 text-lg sm:text-2xl font-bold text-gray-800 dark:text-white">{{ averageRating }}</span>
    <span class="ml-1 text-xs sm:text-sm text-gray-500">/ 10 CineTogether</span>
</div>
                    </div>

                    <div class="mt-4">
                        <h2 class="text-lg sm:text-xl font-semibold dark:text-white mb-1 sm:mb-2">Plot Summary</h2>
                        <p class="text-xs sm:text-sm text-gray-700 dark:text-gray-300 leading-relaxed">{{ movie.description }}</p>
                    </div>

                    <div class="flex flex-wrap gap-2 sm:gap-4 mt-4 sm:mt-8">
                        <button @click="handleToggleFavorite" :disabled="isActionLoading" class="flex items-center px-5 py-3 text-sm font-semibold rounded-lg transition-colors disabled:opacity-50"
    :class="isFavorited ? 'bg-pink-600 text-white hover:bg-pink-700' : 'bg-purple-600 text-white hover:bg-purple-700'">
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

                        <button @click="handleToggleWatched" :disabled="isActionLoading" class="flex items-center px-5 py-3 text-sm font-semibold rounded-lg transition-colors disabled:opacity-50"
                            :class="isWatched ? 'bg-green-600 text-white hover:bg-green-700' : 'bg-gray-200 text-gray-800 hover:bg-gray-300 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600'">
                            <CheckCircleIcon v-if="isWatched" class="w-5 h-5 mr-2" />
                            <PlusCircleIcon v-else class="w-5 h-5 mr-2" />
                            {{ isWatched ? 'Watched' : 'Mark as Watched' }}
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
import { BookmarkIcon as BookmarkIconOutline,PlusCircleIcon } from '@heroicons/vue/outline';
import { BookmarkIcon as BookmarkIconSolid,EyeIcon,PlusIcon, CheckCircleIcon } from '@heroicons/vue/solid';
import { useFavorites } from '~/composables/useFavorites.js';
import { useWatchlist } from '~/composables/useWatchlist.js';
import { useWatched } from '~/composables/useWatched.js' 

const route = useRoute();
const router = useRouter();
const movieId = route.params.id;
const { useAuthUser } = useAuth();
const { addFavorite, removeFavorite } = useFavorites();
const { addToWatchlist, removeFromWatchlist } = useWatchlist();
const { markAsWatched, removeFromWatched } = useWatched(); 
const user = useAuthUser();
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const isActionLoading = ref(false);
const notificationMessage = ref('');
const showNotification = ref(false);
let notificationTimer = null;

// Gerekli tüm verileri tek seferde ve güvenli bir şekilde çekiyoruz
const { data, pending, error, refresh } = await useAsyncData(
    `movie-data-${movieId}`,
    async () => {
        try {
            const movieRes = await $fetch(`/api/movies/${movieId}`, { baseURL: apiBase });
            if (!movieRes.movie) throw new Error("Movie not found");

            // Fetch average rating for the movie
            const avgRatingRes = await $fetch(`/api/ratings/movie/${movieId}/average`, { baseURL: apiBase });

            // If user is not logged in, return public data
            if (!user.value) {
                return { 
                    movie: movieRes.movie, 
                    favorites: [], 
                    userRatings: [], 
                    watchlist: [],
                    watched: [],
                    averageRating: avgRatingRes.average_rating || 0
                };
            }

            // If user is logged in, fetch their specific data
            const [favoritesRes, ratingsRes, watchlistRes,watchedRes] = await Promise.all([
                $fetch(`/api/favorites/user/${user.value.id}`, { baseURL: apiBase }),
                $fetch(`/api/ratings/user/${user.value.id}`, { baseURL: apiBase }),
                $fetch(`/api/watchlists/user/${user.value.id}`, { baseURL: apiBase }),
                $fetch(`/api/watched/user/${user.value.id}`, { baseURL: apiBase })
            ]);


            return {
                movie: movieRes.movie,
                favorites: favoritesRes.favorites || [],
                userRatings: ratingsRes.watch_history || [],
                watchlist: watchlistRes.watchlist || [],
                watched: watchedRes.watched || [], 
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
const watched = ref(data.value?.watched || []);

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

// YENİ: Filmin izlenenler listesinde olup olmadığını kontrol et
const isWatched = computed(() => {
    if (!movie.value) return false;
    return watched.value.some(item => item.movie_id === movie.value.id);
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

// YENİ: İzlenenler listesi butonunun fonksiyonu
async function handleToggleWatched() {
    isActionLoading.value = true;
    try {
        if (isWatched.value) {
            await removeFromWatched(movie.value.id);
            const index = watched.value.findIndex(item => item.movie_id === movie.value.id);
            if (index !== -1) watched.value.splice(index, 1);
            triggerNotification(`'${movie.value.title}' removed from watched list.`);
        } else {
            await markAsWatched(movie.value.id);
            watched.value.push({ movie_id: movie.value.id });
            triggerNotification(`'${movie.value.title}' marked as watched!`);
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