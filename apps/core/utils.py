def correct_latin_number(number: str):
    len_before = len(number)
    number = str(int(number))  # raises ValueError if value has alphabets
    return "0" * (len_before - len(number)) + number
