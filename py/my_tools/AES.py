from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
import binascii

def decrypt_aes_cbc(hex_ciphertext, key_hex, iv_hex):
    """
    解密AES CBC模式的密文
    
    参数:
    hex_ciphertext: 十六进制字符串形式的密文
    key_hex: 十六进制字符串形式的密钥(16/24/32字节对应AES-128/192/256)
    iv_hex: 十六进制字符串形式的初始化向量(16字节)
    
    返回:
    str: 解密后的原始文本
    """
    try:
        # 将十六进制字符串转换为字节
        ciphertext = binascii.unhexlify(hex_ciphertext)
        key = binascii.unhexlify(key_hex)
        iv = binascii.unhexlify(iv_hex)
        
        # 创建AES CBC解密器
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # 解密并去除填充
        decrypted_data = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted_data, AES.block_size)
        
        # 将字节解码为字符串
        return plaintext.decode('utf-8')
    
    except Exception as e:
        print(f"解密错误: {e}")
        return None
def aes_encrypt(plain_text, iv, key):
    """
    AES加密函数 (CBC模式)
    
    参数:
    plain_text: 要加密的字符串
    iv: 初始化向量 (16字节)
    key: 加密密钥 (16, 24, 或32字节对应AES-128, AES-192, AES-256)
    
    返回:
    加密后的数据，以base64编码的字符串形式返回
    """
    # 确保数据是bytes类型
    if isinstance(plain_text, str):
        plain_text = plain_text.encode('utf-8')
    if isinstance(iv, str):
        iv = iv.encode('utf-8')
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    # 创建AES加密器
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # 对数据进行填充并加密
    padded_data = pad(plain_text, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    
    return encrypted_data


# 使用示例
if __name__ == "__main__":
    # 示例数据 - 在实际使用中替换为真实的密文、密钥和IV
    ciphertext_hex = "f4c818c26b8fae389e70f331eb5d3ace5bb2dccb655d0434139f53df107abb41b27f5818b368b72bd27169ad338f881331acc9b80a7077afa37727a5e62187be14320c7195940b984e026b6c50eb7c1db61698b5d8d7cd9d61414d7c9fed20c8"
    key_hex = "a095f0fdfe51e6ab3bf5c777302c473e" 
    iv_hex =  "00000000000000000000000000000000"    
    
    # 解密
    result = decrypt_aes_cbc(ciphertext_hex, key_hex, iv_hex)
    if result:
        print(f"解密结果: {result}")