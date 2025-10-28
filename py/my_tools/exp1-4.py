import hashlib
import itertools

def crack_sha1(target_hash, charset, min_length, max_length):
    target_hash = target_hash.lower()
    
    print(f"开始破解...")
    print(f"字符集: {charset}")
    print(f"密码长度范围: {min_length}-{max_length}")
    print(f"目标哈希: {target_hash}")
    print("-" * 50)
    
    for length in range(min_length, max_length + 1):
        print(f"正在尝试长度 {length}...")
        total_combinations = len(charset) ** length
        print(f"该长度下有 {total_combinations} 种可能组合")
        
        for combination in itertools.product(charset, repeat=length):
            password = ''.join(combination)
            # 计算SHA1哈希
            hash_value = hashlib.sha1(password.encode()).hexdigest()
            
            if hash_value == target_hash:
                print(f"\n✅ 密码找到!: {password}")
                print(f"匹配哈希: {hash_value}")
                return password
    
    print("\n 在给定字符集和长度范围内未找到密码")
    return None

# 目标哈希值
target_hash = "67ae1a64661ac8b4494666f58c4822408dd0a3e4"

charset = "580qwi+n%(=QWI*N"  # 请在这里填入所有可能的字符
min_length = 1  # 请填入密码最小长度
max_length = 8  # 请填入密码最大长度


crack_sha1(target_hash, charset, min_length, max_length)
