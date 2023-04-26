import os
import re

from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'



# Generate hash value from plain-text
def hash_in(plain):
    # if not plain: # Alternate: After implemention this will alter from.
    # return
    result = ""
    for s in str(plain):

        unicode = ord(s)
        quotient = unicode

        for i in range(4):
            reminder = quotient % 62
            digit = str(dec_to_62(reminder))
            result = digit + result
            quotient //= 62

    return "sxtw" + result

# Generate plain-text from hash value


def hash_out(hash):
    result = ""
    hash = str(hash)
    if hash[0: 4] == "sxtw" and len(hash) % 4 == 0:
        hash = hash[4:]
        for i in range(0, len(hash), 4):
            digit = hash[i: i + 4]
            result = chr(dec_from_62(digit)) + result
    else:
        return hash

    return result


# Convert decimal value of chr's ord to 62base digit
def dec_to_62(dec):
    # 1114111
    # try:
    # Data validation
    # assert (not dec.isdigit()), "helpers.dec_to_62: Must enter 10base digits"
    # assert (dec < 0 or dec > 61), "helpers.dec_to_62: Value must between 0 and 61"

    dec = int(dec)
    # Conversion
    if dec < 10:
        return chr(dec + 48)
    elif dec < 36:
        return chr(dec + 55)
    else:
        return chr(dec + 61)
#    except Exception as e:
#        print (e)


# Convert 62base digit to decimal value of chr's ord()
def dec_from_62(hash):
    # Assert len(hash) != 4, "Input string should be 4 characters length represents a plain digit"
    hash = str(hash)[:: -1]
    result = 0
    for i in range(0, 4):
        digit = hash[i: i + 1]
        if digit < 'A':
            result += (ord(digit) - 48) * 62 ** i
        elif digit < 'a':
            result += (ord(digit) - 55) * 62 ** i
        else:
            result += (ord(digit) - 61) * 62 ** i
    return result

