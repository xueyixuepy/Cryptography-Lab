import hashlib
import itertools

def crack_sha1(target_hash, charset, min_length, max_length, phase_name):

    target_hash = target_hash.lower()
    
    print(f"\n {phase_name}")
    print(f"字符集: {charset} (共{len(charset)}个字符)")
    print(f"长度范围: {min_length}-{max_length}")
    print("-" * 40)
    
    for length in range(min_length, max_length + 1):
        total_combinations = len(charset) ** length
        print(f"尝试长度 {length}... ({total_combinations:,} 种组合)")
        
        count = 0
        for combination in itertools.product(charset, repeat=length):
            password = ''.join(combination)
            hash_value = hashlib.sha1(password.encode()).hexdigest()
            
            count += 1
            if count % 1000000 == 0:  # 每100万次显示进度
                print(f"  已尝试: {count:,} 个密码")
            
            if hash_value == target_hash:
                print(f"\n 密码找到!: {password}")
                print(f"匹配哈希: {hash_value}")
                return password
    
    print("未找到密码")
    return None

# 目标哈希值
target_hash = "67ae1a64661ac8b4494666f58c4822408dd0a3e4"

# 指纹键位
base_keys = "580qwi+n"

# 分阶段字符集
phases = [
    {
        "name": "阶段1: 纯小写字母数字",
        "charset": "580qwin",  # 去掉+号，只保留字母数字
        "min_length": 4,
        "max_length": 8
    },
    {
        "name": "阶段2: 小写+大写字母数字", 
        "charset": "580qwinQWIN",  # 添加大写字母
        "min_length": 4,
        "max_length": 8
    },
    {
        "name": "阶段3: 添加+和*符号",
        "charset": "580qwinQWIN+*",  # 添加基础符号
        "min_length": 4, 
        "max_length": 8
    },
    {
        "name": "阶段4: 添加所有Shift符号",
        "charset": "580qwi+n%(=QWI*N",  # 完整Shift字符集
        "min_length": 4,
        "max_length": 10
    },
]


# 按阶段进行破解
for phase in phases:
    password = crack_sha1(target_hash, phase["charset"], phase["min_length"], phase["max_length"], phase["name"])
    if password:
        print(f"\n 破解成功! 密码为: {password}")
        break
else:
    print("未找到密码")