from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class EncryptionAES():
    def create_key(self) -> bytes:
        return get_random_bytes(32)

    def create_iv(self) -> bytes:
        return get_random_bytes(16)

    def encrypt(self, data: str, key: bytes, iv: bytes) -> bytes:
        data = bytes(data, 'utf-8')
        # create AES cipher object
        cipher = AES.new(key, AES.MODE_GCM, iv)
        padded_data = pad(data, AES.block_size, style='pkcs7')
        encrypted = cipher.encrypt(padded_data)

        return encrypted

    def decrypt(self, encrypted: bytes, key: bytes, iv: bytes) -> str:

        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted = cipher.decrypt(encrypted)
        unpadded_data = unpad(decrypted, AES.block_size, style='pkcs7')
        original_data = unpadded_data.decode('utf-8')

        return original_data