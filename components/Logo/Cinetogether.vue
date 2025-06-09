<template>
    <img :src="logoSrc" alt="CineTogether Logo">
</template>

<script setup>
import { useTheme } from '~/composables/useTheme.js';

const { isDarkMode } = useTheme();

// Tema durumuna göre doğru logo URL'ini seçen computed property
const logoSrc = computed(() => {
    if (isDarkMode.value) {
        // Dark Mode için logo
        return 'https://res.cloudinary.com/dxlkdp8p9/image/upload/v1749459361/CineTogether-Logo_DarkMode_Yaz%C4%B1s%C4%B1z_jjwrrl.png';
    }
    // Light Mode için logo
    return 'https://res.cloudinary.com/dxlkdp8p9/image/upload/v1749459370/CineTogetherLogoMain_oelr1d.png';
});
</script>