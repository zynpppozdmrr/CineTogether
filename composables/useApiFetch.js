export const useApiFetch = (url, options = {}) => {
    const { useAuthToken } = useAuth() // Auth composable'dan token'ı alacağız

    // useFetch için varsayılan ayarlar
    const defaults = {
        baseURL: 'http://127.0.0.1:5000', // Backend adresimiz
        key: url, // İstekleri cache'lemek için benzersiz bir anahtar

        // Headers
        headers: useAuthToken().value
            ? { Authorization: `Bearer ${useAuthToken().value}` }
            : {},

        onResponse({ response }) {
            // Başarılı yanıtları logla (isteğe bağlı)
        },

        onResponseError({ response }) {
            // Hata durumunda yapılacaklar
            console.error('API Error:', response._data)
        }
    }

    return useFetch(url, { ...defaults, ...options })
}