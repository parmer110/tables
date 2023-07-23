from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os
import re
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

# Generate hash value from plain-text
def sxtw_encoder(plain):
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


def sxtw_decoder(hash):
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


def generate_encryption_key():
    # تولید کلید امنیتی به عنوان یک رشته تصادفی با طول 32 بایت (256 بیت)
    return os.urandom(32)

def aes_encoder(input_string):
    backend = default_backend()
    padder = padding.PKCS7(128).padder()
    unpadder = padding.PKCS7(128).unpadder()

    # تولید کلید امنیتی تصادفی
    encryption_key = generate_encryption_key()

    # Convert the input string to bytes
    data = input_string.encode('utf-8')

    # Create an AES cipher object with GCM mode
    iv = os.urandom(16)  # Generate a random initialization vector (IV)
    cipher = Cipher(algorithms.AES(encryption_key), modes.GCM(iv), backend=backend)

    # Encrypt the data
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()

    # Return the IV, the ciphertext, the encryption key, and the authentication tag
    encoded_iv = base64.b85encode(iv).decode()
    encoded_ciphertext = base64.b85encode(ciphertext).decode()
    encoded_key = base64.b85encode(encryption_key).decode()
    auth_tag = base64.b85encode(encryptor.tag).decode()

    return f"{encoded_iv}:{encoded_ciphertext}:{encoded_key}:{auth_tag}"

def aes_decoder(encoded_string):
    backend = default_backend()
    padder = padding.PKCS7(128).padder()
    unpadder = padding.PKCS7(128).unpadder()

    # Extract the IV, ciphertext, encryption key, and authentication tag from the encoded string
    encoded_iv, encoded_ciphertext, encoded_key, auth_tag = encoded_string.split(':')
    iv = base64.b85decode(encoded_iv)
    ciphertext = base64.b85decode(encoded_ciphertext)
    encryption_key = base64.b85decode(encoded_key)
    auth_tag = base64.b85decode(auth_tag)

    # Create an AES cipher object with GCM mode
    cipher = Cipher(algorithms.AES(encryption_key), modes.GCM(iv, auth_tag), backend=backend)

    # Decrypt the data
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Return the decrypted data as a string
    return decrypted_data.decode('utf-8')



def encoder(value):
    if isinstance(value, date):
        value = value.isoformat()
    elif isinstance(value, datetime):
        value = value.isoformat()
    elif isinstance(value, Decimal):
        value = str(value)
    elif isinstance(value, int):
        value = str(value)
    elif isinstance(value, bool):
        value = str(value)
    elif isinstance(value, bytes):
        value = value.hex()
    elif isinstance(value, UUID):
        value = str(value)
    elif isinstance(value, float):
        value = repr(value)

    return sxtw_encoder(aes_encoder(value))

def decoder(str):
    if str is not None and str[0: 4] == "sxtw" and len(str) % 4 == 0:
        value =  aes_decoder(sxtw_decoder(str))
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            try:
                value = date.fromisoformat(value)
            except ValueError:
                try:
                    value = Decimal(value)
                except InvalidOperation:
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            if value.lower() == 'true':
                                value = True
                            elif value.lower() == 'false':
                                value = False
                            else:
                                raise ValueError
                        except ValueError:
                            try:
                                value = bytes.fromhex(value)
                            except ValueError:
                                try:
                                    value = UUID(value)
                                except ValueError:
                                    try:
                                        value = float(value)
                                    except ValueError:
                                        pass

        return value
    else:
        return str
