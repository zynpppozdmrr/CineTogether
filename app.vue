<template>
  <div :class="{ 'dark': darkMode }">
    <div class="bg-white dark:bg-dim-900">

      <div v-if="isAuthLoading" class="min-h-screen flex items-center justify-center">
        <p class="text-2xl dark:text-white">Loading...</p>
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
const darkMode = ref(false) // Bunu daha sonra state'e taşıyacağız

const { useAuthLoading, initAuth, useAuthUser } = useAuth()
const isAuthLoading = useAuthLoading()
const user = useAuthUser()

// Uygulama ilk yüklendiğinde çalışır
onBeforeMount(() => {
    initAuth().catch(error => {
        // Token geçersiz veya yoksa hata verecek, bu normal.
        // Middleware bizi login sayfasına yönlendirecek.
        console.log('User not authenticated')
    })
})
</script>