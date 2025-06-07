<template>
  <div :class="{ 'dark': darkMode }">
    <div class="bg-white dark:bg-dim-900">

      <div v-if="isAuthLoading" class="min-h-screen flex items-center justify-center">
        <UISpinner />
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
const darkMode = ref(true);

const { useAuthLoading, initAuth } = useAuth();
const isAuthLoading = useAuthLoading();

onBeforeMount(() => {
  initAuth().catch(() => {});
});
</script>