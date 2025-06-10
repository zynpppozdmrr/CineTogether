// composables/useTimeAgo.js
import { formatDistanceToNowStrict, formatDistanceToNow } from 'date-fns'
import { enUS } from 'date-fns/locale'

// Kendi özel, kısa lokasyonumuzu oluşturuyoruz
const shortLocale = {
    ...enUS, // İngilizce lokasyonunun tüm özelliklerini miras al
    formatDistance: (token, count) => {
        // Token'a göre kısaltmaları belirle
        switch (token) {
            case 'xSeconds':
                return `${count}s`
            case 'xMinutes':
                return `${count}m`
            case 'xHours':
                return `${count}h`
            case 'xDays':
                return `${count}d`
            case 'xWeeks':
                return `${count}w`
            case 'xMonths':
                 return `${count}mo`
            case 'xYears':
                 return `${count}y`
            default:
                // Beklenmedik bir durum için tam metni döndür
                return formatDistanceToNow(new Date(0), { addSuffix: false, locale: enUS })
        }
    }
}

export const useTimeAgo = (date) => {
    if (!date) {
        return ''
    }
    
    // Artık formatDistanceToNowStrict ve kendi özel lokasyonumuzu kullanıyoruz
    return formatDistanceToNowStrict(new Date(date), {
        locale: shortLocale
    })
}