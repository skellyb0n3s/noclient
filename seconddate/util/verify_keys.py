
import nacl.secret
import nacl.utils
from base64 import urlsafe_b64encode, urlsafe_b64decode

# Replace with your hardcoded private key as an uppercase hex string
PRIVATE_KEY_HEX = "2CBC48C54E52ABE63E198DE7DBB358838B3C5CF08C4A32D6D620F00A6ED6ED05"
# Replace with your hardcoded public key as an uppercase hex string
PUBLIC_KEY_HEX = "18D354DF47EB8EBEE1EF98751C7CF3C48301094DCE3AA548B2D0F2B2D0BE5B6A"

# Replace with your hardcoded private key as an uppercase hex string
#PRIVATE_KEY_HEX = "39CA7E13B8CAB401146F1DA3B0DAE7D207E4069B28B35F38D13926ABB41D91ED"
# Replace with your hardcoded public key as an uppercase hex string
#PUBLIC_KEY_HEX = "02B644817C8BD9B8EFB2E59A1967FB0EB02AC6828571644ED7A246D4EAD03E36"



def generate_key():
    return bytes.fromhex(PRIVATE_KEY_HEX)

def encrypt(key, plaintext):
    box = nacl.secret.SecretBox(key)
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    ciphertext = box.encrypt(plaintext.encode(), nonce)
    return ciphertext

def decrypt(key, ciphertext):
    box = nacl.secret.SecretBox(key)
    decrypted = box.decrypt(ciphertext)
    return decrypted.decode()

if __name__ == "__main__":
    # Generate the key from the hardcoded private key
    key = generate_key()

    plaintext = "verify this text yo"

    # Encrypt the plaintext
    encrypted_data = encrypt(key, plaintext)

    print("Encrypted Data:")
    print(urlsafe_b64encode(encrypted_data).decode())

    # Decrypt the ciphertext
    decrypted_text = decrypt(key, encrypted_data)
    print("\nDecrypted Message:")
    print(decrypted_text)
