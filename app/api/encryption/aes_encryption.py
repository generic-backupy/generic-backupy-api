from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def encrypt(data: str) -> bytes:
    # generate a random key
    key = get_random_bytes(32)

    # generate an initialization vector
    iv = get_random_bytes(16)

    data = bytes(data, 'utf-8')

    # create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    padded_data = pad(data, AES.block_size, style='pkcs7')
    encrypted = cipher.encrypt(padded_data)

    return encrypted, key, iv


def decrypt(encrypted: bytes, key: bytes, iv: bytes) -> str:

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    unpadded_data = unpad(decrypted, AES.block_size, style='pkcs7')
    original_data = unpadded_data.decode('utf-8')

    return original_data
