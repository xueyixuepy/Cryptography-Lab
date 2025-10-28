import base64
from itertools import combinations

theCode = """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"""  # Base64密文

#  Base64 解码
ciphertext = base64.b64decode(theCode)

def hamming_distance(bytes1, bytes2):
    """
    计算两个字节串的汉明距离（不同的位数）
    """
    if len(bytes1) != len(bytes2):
        raise ValueError("字节串长度必须相等")
    
    distance = 0
    for b1, b2 in zip(bytes1, bytes2):
        xor = b1 ^ b2
        distance += bin(xor).count('1')
    
    return distance

# 测试汉明距离函数
def test_hamming():
    s1 = b"this is a test"
    s2 = b"wokka wokka!!!"
    dist = hamming_distance(s1, s2)
    print(f"测试汉明距离: {dist} (应为 37)")
    assert dist == 37, "汉明距离计算错误"

test_hamming()

def find_keysize(ciphertext, min_size=2, max_size=40, num_blocks=4):
    """
    寻找最可能的密钥长度
    """
    best_keysize = None
    best_score = float('inf')
    
    for keysize in range(min_size, max_size + 1):
        # 取前 num_blocks 个 keysize 长度的块
        blocks = []
        for i in range(num_blocks):
            start = i * keysize
            end = start + keysize
            if end <= len(ciphertext):
                blocks.append(ciphertext[start:end])
        
        # 计算所有块对之间的平均汉明距离
        total_distance = 0
        count = 0
        
        for i, j in combinations(range(len(blocks)), 2):
            if i < j:  # 避免重复计算
                dist = hamming_distance(blocks[i], blocks[j])
                normalized_dist = dist / keysize
                total_distance += normalized_dist
                count += 1
        
        if count > 0:
            avg_distance = total_distance / count
            # print(f"KEYSIZE {keysize}: 平均归一化距离 = {avg_distance:.4f}")
            
            if avg_distance < best_score:
                best_score = avg_distance
                best_keysize = keysize
    
    return best_keysize

def single_byte_xor_decrypt(ciphertext):
    """
    对单字节XOR加密的密文进行暴力破解
    返回 (解密文本, 密钥字节, 评分)
    """
    best_score = float('-inf')
    best_plaintext = None
    best_key = None
    
    for key in range(256):
        plaintext = bytes([b ^ key for b in ciphertext])
        
        score = 0
        for byte in plaintext:
            # 给英文字母、空格、标点高分
            if 65 <= byte <= 90:  # A-Z
                score += 1
            elif 97 <= byte <= 122:  # a-z
                score += 1
            elif byte == 32:  # 空格
                score += 2
            elif byte in [44, 46, 39, 34, 58, 59, 33, 63]:  # 常见标点 , . ' " : ; ! ?
                score += 1
            elif byte < 32 or byte > 126:  # 非打印字符减分
                score -= 2
        
        if score > best_score:
            best_score = score
            best_plaintext = plaintext
            best_key = key
    
    return best_plaintext, best_key, best_score

def break_repeating_key_xor(ciphertext):
    """
    主函数：破解重复密钥XOR
    """
    keysize = find_keysize(ciphertext)
    print(f"最可能的密钥长度: {keysize}")
    
    
    # 将密文分成keysize长度的块
    blocks = []
    for i in range(0, len(ciphertext), keysize):
        block = ciphertext[i:i + keysize]
        blocks.append(block)
    
    # 转置：创建keysize个新块，每个包含原块对应位置的字节
    transposed_blocks = []
    for i in range(keysize):
        transposed_block = []
        for block in blocks:
            if i < len(block):
                transposed_block.append(block[i])
        transposed_blocks.append(bytes(transposed_block))
    
    key_bytes = []
    decrypted_blocks = []
    
    for i, block in enumerate(transposed_blocks):
        if block:  # 确保块不为空
            plaintext, key_byte, score = single_byte_xor_decrypt(block)
            key_bytes.append(key_byte)
            decrypted_blocks.append(plaintext)
            # print(f"位置 {i}: 密钥字节 = {key_byte:02x} ('{chr(key_byte) if 32 <= key_byte <= 126 else '?'}'), 评分 = {score}")
    
    # 构建完整密钥
    key = bytes(key_bytes)
    print(f"找到密钥: {key} (ASCII: {''.join(chr(b) if 32 <= b <= 126 else '?' for b in key)})")
    
    # 用找到的密钥解密整个密文
    plaintext = bytearray()
    key_length = len(key)
    
    for i, byte in enumerate(ciphertext):
        plaintext.append(byte ^ key[i % key_length])
    
    return bytes(plaintext), key

# 执行破解
if __name__ == "__main__":
    if theCode.strip():
        plaintext, key = break_repeating_key_xor(ciphertext)
        print("解密结果:")
        try:
            print(plaintext.decode('utf-8', errors='replace'))
        except:
            print(plaintext[:500])  
