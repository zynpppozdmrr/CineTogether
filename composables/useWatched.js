// composables/useWatched.js
export const useWatched = () => {
    const { useAuthToken } = useAuth()
    const authToken = useAuthToken()
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    const markAsWatched = (movieId) => {
        const formData = new FormData();
        formData.append('movie_id', movieId);

        return $fetch('/api/watched/add', {
            method: 'POST',
            body: formData,
            baseURL: apiBase,
            headers: { 'Authorization': `Bearer ${authToken.value}` }
        });
    }

    const removeFromWatched = (movieId) => {
        const formData = new FormData();
        formData.append('movie_id', movieId);

        return $fetch('/api/watched/remove', {
            method: 'POST',
            body: formData,
            baseURL: apiBase,
            headers: { 'Authorization': `Bearer ${authToken.value}` }
        });
    }

    return {
        markAsWatched,
        removeFromWatched
    }
}