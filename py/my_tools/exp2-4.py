from AES_base64 import *
from normal_tools import *
#随机密钥
random_key = "0123456789ABCDEF"
iv = "789ABCDEF0123456"
def efun(user_data):
    qian = "comment1=cooking%20MCs;userdata="
    hou = ";comment2=%20like%20a%20pound%20of%20bacon"
    user_data = user_data.replace(";", "%3B").replace("=", "%3D")
    link_str = qian+user_data+hou
    return aes_cbc_encrypt(link_str,random_key,iv)

def dfun(miwen):
    return aes_cbc_decrypt(miwen,random_key,iv)

    

def cbc_attack():
    a_input = "?admin?true?aaaa"
    e = hex_to_bytes(decode_base64(efun(a_input)))
    e = bytearray(e)
    e[16] ^= 0x04  
    e[22] ^= 0x02
    e[27] ^= 0x04
    e = bytes(e)  
    changed_e = encode_base64(bytes_to_hex_string(e))
    
    # 手动解密检查字节
    import base64
    from Crypto.Cipher import AES
    cipher_bytes = base64.b64decode(changed_e)
    cipher = AES.new(random_key.encode(), AES.MODE_CBC, iv.encode())
    decrypted = cipher.decrypt(cipher_bytes)
    
    # 检查字节中是否包含目标
    target_bytes = b";admin=true;"
    success = target_bytes in decrypted
    
    print("解密结果:", decrypted)
    print(success)
    return success
    

if __name__ == "__main__":
    e = efun(";admin=true;")
    d = dfun(e)
    print(e)
    print(d)
    cbc_attack()
