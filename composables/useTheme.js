// composables/useTheme.js
export const useTheme = () => {
    // 'theme' adında bir cookie oluşturuyoruz, varsayılan değeri 'light'
    const theme = useCookie('theme', { default: () => 'light' });

    // Tema 'dark' ise true dönecek bir computed
    const isDarkMode = computed(() => theme.value === 'dark');

    // Temayı değiştiren fonksiyon
    function toggleTheme() {
        theme.value = theme.value === 'light' ? 'dark' : 'light';
    }

    return {
        isDarkMode,
        toggleTheme
    };
};