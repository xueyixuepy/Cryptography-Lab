def decrypt_with_xor(key_stream_decimal, ciphertext_hex):
    try:
        # 将十六进制密文字符串转换为字节列表
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
        
        # 将十进制密钥流转换为字节
        key_bytes = bytes(key_stream_decimal)
        
        # 截断密文使其与密钥长度一致
        min_length = min(len(key_bytes), len(ciphertext_bytes))
        truncated_ciphertext = ciphertext_bytes[:min_length]
        truncated_key = key_bytes[:min_length]
        
        # 执行异或解密
        decrypted_bytes = []
        for i in range(min_length):
            key_byte = truncated_key[i]
            cipher_byte = truncated_ciphertext[i]
            decrypted_byte = cipher_byte ^ key_byte
            decrypted_bytes.append(decrypted_byte)
        
        # 将解密后的字节转换为字符串
        plaintext = bytes(decrypted_bytes).decode('utf-8', errors='ignore')
        
        # 将密钥转换为十六进制字符串形式
        hex_key_str = ''.join([format(k, '02x') for k in truncated_key])
        
        return {
            'plaintext': plaintext,
            'hex_key': hex_key_str,
            'truncated_ciphertext': truncated_ciphertext.hex(),
            'key_length': min_length,
            'decrypted_bytes': decrypted_bytes
        }
        
    except Exception as e:
        return {'error': f"解密过程中出现错误: {e}"}

def main():
    # 直接在代码中提供密钥和密文
    key_stream = [102, 57, 110, 137, 201, 219, 216, 204, 152, 116, 53, 42, 205, 99, 149, 16, 46, 175, 206, 120, 170, 127, 237, 40, 160, 127, 107, 201, 141, 41, 197, 11, 105, 176, 51, 154, 25, 248, 170, 64, 26, 156, 109, 112, 143, 128, 192, 102, 199, 99, 254, 240, 18, 49, 72, 205, 216, 232, 2, 208, 91, 169, 135, 119, 51, 93, 174, 252, 236, 213, 156, 67, 58, 107, 38, 139, 96, 191, 78, 240, 60, 154, 97]  # 十进制密钥
    ciphertext = "315c4eeaa8b5f8bffd11155ea506b56041c6a00c8a08854dd21a4bbde54ce56801d943ba708b8a3574f40c00fff9e00fa1439fd0654327a3bfc860b92f89ee04132ecb9298f5fd2d5e4b45e40ecc3b9d59e9417df7c95bba410e9aa2ca24c5474da2f276baa3ac325918b2daada43d6712150441c2e04f6565517f317da9d3"        # 十六进制密文
    
    print("=== 异或解密程序 ===")
    print(f"密钥（十进制）: {key_stream}")
    print(f"密文（十六进制）: {ciphertext}")
    
    # 执行解密
    result = decrypt_with_xor(key_stream, ciphertext)
    
    if 'error' in result:
        print(f"错误: {result['error']}")
        return
    
    # 显示结果
    print(f"\n=== 解密结果 ===")
    print(f"密钥长度: {result['key_length']} 字节")
    print(f"十六进制密钥: {result['hex_key']}")
    print(f"截断后的密文: {result['truncated_ciphertext']}")
    print(f"明文: {result['plaintext']}")
    
    # 显示详细的解密过程
    print(f"\n=== 详细解密过程 ===")
    key_bytes = bytes(key_stream[:result['key_length']])
    cipher_bytes = bytes.fromhex(result['truncated_ciphertext'])
    
    for i in range(result['key_length']):
        key_byte = key_bytes[i]
        cipher_byte = cipher_bytes[i]
        plain_byte = result['decrypted_bytes'][i]
        
        # 显示可打印字符或转义不可打印字符
        if 32 <= plain_byte <= 126:
            char_repr = f"'{chr(plain_byte)}'"
        else:
            char_repr = "不可打印字符"
            
        print(f"位置 {i}: 密文 {hex(cipher_byte)} XOR 密钥 {hex(key_byte)} = 明文 {hex(plain_byte)} ({char_repr})")

if __name__ == "__main__":
    main()