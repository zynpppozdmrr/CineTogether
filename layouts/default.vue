<template>
  <div class="min-h-screen bg-white dark:bg-dim-900">
    
    <Transition name="slide-right">
        <div v-if="showRightSidebar" class="fixed top-0 right-0 w-80 h-full bg-white dark:bg-dim-900 z-50 shadow-lg">
             <SidebarRight />
        </div>
    </Transition>
    <div v-if="showRightSidebar" @click="closeSidebars" class="fixed inset-0 bg-black/40 z-40"></div>

   <div class="container mx-auto">
        <div class="grid grid-cols-12 mx-auto sm:px-6 lg:max-w-7xl lg:px-8 lg:gap-5">

            <div class="hidden sm:block md:col-span-1 xl:col-span-3">
                <div class="sticky top-0">
                    <SidebarLeft />
                </div>
            </div>

            <main class="col-span-12 sm:col-span-11 md:col-span-8 xl:col-span-5 border-x dark:border-gray-700 min-h-screen pb-16 sm:pb-0">
                <Header/>
                <slot />
            </main>

            <div class="hidden md:block col-span-12 md:col-span-3 xl:col-span-4">
                <div class="sticky top-0">
                    <SidebarRight />
                </div>
            </div>

        </div>
        </div>

    <BottomNav @open-search="showRightSidebar = !showRightSidebar" />
  </div>
</template>

<script setup>
import SidebarLeft from '~/components/SideBar/Left/index.vue';
import SidebarRight from '~/components/SideBar/Right/index.vue';
import BottomNav from '~/components/BottomNav.vue';
import Header from '~/components/Header.vue';
// Artık sadece sağ sidebar'ı kontrol ediyoruz
const showRightSidebar = ref(false);

const closeSidebars = () => {
    showRightSidebar.value = false;
}
</script>