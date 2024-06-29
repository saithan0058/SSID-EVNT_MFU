from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def pad(text):
    block_size = 16
    pad_size = block_size - len(text) % block_size
    return text + pad_size * chr(pad_size)

def encrypt_aes_256(text, key):
    text = pad(text)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(text.encode('utf-8'))
    return base64.b64encode(iv + ciphertext).decode('utf-8')

# Example usage
key = get_random_bytes(32)  # 256-bit key
plaintext = "flag1"
encrypted_text = encrypt_aes_256(plaintext, key)
print("Encrypted:", encrypted_text)
