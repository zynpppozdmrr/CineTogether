<template>
    <div class="mt-8 p-4 sm:p-6 bg-gray-50 dark:bg-dim-800 rounded-lg">
        <h3 class="text-lg font-semibold dark:text-white">Your Rating</h3>

        <div 
            class="flex items-center mt-4 flex-wrap gap-x-1 gap-y-2"
            @mouseleave="handleMouseLeave"
            :class="{ 'opacity-70': isSubmitting }"
        >
            <div 
                v-for="star in 10" 
                :key="star" 
                @mousemove="handleStarHover(star, $event)"
                @click="submitRating" 
                class="relative w-7 h-7"
                :class="{ 'cursor-pointer': !isSubmitting }"
            >
                <StarIconSolid class="w-7 h-7 text-gray-300 dark:text-gray-600" />
                <div class="absolute top-0 left-0 h-full overflow-hidden" :style="{ width: getStarWidth(star) }">
                    <StarIconSolid class="w-7 h-7 text-yellow-400 absolute top-0 left-0" />
                </div>
            </div>

            <div v-if="currentUserRating" class="ml-4 flex items-center space-x-4">
                <div>
                    <span class="font-bold text-lg dark:text-white">{{ displayedRating.toFixed(1) }} / 10</span>
                    <p v-if="currentUserRating" class="text-xs text-gray-500">(Click a star to change your rating)</p>
                </div>
                <button v-if="currentUserRating" @click="handleDeleteRating" :disabled="isSubmitting" class="p-2 rounded-full text-gray-400 hover:bg-red-100 hover:text-red-500 dark:hover:bg-red-500/20">
                    <TrashIcon class="w-5 h-5" />
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { StarIcon as StarIconSolid, TrashIcon } from '@heroicons/vue/solid';
import { useRatings } from '~/composables/useRatings';

const props = defineProps({
    movieId: { type: [String, Number], required: true },
    currentUserRating: { type: Object, default: null }
});
const emits = defineEmits(['onSuccess']);

const { addRating, updateRating, deleteRating } = useRatings();
const hoverRating = ref(0);
const isSubmitting = ref(false);

const displayedRating = computed(() => {
    return hoverRating.value || props.currentUserRating?.user_rating || 0;
});

// Yıldızın doluluk oranını (%0, %50, %100) hesaplayan fonksiyon
const getStarWidth = (star) => {
    const rating = displayedRating.value;
    if (star <= rating) return '100%'; // Tam yıldız
    if (star === Math.ceil(rating) && (rating % 1 !== 0)) return '50%'; // Yarım yıldız
    return '0%'; // Boş yıldız
};

// Fare yıldızların üzerindeyken buçuklu puanı hesaplar
const handleStarHover = (star, event) => {
    if (isSubmitting.value) return;
    const rect = event.currentTarget.getBoundingClientRect();
    const isHalf = event.clientX - rect.left < rect.width / 2;
    hoverRating.value = star - (isHalf ? 0.5 : 0);
};

const starClass = (star) => {
    return star <= displayedRating.value ? 'text-yellow-400' : 'text-gray-300 dark:text-gray-600';
};

const handleMouseLeave = () => { hoverRating.value = 0; };


// Bir yıldıza tıklandığında puanı ekler veya günceller
async function submitRating() {
    if (isSubmitting.value || hoverRating.value === 0) return;
    
    isSubmitting.value = true;
    try {
        const ratingData = {
            movieId: props.movieId,
            rating: hoverRating.value,
            comment: props.currentUserRating?.comment // Mevcut yorumu koru
        };

        if (props.currentUserRating) {
            await updateRating(ratingData);
        } else {
            await addRating(ratingData);
        }
        emits('onSuccess');
    } catch (error) {
        console.error("Failed to submit rating:", error);
    } finally {
        isSubmitting.value = false;
        hoverRating.value = 0; // Hover'ı sıfırla
    }
}


async function handleStarClick(newRating) {
    if (isSubmitting.value) return;
    
    isSubmitting.value = true;
    try {
        if (props.currentUserRating) {
            await updateRating({ movieId: props.movieId, rating: newRating });
        } else {
            await addRating({ movieId: props.movieId, rating: newRating, comment: null });
        }
        emits('onSuccess');
    } catch (error) {
        console.error("Failed to submit rating:", error);
    } finally {
        isSubmitting.value = false;
    }
}

// ================== GÜNCELLENMİŞ SİLME FONKSİYONU ==================
async function handleDeleteRating() {
    if (isSubmitting.value || !props.currentUserRating) return;

    // Onay penceresi (confirm) kaldırıldı.
    isSubmitting.value = true;
    try {
        await deleteRating(props.movieId);
        emits('onSuccess'); // Sayfayı yenilemek için sinyal gönder
    } catch (error) {
        console.error("Failed to delete rating:", error);
        alert('An error occurred while deleting your rating.');
    } finally {
        isSubmitting.value = false;
    }
}
// ================================================================
</script>