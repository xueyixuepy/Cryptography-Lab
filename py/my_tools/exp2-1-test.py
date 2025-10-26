from Crypto.Cipher import AES
import base64
import hashlib
def sha1_hash(text):
    #计算sha-1的hash值，以十六进制字符串形式返回
    return hashlib.sha1(text.encode()).hexdigest()
def string_to_hex(text):
    # 将字符串编码为字节，然后转换为十六进制
    hex_string = text.encode('utf-8').hex()
    return hex_string
def aes_cbc_decrypt_zero_iv(key_hex, base64_ciphertext):
    """
    AES-CBC 解密，IV 为 16 字节零，处理 01-00 填充
    
    Args:
        key_hex: 16 字节密钥的十六进制字符串
        base64_ciphertext: Base64 编码的密文
    
    Returns:
        解密后的文本字符串
    """
    # 解码密钥
    key = bytes.fromhex(key_hex)
    
    # 解码 Base64 密文
    ciphertext = base64.b64decode(base64_ciphertext)
    
    # 检查数据长度
    if len(ciphertext) % 16 != 0:
        raise ValueError("密文长度不是 16 字节的倍数")
    
    # 创建 AES-CBC 解密器，IV 为 16 字节零
    iv = b'\x00' * 16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # 解密
    decrypted = cipher.decrypt(ciphertext)
    
    # 处理 01-00 填充
    # 查找最后一个 0x01 字节，它后面的都应该是 0x00 或者是填充开始
    pad_index = -1
    for i in range(len(decrypted) - 1, -1, -1):
        if decrypted[i] == 0x01:
            pad_index = i
            break
        elif decrypted[i] != 0x00:
            # 遇到非零非 0x01 字节，说明不是 01-00 填充
            break
    
    if pad_index != -1:
        # 验证从 pad_index 到末尾都是 0x00 或 0x01（只有第一个是 0x01）
        valid_padding = True
        for i in range(pad_index + 1, len(decrypted)):
            if decrypted[i] != 0x00:
                valid_padding = False
                break
        
        if valid_padding:
            decrypted = decrypted[:pad_index]
    
    # 尝试解码为文本
    try:
        # 先尝试 UTF-8
        return decrypted.decode('utf-8')
    except UnicodeDecodeError:
        try:
            # 尝试 Latin-1（不会失败）
            return decrypted.decode('latin-1')
        except:
            # 返回十六进制表示
            return decrypted.hex()

# 测试用例
if __name__ == "__main__":
    # 你的数据
    base64_cipher = "9MgYwmuPrjiecPMx6106zluy3MtlXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyel5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI"
    

    kenc=sha1_hash("12345678<811101821111167")[:32]
    # 根据之前计算得到的 Kenc
    #kenc = "629773ef8d2988cf37a7cbf285f28ec4"  # SHA1("12345678<111018111116") 前16字节
    #kenc = string_to_hex("7b8c92ca6b66a5e5")
    # 解密
    result = aes_cbc_decrypt_zero_iv(kenc, base64_cipher)
    print("解密结果:")
    print(result)
    
    # # 也打印原始字节以便分析
    # ciphertext = base64.b64decode(base64_cipher)
    # key = bytes.fromhex(kenc)
    # iv = b'\x00' * 16
    # cipher = AES.new(key, AES.MODE_CBC, iv)
    # raw_decrypted = cipher.decrypt(ciphertext)
    # print("\n原始解密字节:")
    # print(raw_decrypted)
    # print("十六进制:", raw_decrypted.hex())