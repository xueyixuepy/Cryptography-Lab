import hashlib

def derive_k_enc(seed_hex):
    """
    从32位十六进制密钥种子派生K(ENC)
    
    参数:
    seed_hex (str): 32位十六进制字符串的密钥种子
    
    返回:
    str: K(ENC)密钥的十六进制字符串
    """
    # 验证输入是否为32位十六进制
    if len(seed_hex) != 32:
        raise ValueError("密钥种子必须是32位十六进制字符串")
    
    # 将十六进制种子转换为字节
    seed_bytes = bytes.fromhex(seed_hex)
    
    # 第一次哈希：SHA-1(seed || 0x00)
    data1 = seed_bytes + b'\x00'
    hash1 = hashlib.sha1(data1).digest()
    
    # 第二次哈希：SHA-1(seed || 0x01)  
    data2 = seed_bytes + b'\x01'
    hash2 = hashlib.sha1(data2).digest()
    
    # 第三次哈希：SHA-1(seed || 0x02)
    data3 = seed_bytes + b'\x02'
    hash3 = hashlib.sha1(data3).digest()
    
    # 取每个哈希的前16字节，连接形成K(ENC)
    k_enc = hash1[:16] + hash2[:16] + hash3[:16]
    
    return k_enc.hex()

# 使用示例
if __name__ == "__main__":
    # 示例密钥种子
    seed = "a095f0fdfe51e6ab3bf5c777302c473e"
    
    try:
        k_enc = derive_k_enc(seed)
        print(f"密钥种子: {seed}")
        print(f"K(ENC):   {k_enc}")
        print(f"K(ENC)长度: {len(k_enc)//2} 字节")
    except ValueError as e:
        print(f"错误: {e}")