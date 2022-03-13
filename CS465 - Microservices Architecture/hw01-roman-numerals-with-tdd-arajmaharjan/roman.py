Roman_Values = [
    ('C', 100), ('XC', 90),
    ('L', 50), ('XL', 40),
    ('X', 10), ('IX', 9),
    ('V', 5), ('IV', 4),
    ('I', 1)
] 
def int_to_roman(number):
    number = int(number)
    result = ''
    if ((number <= 0) or (number >= 110)):
        print ("Input number is not vaild integer for this program. Please input an integer 1 to 109!")
    else:
        for symbol, value in Roman_Values:
            result += (number//value) * symbol
            number = number % value
        print (result)
    return(result)