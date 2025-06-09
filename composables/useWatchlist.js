// composables/useWatchlist.js
export const useWatchlist = () => {
    const { useAuthToken } = useAuth()
    const authToken = useAuthToken()
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    const addToWatchlist = (movieId) => {
        const formData = new FormData();
        formData.append('movie_id', movieId);

        return $fetch('/api/watchlists/add', {
            method: 'POST',
            body: formData,
            baseURL: apiBase,
            headers: {
                'Authorization': `Bearer ${authToken.value}`
            }
        });
    }

    const removeFromWatchlist = (movieId) => {
        const formData = new FormData();
        formData.append('movie_id', movieId);

        return $fetch('/api/watchlists/remove', {
            method: 'POST',
            body: formData,
            baseURL: 'http://127.0.0.1:5000',
            headers: {
                'Authorization': `Bearer ${authToken.value}`
            }
        });
    }

    return {
        addToWatchlist,
        removeFromWatchlist
    }
}