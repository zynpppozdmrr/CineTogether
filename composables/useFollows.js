export const useFollows = () => {
    const { useAuthToken } = useAuth()
    const authToken = useAuthToken()
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    const makeFollowRequest = (endpoint, followeeId) => {
        const formData = new FormData();
        formData.append('followee_id', followeeId); // Backend'in beklediği anahtar: 'followee_id'

        return $fetch(endpoint, {
            method: 'POST',
            body: formData,
            baseURL: apiBase,
            headers: {
                'Authorization': `Bearer ${authToken.value}`
            }
        });
    }

    const followUser = (followeeId) => {
        return makeFollowRequest('/api/follows/follow', followeeId);
    }

    const unfollowUser = (followeeId) => {
        return makeFollowRequest('/api/follows/unfollow', followeeId);
    }

    return {
        followUser,
        unfollowUser
    }
}