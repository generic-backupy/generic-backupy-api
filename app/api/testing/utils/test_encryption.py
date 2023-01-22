from api.encryption.aes_encryption import EncryptionAES
from django.test import TestCase


class TestEncryption(TestCase):

    def setUp(self):
        self.encryption_aes = EncryptionAES()
        self.test_data = "This is a test secret"
        self.test_key = self.encryption_aes.create_key()
        self.test_iv = self.encryption_aes.create_iv()

    def test_key_generation(self):
        key = self.encryption_aes.create_key()
        self.assertEqual(len(key), 32)

    def test_key_generation(self):
        key = self.encryption_aes.create_key()
        self.assertEqual(len(key), 16)

    def test_encryption_correct(self):
        encrypted = self.encryption_aes.encrypt(
            self.test_data, self.test_key, self.test_iv)
        decrypted = self.encryption_aes.decrypt(
            encrypted, self.test_key, self.test_iv)
        self.assertEqual(decrypted, self.test_data)

    def test_encrypt_with_wrong_key(self):
        encrypted = self.encryption_aes.encrypt(
            self.test_data, self.test_key, self.test_iv)
        new_key = self.encryption_aes.create_key()
        decrypted = self.encryption_aes.decrypt(
            encrypted, new_key, self.test_iv)
        self.assertNotEqual(decrypted, self.test_data)
