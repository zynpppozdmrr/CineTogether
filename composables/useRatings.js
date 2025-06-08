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
            headers: {
                'Authorization': `Bearer ${authToken.value}`
            }
        });
    }

    return {
        addRating
    }
}