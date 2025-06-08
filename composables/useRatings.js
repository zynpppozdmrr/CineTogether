// composables/useRatings.js
export const useRatings = () => {
    const { useAuthToken } = useAuth()
    const authToken = useAuthToken()

    const addRating = ({ movieId, rating, comment }) => {
        const formData = new FormData();
        formData.append('movie_id', movieId);
        formData.append('rating', rating);
        if (comment) {
            formData.append('comment', comment);
        }
        return $fetch('/api/ratings/', {
            method: 'POST',
            body: formData,
            baseURL: 'http://127.0.0.1:5000',
            headers: { 'Authorization': `Bearer ${authToken.value}` }
        });
    }

    // ================ YENİ FONKSİYONLAR ================
    const updateRating = ({ movieId, rating, comment }) => {
        const formData = new FormData();
        formData.append('movie_id', movieId);
        if (rating) {
            formData.append('rating', rating);
        }
        if (comment) {
            formData.append('comment', comment);
        }
        return $fetch('/api/ratings/update', {
            method: 'PUT',
            body: formData,
            baseURL: 'http://127.0.0.1:5000',
            headers: { 'Authorization': `Bearer ${authToken.value}` }
        });
    }

    const deleteRating = (movieId) => {
        const formData = new FormData();
        formData.append('movie_id', movieId);
        return $fetch('/api/ratings/delete', {
            method: 'DELETE',
            body: formData,
            baseURL: 'http://127.0.0.1:5000',
            headers: { 'Authorization': `Bearer ${authToken.value}` }
        });
    }
    // =======================================================

    return {
        addRating,
        updateRating,
        deleteRating
    }
}