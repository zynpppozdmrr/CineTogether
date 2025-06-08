<template>
    <div class="mt-8 p-6 bg-gray-50 dark:bg-dim-800 rounded-lg">
        <h3 class="text-lg font-semibold dark:text-white">Your Rating</h3>

        <div 
            class="flex items-center mt-4" 
            @mouseleave="handleMouseLeave"
            :class="{ 'pointer-events-none opacity-70': isSubmitting || currentUserRating }"
        >
            <div 
                v-for="star in 10" 
                :key="star" 
                @mousemove="handleStarHover(star, $event)"
                @click="submitRating" 
                class="relative cursor-pointer w-7 h-7"
            >
                <StarIconSolid class="w-7 h-7 text-gray-300 dark:text-gray-600" />
                <div class="absolute top-0 left-0 h-full overflow-hidden" :style="{ width: getStarWidth(star) }">
                    <StarIconSolid class="w-7 h-7 text-yellow-400 absolute top-0 left-0" />
                </div>
            </div>

            <div class="ml-4">
                <span class="font-bold text-lg dark:text-white">
                    {{ displayedRating }} / 10
                </span>
                <p v-if="currentUserRating" class="text-xs text-gray-500">(You have already rated)</p>
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

const { addRating } = useRatings();

// Reaktif değişkenler
const hoverRating = ref(0);
const finalRating = ref(props.currentUserRating?.user_rating || 0);
const isSubmitting = ref(false);

// Ekranda gösterilecek puanı hesaplayan computed property
const displayedRating = computed(() => hoverRating.value || finalRating.value);

// Bir yıldızın ne kadarının sarı olacağını hesaplar (% olarak)
const getStarWidth = (star) => {
    const rating = displayedRating.value;
    if (star <= rating) {
        return '100%'; // Tam yıldız
    }
    if (star === Math.ceil(rating) && rating % 1 !== 0) {
        return '50%'; // Yarım yıldız
    }
    return '0%'; // Boş yıldız
};

// Fare yıldızların üzerindeyken hover puanını hesaplar
const handleStarHover = (star, event) => {
    if (props.currentUserRating) return;
    const rect = event.currentTarget.getBoundingClientRect();
    const isHalf = event.clientX - rect.left < rect.width / 2;
    hoverRating.value = star - (isHalf ? 0.5 : 0);
};

// Fare yıldızların üzerinden çekildiğinde hover'ı sıfırlar
const handleMouseLeave = () => {
    hoverRating.value = 0;
};

// Bir yıldıza tıklandığında puanı gönderir
async function submitRating() {
    if (isSubmitting.value || props.currentUserRating || hoverRating.value === 0) return;
    
    isSubmitting.value = true;
    finalRating.value = hoverRating.value; // Seçilen puanı kalıcı yap

    try {
        await addRating({
            movieId: props.movieId,
            rating: finalRating.value,
            comment: null
        });
        emits('onSuccess');
    } catch (error) {
        console.error("Failed to submit rating:", error);
        alert('An error occurred. You may have already rated this movie.');
        finalRating.value = 0; // Hata durumunda puanı sıfırla
    } finally {
        isSubmitting.value = false;
    }
}
</script>