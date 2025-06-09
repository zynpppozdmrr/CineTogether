<template>
  <div :class="{ 'dark': isDarkMode }">
    <div class="bg-white dark:bg-dim-900">
      <div v-if="isAuthLoading" class="min-h-screen flex items-center justify-center">
        <div class="w-60 h-60">
          <LogoCinetogether class="animate-ping" />
        </div>
      </div>
      <div v-else>
        <NuxtLayout>
          <NuxtPage />
        </NuxtLayout>
      </div>
    </div>
  </div>
</template>

<script setup>
import UISpinner from '~/components/UI/Spinner.vue';
import { useTheme } from '~/composables/useTheme.js'; // Yeni yardımcımızı import ediyoruz

const { isDarkMode } = useTheme(); // Global durumdan isDarkMode'u alıyoruz

const { useAuthLoading, initAuth } = useAuth();
const isAuthLoading = useAuthLoading();

onBeforeMount(() => {
  initAuth().catch(() => {});
});
</script>