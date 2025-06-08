<template>
    <div class="mt-8 p-6 bg-gray-50 dark:bg-dim-800 rounded-lg">
        <h3 class="text-lg font-semibold dark:text-white">Your Rating</h3>

        <div 
            class="flex items-center mt-4 flex-wrap gap-x-1 gap-y-2"
            @mouseleave="handleMouseLeave"
            :class="{ 'opacity-70': isSubmitting }"
        >
            <div 
                v-for="star in 10" 
                :key="star" 
                @mouseover="hoverRating = star" 
                @click="handleStarClick(star)" 
                class="cursor-pointer"
            >
                <StarIconSolid class="w-7 h-7 transition-colors" :class="starClass(star)" />
            </div>

            <div class="ml-4">
                <span class="font-bold text-lg dark:text-white">
                    {{ displayedRating }} / 10
                </span>
                <p v-if="currentUserRating" class="text-xs text-gray-500">(Click a star to change your rating)</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { StarIcon as StarIconSolid } from '@heroicons/vue/solid';
import { useRatings } from '~/composables/useRatings';

const props = defineProps({
    movieId: { type: [String, Number], required: true },
    currentUserRating: { type: Object, default: null }
});
const emits = defineEmits(['onSuccess']);

const { addRating, updateRating } = useRatings();
const hoverRating = ref(0);
const isSubmitting = ref(false);

const displayedRating = computed(() => {
    // If hovering, show hover rating. Otherwise, show the saved rating.
    return hoverRating.value || props.currentUserRating?.user_rating || 0;
});

const starClass = (star) => {
    return star <= displayedRating.value ? 'text-yellow-400' : 'text-gray-300 dark:text-gray-600';
};

const handleMouseLeave = () => {
    hoverRating.value = 0;
};

async function handleStarClick(newRating) {
    if (isSubmitting.value) return;
    
    isSubmitting.value = true;
    try {
        // If a rating already exists, update it.
        if (props.currentUserRating) {
            await updateRating({
                movieId: props.movieId,
                rating: newRating,
                comment: props.currentUserRating.comment // Keep the old comment for now
            });
        } 
        // Otherwise, add a new one.
        else {
            await addRating({
                movieId: props.movieId,
                rating: newRating,
                comment: null
            });
        }
        emits('onSuccess'); // Refresh the page to show the definitive new state
    } catch (error) {
        console.error("Failed to submit rating:", error);
        alert('An error occurred while submitting your rating.');
    } finally {
        isSubmitting.value = false;
    }
}
</script>