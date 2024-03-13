# requires cryptography library
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.hazmat.primitives import padding

class EncryptUtil:
    SALT = bytes([107, 206, 171, 33, 223, 141, 140, 37, 39, 33, 33, 182, 117, 141, 20, 221, 74, 160, 252, 135])
    KEY_ITERATION_COUNT = 1024
    KEY_SIZE = 128
    KEY_ALGORITHM = 'PBKDF2HMAC'
    KEY_TRANSFORMATION = 'AES/CBC/PKCS5Padding'
    KEY_PROTOCOL = 'AES'
    CIPHER_IV = bytes([181, 16, 92, 14, 117, 74, 160, 252, 135, 38, 105, 191, 55, 24, 118, 211])

    @staticmethod
    def encrypt(key, plain_text):
        if not plain_text or plain_text.isspace():
            raise ValueError("Input text can't be empty")
        try:
            # Pad the plaintext to ensure it's a multiple of the block size
            padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(plain_text.encode('utf-8')) + padder.finalize()

            cipher = Cipher(algorithms.AES(key), modes.CBC(EncryptUtil.CIPHER_IV), backend=default_backend())
            encryptor = cipher.encryptor()
            encrypted_text = encryptor.update(padded_data) + encryptor.finalize()
            return urlsafe_b64encode(encrypted_text).decode().replace('/', '___')
        except Exception as e:
            print(f"Error while encrypting message: {plain_text}")
            raise e

    @staticmethod
    def generate_key(password, salt=None):
        if salt is None:
            salt = EncryptUtil.SALT
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA1(),
            length=EncryptUtil.KEY_SIZE // 8,
            salt=salt,
            iterations=EncryptUtil.KEY_ITERATION_COUNT,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        return key

# Example usage
if __name__ == "__main__":
    # SSO key from your account
    sso_key = "08b1721058b0490e8808b232ea4931d5"
    key = EncryptUtil.generate_key(sso_key)

    # Content Filters payload of the paramaters you want to pass in. 
    content_filters = 'contentFilters=[{"fieldName":"Company","values":["Tesla"],"operator":"="}]'
    encrypted_text = EncryptUtil.encrypt(key, content_filters)
    print(f"Encrypted text: {encrypted_text}")
