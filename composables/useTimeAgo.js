// composables/useTimeAgo.js
import { formatDistanceToNow } from 'date-fns'
import { enUS } from 'date-fns/locale' // Türkçe (tr) yerine İngilizce (ABD) dil paketini import ediyoruz

export const useTimeAgo = (date) => {
    if (!date) {
        return ''
    }
    // locale seçeneğini 'enUS' olarak güncelliyoruz
    return formatDistanceToNow(new Date(date), { addSuffix: true, locale: enUS })
}