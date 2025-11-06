def fast_modular_exponentiation(base, exponent, modulus):
    """
    快速模指数算法计算 (base^exponent) % modulus
    
    参数:
        base: 底数(任意整数)
        exponent: 指数（正整数）
        modulus: 模数（正整数）
    
    返回:
        (base^exponent) % modulus
    """
    if modulus == 1:
        return 0
    
    result = 1
    base = base % modulus
    
    while exponent > 0:
        # 如果当前二进制位为1，将结果乘以当前base
        if exponent & 1:  # 等价于 exponent % 2 == 1
            result = (result * base) % modulus
        
        # 将base平方，指数右移一位
        base = (base * base) % modulus
        exponent = exponent >> 1  # 等价于 exponent //= 2
    
    return result

def is_prime(n):
    """
    判断一个数是否是素数
    
    参数:
        n: 要判断的整数
    
    返回:
        True 如果是素数，False 如果不是素数
    """
    # 处理特殊情况
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    # 检查所有形如 6k ± 1 的数
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    return True



if __name__ == "__main__":
    base = 7
    exp = 10001
    modulus = 10
    print(fast_modular_exponentiation(base,exp,modulus))

    test_num = 281
    print(is_prime(test_num))