from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import base64
from Crypto.Hash import SHA256
def aes_cbc_encrypt(text, key, iv):
    """
    AES加密函数
    
    参数:
    text: 要加密的文本字符串
    key: 密钥（16, 24或32字节）
    iv: 初始化向量（16字节）
    
    返回:
    base64编码的加密字符串
    """
    # 确保文本是bytes类型
    if isinstance(text, str):
        text = text.encode('utf-8')
    
    # 确保key和iv是bytes类型
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(iv, str):
        iv = iv.encode('utf-8')
    
    # 创建AES cipher对象，使用CBC模式
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # 对文本进行填充并加密
    # AES块大小是16字节，所以需要填充到16的倍数
    encrypted_data = cipher.encrypt(pad(text, AES.block_size))
    
    # 将加密后的bytes转换为base64字符串，便于存储和传输
    encrypted_text = base64.b64encode(encrypted_data).decode('utf-8')
    
    return encrypted_text
def aes_cbc_decrypt(encrypted_text, key, iv):
    """
    AES解密函数
    
    输入是base64加密的字符串
    key和iv都可以是文本字符串


    """
    # 确保key和iv是bytes类型
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(iv, str):
        iv = iv.encode('utf-8')
    
    # 从base64解码
    encrypted_data = base64.b64decode(encrypted_text)
    
    # 创建AES cipher对象
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # 解密并去除填充
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    
    # 转换为字符串
    return decrypted_data.decode('utf-8')

def aes_ecb_encrypt(plaintext, key):
    """
    AES ECB模式加密函数
    明文 文本字符串
    密钥是 文本字符串
    返回是 base64编码的加密字符串
    """
    # 处理密钥
    key_bytes = key.encode('utf-8')
    if len(key_bytes) not in [16, 24, 32]:
        # 如果密钥长度不符合要求，使用SHA256哈希并取前32字节
        key_bytes = SHA256.new(key_bytes).digest()
    
    # 创建AES ECB加密器
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    
    # 对明文进行填充并加密
    plaintext_bytes = plaintext.encode('utf-8')
    padded_data = pad(plaintext_bytes, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    
    # 返回base64编码的加密结果
    return base64.b64encode(encrypted_data).decode('utf-8')

def aes_ecb_decrypt(ciphertext_base64, key):
    """
    AES ECB模式解密函数
    密文是 base64编码的密文字符串
    密钥是 文本字符串
    返回是 原始明文字符串
    """
    # 处理密钥
    key_bytes = key.encode('utf-8')
    if len(key_bytes) not in [16, 24, 32]:
        # 如果密钥长度不符合要求，使用SHA256哈希并取前32字节
        key_bytes = SHA256.new(key_bytes).digest()
    
    # 创建AES ECB解密器
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    
    # 解码base64并解密
    encrypted_data = base64.b64decode(ciphertext_base64)
    decrypted_data = cipher.decrypt(encrypted_data)
    
    # 去除填充并返回原始字符串
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data.decode('utf-8')

# 使用示例
if __name__ == "__main__":
    # 示例数据
    plain_text = "Hello, World! 这是一个测试文本。"
    # 密钥必须是16, 24或32字节长度
    key = "0123456789ABCDEF0123456789ABCDEF"  # 32字节
    # IV必须是16字节长度
    iv = "ABCDEFGHIJKLMNOP"  # 16字节
    
    # 加密
    encrypted = aes_cbc_encrypt(plain_text, key, iv)
    decrypted = aes_cbc_decrypt(encrypted,key,iv)
    print("加密后的文本:", encrypted)
    print("解密后的文本:", decrypted)

    encrypted = aes_ecb_encrypt(plain_text, key)
    decrypted = aes_ecb_decrypt(encrypted,key)
    print("加密后的文本:", encrypted)
    print("解密后的文本:", decrypted)