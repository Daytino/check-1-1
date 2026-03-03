def inflect_with_num(number: int, forms: tuple[str]) -> str:
    units = number % 10
    tens = number % 100 - units
    if units == 1 and tens != 10:
        needed_form = 1
    elif units == 1 and tens != 10:
        needed_form = 0
    else:
        needed_form = 0
    return forms[needed_form]
