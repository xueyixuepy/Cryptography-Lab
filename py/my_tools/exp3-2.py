import random
import math
from is_prime_test import *
def generate_primes():
    """
    生成两个随机质数
    返回: p, q
    """
    # 使用预先生成的质数列表（前100个质数）
    primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
        157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
        233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311,
        313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397,
        401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479,
        487, 491, 499, 503, 509, 521, 523, 541
    ]
    
    # 随机选择两个不同的质数
    p = random.choice(primes)
    q = random.choice(primes)
    while p == q:
        q = random.choice(primes)
    
    return p, q

def generate_primes_plus(length):
    """
    1. 生成两个随机质数(先随机生成再判断是不是素数，k取20)
    返回: p, q
    """
    p,q = random.randint(2,length),random.randint(2,length)
    is_p_prime,pro = fermat_primality_test(p,20) 
    is_q_prime,pro = fermat_primality_test(q,20) 
    while  not is_p_prime:
       p = random.randint(2,length)
       is_p_prime,pro = fermat_primality_test(p,20) 
    while  not is_q_prime:
       q = random.randint(2,length)
       is_q_prime,pro = fermat_primality_test(q,20) 

    return p, q

def mod_inverse(e, et):
    """
    2. 计算 e 在模 et 下的乘法逆元
    输入: e, et
    返回: d (e * d ≡ 1 mod et)
    """
    # 使用扩展欧几里得算法
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, y = extended_gcd(e, et)
    if gcd != 1:
        raise ValueError(f"逆元不存在，gcd({e}, {et}) = {gcd}")
    return x % et
def generate_keys_plus(m):
    """
    3. 生成RSA公钥和私钥
    返回: 公钥 (e, n), 私钥 (d, n)
    """
    # 生成两个质数
    p, q = generate_primes_plus(m)
    
    # 计算 n 和欧拉函数值
    n = p * q
    et = (p - 1) * (q - 1)
    
    # 选择公钥指数 e
    e = 3
    
    # 确保 e 和 et 互质
    while math.gcd(e, et) != 1:
        #重新生成p与q
        p, q = generate_primes()
        n = p * q
        et = (p - 1) * (q - 1)
    
    # 计算私钥指数 d
    d = mod_inverse(e, et)
    
    return (e, n), (d, n)
def generate_keys():
    """
    3. 生成RSA公钥和私钥
    返回: 公钥 (e, n), 私钥 (d, n)
    """
    # 生成两个质数
    p, q = generate_primes()
    
    # 计算 n 和欧拉函数值
    n = p * q
    et = (p - 1) * (q - 1)
    
    # 选择公钥指数 e
    e = 3
    
    # 确保 e 和 et 互质
    while math.gcd(e, et) != 1:
        #重新生成p与q
        p, q = generate_primes()
        n = p * q
        et = (p - 1) * (q - 1)
    
    # 计算私钥指数 d
    d = mod_inverse(e, et)
    
    return (e, n), (d, n)

def encrypt(public_key, m):
    """
    4. 加密函数
    输入: 公钥 (e, n), 明文整数 m
    返回: 密文整数 c
    """
    e, n = public_key
    return pow(m, e, n)

def decrypt(private_key, c):
    """
    5. 解密函数
    输入: 私钥 (d, n), 密文整数 c
    返回: 明文整数 m
    """
    d, n = private_key
    return pow(c, d, n)

def string_to_number(text):
    """
    将字符串转换为数字
    """
    # 将字符串转换为字节，然后转换为十六进制字符串
    hex_string = text.encode('utf-8').hex()
    
    # 在十六进制字符串前加上'0x'，然后转换为整数
    number = int('0x' + hex_string, 16)

    return number

def number_to_string(number):
    """
    将数字转换回字符串
    """
    # 将数字转换为十六进制字符串，去掉'0x'前缀
    hex_string = hex(number)[2:]
    
    # 将十六进制字符串转换回字节，然后解码为字符串
    text = bytes.fromhex(hex_string).decode('utf-8')
    return text

def encrypt_string(public_key,m_str):
    m_num = string_to_number(m_str)
    e, n = public_key
    if m_num >= n:
        return 0
    else:
        return encrypt(public_key,m_num)

def decrypt_string(private_key,c_num):
    m_num = decrypt(private_key,c_num)
    return number_to_string(m_num)


if __name__ == "__main__":
    public_key, private_key = generate_keys()
    e, n = public_key
    d, n_priv = private_key
    
    print(f"公钥 (e, n): ({e}, {n})")
    print(f"私钥 (d, n): ({d}, {n_priv})")

    test_num = 42

    print(f"加密{test_num}得密文{encrypt(public_key,test_num)}")
    print(f"解密{encrypt(public_key,test_num)}得明文{decrypt(private_key,encrypt(public_key,test_num))}")

    test_string = "hello_world"
    avoid_kashi = 0
    print(generate_keys_plus(string_to_number(test_string)))

    while not encrypt_string(public_key,test_string):
        public_key, private_key = generate_keys_plus(string_to_number(test_string))
        e, n = public_key
        d, n_priv = private_key
        print(f"生成密钥不合适")
        print(f"重新生成公钥({e},{n})")
        print(f"重新生成私钥({d},{n})")
        avoid_kashi += 1
        if avoid_kashi>100:
            print("长时间未找到合适密钥，停止加密")
            break
    else:
        c_str = encrypt_string(public_key,test_string)
        print(f"加密{test_string}得密文{c_str}")
        print(f"解密{c_str}得明文{decrypt_string(private_key,c_str)}")




    # public_key, private_key = generate_keys()
    # e, n = public_key
    # d, n_priv = private_key
    #print(generate_keys_plus(500))
