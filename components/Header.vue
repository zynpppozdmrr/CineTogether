<template>
    <div class="sticky top-0 z-10 px-4 py-2 bg-white/80 backdrop-blur-md dark:bg-dim-900/80 border-b dark:border-gray-700">
        <div class="flex items-center justify-between">
            
            <div class="flex items-center space-x-2">
                <button v-if="showBackButton" @click="router.back()" class="p-2 -ml-2 rounded-full text-purple-600 hover:bg-gray-100 dark:hover:bg-dim-800">
                    <ArrowLeftIcon class="w-6 h-6" />
                </button>
                <h2 class="text-xl font-bold text-gray-800 dark:text-white">{{ title }}</h2>
            </div>

            <div class="sm:hidden">
                <Menu as="div" class="relative">
                    <MenuButton class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-dim-800">
                        <DotsVerticalIcon class="w-6 h-6 text-gray-800 dark:text-white" />
                    </MenuButton>

                    <transition enter-active-class="transition duration-100 ease-out" enter-from-class="transform scale-95 opacity-0" enter-to-class="transform scale-100 opacity-100" leave-active-class="transition duration-75 ease-in" leave-from-class="transform scale-100 opacity-100" leave-to-class="transform scale-95 opacity-0">
                        <MenuItems class="absolute top-full right-0 mt-2 w-56 origin-top-right rounded-2xl bg-white dark:bg-dim-700 shadow-lg ring-1 ring-black/5 focus:outline-none">
                            <div class="p-1">
                                <MenuItem v-if="user && user.role === 'admin'" v-slot="{ active }">
                                    <NuxtLink to="/admin/users" :class="[active ? 'bg-gray-100 dark:bg-dim-800' : '', 'group flex w-full items-center rounded-md px-2 py-2 text-sm font-bold text-gray-900 dark:text-white']">
                                        <UserGroupIcon class="w-5 h-5 mr-2" />
                                        Manage Users
                                    </NuxtLink>
                                </MenuItem>
                                <MenuItem v-slot="{ active }">
                                    <button @click="toggleTheme" :class="[active ? 'bg-gray-100 dark:bg-dim-800' : '', 'group flex w-full items-center rounded-md px-2 py-2 text-sm font-bold text-gray-900 dark:text-white']">
                                        <template v-if="isDarkMode">
                                            <SunIcon class="w-5 h-5 mr-2" /> Light Mode
                                        </template>
                                        <template v-else>
                                            <MoonIcon class="w-5 h-5 mr-2" /> Dark Mode
                                        </template>
                                    </button>
                                </MenuItem>
                                <MenuItem v-slot="{ active }">
                                    <button @click="handleLogout" :class="[active ? 'bg-gray-100 dark:bg-dim-800' : '', 'group flex w-full items-center rounded-md px-2 py-2 text-sm font-bold text-red-500']">
                                        <LogoutIcon class="w-5 h-5 mr-2" aria-hidden="true" />
                                        Log out
                                    </button>
                                </MenuItem>
                            </div>
                        </MenuItems>
                    </transition>
                </Menu>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import { ArrowLeftIcon, DotsVerticalIcon, SunIcon, MoonIcon, LogoutIcon, UserGroupIcon } from '@heroicons/vue/outline'

const { useAuthUser, logout } = useAuth();
const { isDarkMode, toggleTheme } = useTheme();
const user = useAuthUser();
const route = useRoute();
const router = useRouter();

// Mevcut sayfaya göre başlığı dinamik olarak belirle
const title = computed(() => {
    if (route.name.startsWith('profile-')) return route.params.username;
    if (route.name.startsWith('post-')) return 'Post';
    if (route.name.startsWith('movies-id')) return 'Movie Details';
    if (route.name === 'movies') return 'Movies';
    if (route.name === 'favorites') return 'Favorites';
    if (route.name === 'lists') return 'My Lists';
    if (route.name.startsWith('admin')) return 'Admin';
    return 'Home';
});

// ================== DEĞİŞİKLİK BURADA ==================
// Sadece ana sayfada (path: '/') değilken geri butonunu göster
const showBackButton = computed(() => {
    return route.path !== '/';
});
// =======================================================

async function handleLogout() {
  await logout();
  await navigateTo('/login');
}
</script>