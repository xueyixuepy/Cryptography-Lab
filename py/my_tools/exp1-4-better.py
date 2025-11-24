import hashlib
import itertools
import datetime

def sha_encrypt(s):
    return hashlib.sha1(s.encode()).hexdigest()

def optimized_dfs(str2, hash1):
    """优化后的DFS函数"""
    n = len(str2)
    checked_strings = set()  # 用于记录已经检查过的字符串
    
    # 生成所有可能的字符组合
    for combo in itertools.product(*str2):
        base_string = ''.join(combo)
        
        # 如果这个组合已经检查过，跳过
        if base_string in checked_strings:
            continue
            
        # 生成所有排列并检查
        # 使用set来去除重复的排列
        for perm in set(itertools.permutations(base_string)):
            candidate = ''.join(perm)
            
            # 如果这个候选字符串已经检查过，跳过
            if candidate in checked_strings:
                continue
                
            checked_strings.add(candidate)
            
            if sha_encrypt(candidate) == hash1:
                print(f"找到密码: {candidate}")
                return True
                
    return False

starttime = datetime.datetime.now()
hash1 = "67ae1a64661ac8b4494666f58c4822408dd0a3e4"
str2 = [['Q', 'q'], ['W', 'w'], ['%', '5'], ['8', '('], 
        ['=', '0'], ['I', 'i'], ['*', '+'], ['n', 'N']]

optimized_dfs(str2, hash1)
print(f"耗时: {(datetime.datetime.now() - starttime).total_seconds():.2f}秒")

