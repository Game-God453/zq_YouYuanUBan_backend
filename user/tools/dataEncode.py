import base64
import hashlib
from cryptography.fernet import Fernet
from django.conf import settings

# 使用 SECRET_KEY 生成一个 Fernet 密钥
def generate_fernet_key(secret_key):
    # 使用 hashlib 对 SECRET_KEY 进行哈希处理，确保密钥长度符合要求
    hashed_key = hashlib.sha256(secret_key.encode('utf-8')).digest()
    fernet_key = base64.urlsafe_b64encode(hashed_key)
    return fernet_key

# 初始化 Fernet 对象
fernet_key = generate_fernet_key(settings.SECRET_KEY)
cipher_suite = Fernet(fernet_key)

# 加密
def encrypt_id(id):
    id_bytes = str(id).encode('utf-8')
    encrypted_id = cipher_suite.encrypt(id_bytes)
    return encrypted_id.decode('utf-8')

# 解密
def decrypt_id(encrypted_id):
    encrypted_id_bytes = encrypted_id.encode('utf-8')
    decrypted_id = cipher_suite.decrypt(encrypted_id_bytes)
    return int(decrypted_id.decode('utf-8'))