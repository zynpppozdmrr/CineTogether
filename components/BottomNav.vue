<template>
    <div class="sm:hidden fixed bottom-0 left-0 z-50 w-full h-16 bg-white border-t border-gray-200 dark:bg-dim-900 dark:border-gray-700">
        <div class="grid h-full max-w-lg grid-cols-5 mx-auto font-medium">
            
            <NuxtLink to="/movies" class="inline-flex flex-col items-center justify-center px-5 hover:bg-gray-50 dark:hover:bg-gray-800 group" active-class="text-blue-500">
                <FilmIcon class="w-6 h-6 mb-1 text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500" />
                <span class="text-xs">Movies</span>
            </NuxtLink>

            <NuxtLink to="/lists" class="inline-flex flex-col items-center justify-center px-5 hover:bg-gray-50 dark:hover:bg-gray-800 group" active-class="text-blue-500">
                <ViewListIcon class="w-6 h-6 mb-1 text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500" />
                <span class="text-xs">Lists</span>
            </NuxtLink>

            <NuxtLink to="/favorites" class="inline-flex flex-col items-center justify-center px-5 hover:bg-gray-50 dark:hover:bg-gray-800 group" active-class="text-blue-500">
                <BookmarkIcon class="w-6 h-6 mb-1 text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500" />
                <span class="text-xs">Favorites</span>
            </NuxtLink>

            <button @click="$emit('openSearch')" type="button" class="inline-flex flex-col items-center justify-center px-5 hover:bg-gray-50 dark:hover:bg-gray-800 group">
                <SearchIcon class="w-6 h-6 mb-1 text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500" />
                <span class="text-xs text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500">Search</span>
            </button>

            <NuxtLink v-if="user" :to="'/profile/' + user.username" class="inline-flex flex-col items-center justify-center px-5 hover:bg-gray-50 dark:hover:bg-gray-800 group" active-class="text-blue-500">
                <UserIcon class="w-6 h-6 mb-1 text-gray-500 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500" />
                <span class="text-xs">Profile</span>
            </NuxtLink>

        </div>
    </div>
</template>

<script setup>
import { FilmIcon, ViewListIcon, BookmarkIcon, SearchIcon, UserIcon } from '@heroicons/vue/outline';

const { useAuthUser } = useAuth();
const user = useAuthUser();

// Artık sadece 'openSearch' olayını yayıyoruz
defineEmits(['openSearch']);
</script>