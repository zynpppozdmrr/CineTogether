<template>
  <div class="min-h-full bg-white dark:bg-dim-900">
    <div class="container mx-auto">
        <div class="grid grid-cols-12">

            <div class="hidden sm:block col-span-1 xl:col-span-2">
                <div class="sticky top-0">
                    <SidebarLeft />
                </div>
            </div>

            <main class="col-span-12 sm:col-span-11 md:col-span-8 xl:col-span-6 border-x dark:border-gray-700">
                <NuxtPage />
            </main>

            <div class="hidden md:block col-span-12 md:col-span-3 xl:col-span-4">
                <div class="sticky top-0">
                    <SidebarRight />
                </div>
            </div>

        </div>
    </div>
  </div>
</template>


<script setup>
// Import components from the exact paths you provided
import SidebarLeft from '~/components/SideBar/Left/index.vue';
import SidebarRight from '~/components/SideBar/Right/index.vue';
</script>