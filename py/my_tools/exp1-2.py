import string

def analyze_segment(encrypted_segment):
    """
    分析被相同密钥字节加密的密文段，找出可能的密钥字节
    """
    allowed_chars = string.ascii_letters + string.digits + ',. '
    candidate_keys = []
    
    # 测试所有可能的单字节密钥
    for potential_key in range(256):
        valid_key = True
        # 检查该密钥是否能将密文段全部解密为可见字符
        for encrypted_byte in encrypted_segment:
            decrypted_char = chr(potential_key ^ encrypted_byte)
            if decrypted_char not in allowed_chars:
                valid_key = False
                break
        if valid_key:
            candidate_keys.append(potential_key)
    
    return candidate_keys
def find_vigenere_key(ciphertext_hex, max_key_length=13):
    cipher_bytes = bytes.fromhex(ciphertext_hex)
    
    for key_size in range(1, max_key_length + 1):
        print(f"\n分析密钥长度: {key_size}")
        key_found = []
        all_positions_have_keys = True
        
        # 分析每个密钥位置
        for key_position in range(key_size):
            segment = cipher_bytes[key_position::key_size]
            possible_keys = analyze_segment(segment)
            
            if possible_keys:
                print(f"  位置 {key_position}: {len(possible_keys)} 个候选 → {[hex(k) for k in possible_keys]}")
                key_found.append(possible_keys)
            else:
                print(f"  位置 {key_position}: 无候选密钥")
                all_positions_have_keys = False
                break
        
        # 如果所有位置都有且只有一个候选密钥，我们就找到了！
        if all_positions_have_keys and all(len(keys) == 1 for keys in key_found):
            final_key = [keys[0] for keys in key_found]
            print(f"找到唯一密钥: {final_key}")
            return final_key
    
    return None
def decrypt_vigenere(ciphertext_hex, key_bytes):
    """
    使用给定的密钥解密Vigenere密文
    """
    cipher_bytes = bytes.fromhex(ciphertext_hex)
    decrypted_text = []
    key_length = len(key_bytes)
    
    for position, cipher_byte in enumerate(cipher_bytes):
        key_index = position % key_length
        decrypted_char = chr(cipher_byte ^ key_bytes[key_index])
        decrypted_text.append(decrypted_char)
    
    return ''.join(decrypted_text)
    

if __name__ == "__main__":
    # 密文字符串
    encrypted_data = "F96DE8C227A259C87EE1DA2AED57C93FE5DA36ED4EC87EF2C63AAE5B9A7EFFD673BE4ACF7BE8923CAB1ECE7AF2DA3DA44FCF7AE29235A24C963FF0DF3CA3599A70E5DA36BF1ECE77F8DC34BE129A6CF4D126BF5B9A7CFEDF3EB850D37CF0C63AA2509A76FF9227A55B9A6FE3D720A850D97AB1DD35ED5FCE6BF0D138A84CC931B1F121B44ECE70F6C032BD56C33FF9D320ED5CDF7AFF9226BE5BDE3FF7DD21ED56CF71F5C036A94D963FF8D473A351CE3FE5DA3CB84DDB71F5C17FED51DC3FE8D732BF4D963FF3C727ED4AC87EF5DB27A451D47EFD9230BF47CA6BFEC12ABE4ADF72E29224A84CDF3FF5D720A459D47AF59232A35A9A7AE7D33FB85FCE7AF5923AA31EDB3FF7D33ABF52C33FF0D673A551D93FFCD33DA35BC831B1F43CBF1EDF67F0DF23A15B963FE5DA36ED68D378F4DC36BF5B9A7AFFD121B44ECE76FEDC73BE5DD27AFCD773BA5FC93FE5DA3CB859D26BB1C63CED5CDF3FE2D730B84CDF3FF7DD21ED5ADF7CF0D636BE1EDB79E5D721ED57CE3FE6D320ED57D469F4DC27A85A963FF3C727ED49DF3FFFDD24ED55D470E69E73AC50DE3FE5DA3ABE1EDF67F4C030A44DDF3FF5D73EA250C96BE3D327A84D963FE5DA32B91ED36BB1D132A31ED87AB1D021A255DF71B1C436BF479A7AF0C13AA14794"
    
    cipher_bytes = bytes.fromhex(encrypted_data)
    
    
    
    correct_key = find_vigenere_key(encrypted_data)
    plaintext = decrypt_vigenere(encrypted_data, correct_key)
    print("\n解密结果:")
    print(plaintext)