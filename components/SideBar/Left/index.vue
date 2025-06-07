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
      <SidebarLeftTab :to="home.to" :active="isActive(home.to)">
        <template v-slot:icon>
          <HomeIconOutline />
        </template>
        <template v-slot:activeIcon>
          <HomeIconSolid />
        </template>
        <template v-slot:name>
          {{ home.name }}
        </template>
      </SidebarLeftTab>

      <SidebarLeftTab :to="movies.to" :active="isActive(movies.to)">
        <template v-slot:icon>
          <FilmIconOutline />
        </template>
        <template v-slot:activeIcon>
          <FilmIconSolid />
        </template>
        <template v-slot:name>
          {{ movies.name }}
        </template>
      </SidebarLeftTab>

      <SidebarLeftTab :to="favorites.to" :active="isActive(favorites.to)">
        <template v-slot:icon>
          <BookmarkIconOutline />
        </template>
        <template v-slot:activeIcon>
          <BookmarkIconSolid />
        </template>
        <template v-slot:name>
          {{ favorites.name }}
        </template>
      </SidebarLeftTab>

      <SidebarLeftTab :to="profile.to" :active="isActive(profile.to)">
        <template v-slot:icon>
          <UserIconOutline />
        </template>
        <template v-slot:activeIcon>
          <UserIconSolid />
        </template>
        <template v-slot:name>
          {{ profile.name }}
        </template>
      </SidebarLeftTab>
    </div>
  </div>
</template>

<script setup>
import { HomeIcon as HomeIconOutline, UserIcon as UserIconOutline, BookmarkIcon as BookmarkIconOutline, FilmIcon as FilmIconOutline } from '@heroicons/vue/outline'
import { HomeIcon as HomeIconSolid, UserIcon as UserIconSolid, BookmarkIcon as BookmarkIconSolid, FilmIcon as FilmIconSolid } from '@heroicons/vue/solid'
import SidebarLeftTab from './Tab.vue';
import { useRoute } from 'vue-router'

// Get the logged-in user's data
const { useAuthUser } = useAuth()
const user = useAuthUser()

const { defaultTransition } = useTailwindConfig();
const route = useRoute();

const isActive = (path) => route.path === path;

const home = { name: 'Home', to: '/' };
const movies = { name: 'Movies', to: '/movies' };
const favorites = { name: 'Favorites', to: '/favorites' };
// Update the profile object to have a dynamic 'to' link
const profile = { name: 'Profile', to: `/profile/${user.value?.username}` };

const FilmIcon = FilmIconOutline;
</script>