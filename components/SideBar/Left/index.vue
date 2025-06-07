<template>
  <div class="flex flex-col h-screen p-2">
    <div class="p-2 my-2 rounded-full w-min hover:bg-blue-50 dark:hover:bg-white/20" :class="defaultTransition">
      <NuxtLink to="/">
        <div class="w-8 h-8">
            <FilmIcon />
        </div>
      </NuxtLink>
    </div>

    <div class="mt-2 space-y-2">
      <SidebarLeftTab to="/" :active="isActive('/')">
        <template v-slot:icon><HomeIconOutline /></template>
        <template v-slot:activeIcon><HomeIconSolid /></template>
        <template v-slot:name>Home</template>
      </SidebarLeftTab>
      <SidebarLeftTab to="/movies" :active="isActive('/movies')">
        <template v-slot:icon><FilmIconOutline /></template>
        <template v-slot:activeIcon><FilmIconSolid /></template>
        <template v-slot:name>Movies</template>
      </SidebarLeftTab>
      <SidebarLeftTab to="/favorites" :active="isActive('/favorites')">
        <template v-slot:icon><BookmarkIconOutline /></template>
        <template v-slot:activeIcon><BookmarkIconSolid /></template>
        <template v-slot:name>Favorites</template>
      </SidebarLeftTab>
      <SidebarLeftTab :to="profile.to" :active="isActive(profile.to)">
        <template v-slot:icon><UserIconOutline /></template>
        <template v-slot:activeIcon><UserIconSolid /></template>
        <template v-slot:name>Profile</template>
      </SidebarLeftTab>

       <div v-if="user && user.role === 'admin'" class="pt-2 border-t border-gray-200 dark:border-gray-700">
             <SidebarLeftTab to="/admin/users" :active="isActive('/admin/users')">
                <template v-slot:icon><UsersIconOutline /></template>
                <template v-slot:activeIcon><UsersIconSolid /></template>
                <template v-slot:name>Manage Users</template>
            </SidebarLeftTab>
        </div>
    </div>

    <div class="mt-auto">
      <Menu as="div" class="relative inline-block text-left w-full">
        <div>
          <MenuButton class="flex border-2 items-center w-full p-2 rounded-full hover:bg-gray-200 dark:hover:bg-dim-800" :class="defaultTransition">
            <img :src="user?.profile_picture_url || '/default-avatar.png'" alt="profile" class="w-10 h-10 rounded-full">
            <div class="hidden ml-2 xl:block" v-if="user">
              <p class="text-sm font-bold text-left text-gray-800 dark:text-white">{{ user.full_name }}</p>
              <p class="text-sm text-gray-500">@{{ user.username }}</p>
            </div>
          </MenuButton>
        </div>

        <transition
          enter-active-class="transition duration-100 ease-out"
          enter-from-class="transform scale-95 opacity-0"
          enter-to-class="transform scale-100 opacity-100"
          leave-active-class="transition duration-75 ease-in"
          leave-from-class="transform scale-100 opacity-100"
          leave-to-class="transform scale-95 opacity-0"
        >
          <MenuItems class="absolute bottom-full mb-2 w-64 origin-bottom-left rounded-2xl bg-white dark:bg-dim-700 shadow-lg ring-1 ring-black/5 focus:outline-none">
            <div class="p-1">
              <MenuItem v-slot="{ active }">
                <button @click="handleLogout" :class="[active ? 'bg-gray-100 dark:bg-dim-800' : '', 'group flex w-full items-center rounded-md px-2 py-2 text-sm font-bold text-gray-900 dark:text-white']">
                  <LogoutIcon class="w-5 h-5 mr-2" aria-hidden="true" />
                  Log out @{{ user.username }}
                </button>
              </MenuItem>
            </div>
          </MenuItems>
        </transition>
      </Menu>
    </div>
    </div>
</template>

<script setup>
// Gerekli ikonları ve menü componentlerini import ediyoruz
import { 
  HomeIcon as HomeIconOutline, 
  UserIcon as UserIconOutline, 
  BookmarkIcon as BookmarkIconOutline, 
  FilmIcon as FilmIconOutline,
  UsersIcon as UsersIconOutline, // Yeni ikon
  LogoutIcon 
} from '@heroicons/vue/outline'
import { 
  HomeIcon as HomeIconSolid, 
  UserIcon as UserIconSolid, 
  BookmarkIcon as BookmarkIconSolid, 
  FilmIcon as FilmIconSolid,
  UsersIcon as UsersIconSolid // Yeni ikon (solid)
} from '@heroicons/vue/solid'
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'



// Diğer component ve fonksiyonları import ediyoruz
import SidebarLeftTab from './Tab.vue';
import { useRoute } from 'vue-router';
const { useAuthUser, logout } = useAuth();
const user = useAuthUser();
const { defaultTransition } = useTailwindConfig();
const route = useRoute();

const isActive = (path) => route.path === path;
const profile = { name: 'Profile', to: `/profile/${user.value?.username}` };
const FilmIcon = FilmIconOutline; // Logo için placeholder

// Log out fonksiyonu aynı kalıyor
async function handleLogout() {
  await logout();
  await navigateTo('/login');
}
</script>