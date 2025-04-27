def get_iriski_word(count: int) -> str:
    if 11 <= (count % 100) <= 14:
        return "ирисок"
    last_digit = count % 10
    if last_digit == 1:
        return "ириска"
    elif 2 <= last_digit <= 4:
        return "ириски"
    else:
        return "ирисок"


def get_otpravleno_word(count: int) -> str:
    if count == 1:
        return "Отправлена"
    elif 2 <= (count % 10) <= 4 and not (12 <= (count % 100) <= 14):
        return "Отправлены"
    else:
        return "Отправлено"
