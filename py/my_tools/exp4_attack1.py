from exp4_try1 import get_nec
from normal_tools import extended_gcd,hex_to_int,int_to_hex,hex_to_text,CRT,gcd,string_to_hex
import gmpy2
import math
import time
def factor_collision_attack(n_list, e_list, c_list):
    """
    使用因数碰撞法攻击RSA
    
    参数:
    n_list: RSA模数列表
    e_list: 公钥指数列表  
    c_list: 密文列表

    返回:
    解密结果列表，每个元素为明文或None
    """
    results = []
    
    # 第一步：寻找共享质因数的模数
    factor_dict = {}  # 存储已找到的因子
    
    for i in range(len(n_list)):
        for j in range(i + 1, len(n_list)):
            # 计算两个模数的GCD
            common_factor = gcd(n_list[i], n_list[j])
            
            # 如果找到共享质因数
            if common_factor > 1 and common_factor < n_list[i] and common_factor < n_list[j]:
                # 记录第一个模数的分解
                if i not in factor_dict:
                    p = common_factor
                    q = n_list[i] // p
                    factor_dict[i] = (p, q)
                
                # 记录第二个模数的分解
                if j not in factor_dict:
                    p = common_factor
                    q = n_list[j] // p
                    factor_dict[j] = (p, q)
    
    for i in range(len(n_list)):
        if i in factor_dict:
            # 有共享因数，可以解密
            p, q = factor_dict[i]
            n = n_list[i]
            e = e_list[i]
            c = c_list[i]
            
            # 计算私钥
            phi = (p - 1) * (q - 1)
            
            # 计算模逆元
            try:
                d = pow(e, -1, phi)  
                # 解密
                m = pow(c, d, n)
                results.append(m)
            except:
                results.append(None)
        else:
            # 没有找到共享因数
            results.append(None)
    
    return results
def _pollard_p1_core(n, a, B, start_time, timeout):
    """Pollard p-1核心算法实现"""
    # 初始检查
    g = math.gcd(a, n)
    if 1 < g < n:
        return g
    
    # 主循环
    for i in range(2, B + 1):
        # 定期检查超时
        if i % 100 == 0 and time.time() - start_time > timeout:
            return None
            
        # 计算 a^i mod n
        a = pow(a, i, n)
        
        # 定期检查gcd
        if i % 1000 == 0:
            g = math.gcd(a - 1, n)
            if 1 < g < n:
                return g
    
    # 最终检查
    g = math.gcd(a - 1, n)
    if 1 < g < n:
        return g
    
    return None
def pollard_p1_with_timeout(n, timeout=4):
    """
    Pollard p-1分解法，带有超时控制
    
    参数:
    n: 要分解的大整数
    timeout: 超时时间（秒），默认3秒
    
    返回:
    如果找到非平凡因子则返回因子，超时返回None
    """
    start_time = time.time()
    
    # 基本检查
    if n <= 3:
        return None
    if n % 2 == 0:
        return 2
    
    # 检查小质数因子
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    for p in small_primes:
        if n % p == 0:
            return p
    
    # 尝试不同的基值和边界
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    boundaries = [1000, 5000, 10000, 50000, 100000]
    
    for base in bases:
        for B in boundaries:
            # 检查是否超时
            if time.time() - start_time > timeout:
                return None
                
            factor = _pollard_p1_core(n, base, B, start_time, timeout)
            if factor and 1 < factor < n:
                return factor
    
    return None
def fermat_factorization(n):
    """
    使用费马分解法分解大整数
    
    参数:
    n: 要分解的大整数
    
    返回:
    (p, q): 如果成功分解，返回两个因子
    None: 如果n是质数或无法用此法分解
    """
    
    # 检查n是否为偶数
    if n % 2 == 0:
        return 2, n // 2
    
    # 检查n是否为完全平方数
    root = math.isqrt(n)
    if root * root == n:
        return root, root
    
    # 费马分解法主循环
    x = math.isqrt(n) + 1
    max_iterations = 1000000  # 防止无限循环
    
    for i in range(max_iterations):
        x_squared = x * x
        y_squared = x_squared - n
        
        # 检查y_squared是否为完全平方数
        y = math.isqrt(y_squared)
        if y * y == y_squared:
            # 找到因子
            p = x + y
            q = x - y
            
            # 验证结果
            if p * q == n:
                return p, q
        
        x += 1
    
    return None  # 未能在迭代限制内分解
def pp1(n):
    B=2**20
    a=2
    for i in range(2,B+1):
        a=pow(a,i,n)
        d=gmpy2.gcd(a-1,n)
        if (d>=2)and(d<=(n-1)):
            q=n//d
            n=q*d
    return d
def attack_04():
    ns, es, cs = get_nec()
    e0 = hex_to_int(es[0])
    e4 = hex_to_int(es[4])
    g, x, y = extended_gcd(e0, e4)
    
    if g != 1:
        raise ValueError(f"e0 和 e4 的最大公约数不为 1: {g}")
    
    n = hex_to_int(ns[0])
    c0 = hex_to_int(cs[0])
    c4 = hex_to_int(cs[4])
    
    # 处理负指数
    if x < 0:
        c0 = pow(c0, -1, n)  
        x = -x
    else:
        c0 = pow(c0, 1, n)  # 确保在模 n 下
    
    if y < 0:
        c4 = pow(c4, -1, n) 
        y = -y
    else:
        c4 = pow(c4, 1, n)  # 确保在模 n 下
    
    # 计算明文
    m_int = (pow(c0, x, n) * pow(c4, y, n)) % n
    
    print("Frame0,4:",hex_to_text(int_to_hex(m_int)[-16:]))



def attack_71115():
    ns, es, cs = get_nec()
    session_data = [
        {"cipher": int(cs[7], 16), "modulus": int(ns[7], 16)},
        {"cipher": int(cs[11], 16), "modulus": int(ns[11], 16)},
        {"cipher": int(cs[15], 16), "modulus": int(ns[15], 16)}
    ]
    
    congruence_list = []
    for entry in session_data:
        congruence_list.append((entry['cipher'], entry['modulus']))
    
    crt_result, total_modulus = CRT(congruence_list)
    
    # 直接开三次方根
    plaintext_result = gmpy2.iroot(gmpy2.mpz(crt_result), 3)
    print("Frame7,11,15:",hex_to_text(int_to_hex(plaintext_result[0])[-16:]))

def attack_38121620():
    ns, es, cs = get_nec()
    session_data = [
        {"cipher": int(cs[3], 16), "modulus": int(ns[3], 16)},
        {"cipher": int(cs[8], 16), "modulus": int(ns[8], 16)},
        {"cipher": int(cs[12], 16), "modulus": int(ns[12], 16)},
        {"cipher": int(cs[16], 16), "modulus": int(ns[16], 16)},
        {"cipher": int(cs[20], 16), "modulus": int(ns[20], 16)}
    ]
    
    congruence_list = []
    for entry in session_data:
        congruence_list.append((entry['cipher'], entry['modulus']))
    
    crt_result, total_modulus = CRT(congruence_list)
    
    # 直接开五次方根
    plaintext_result = gmpy2.iroot(gmpy2.mpz(crt_result), 5)
    print("Frame3,8,12,16,20:",hex_to_text(int_to_hex(plaintext_result[0])[-16:]))

def try_find_pq():
    ns, es, cs = get_nec()
    for i in range(len(ns)):
        if fermat_factorization(hex_to_int(ns[i])) != None:
            p,q = fermat_factorization(hex_to_int(ns[i]))
            print(f"Frame{i}的n可以分解为{p,q}")

def attack_10():
    p = 9686924917554805418937638872796017160525664579857640590160320300805115443578184985934338583303180178582009591634321755204008394655858254980766008932978699
    q = 9686924917554805418937638872796017160525664579857640590160320300805115443578184985934338583303180178582009591634321755204008394655858254980766008932978633
    ns, es, cs = get_nec()
    n = hex_to_int(ns[10])
    c = hex_to_int(cs[10])
    e = hex_to_int(es[10])
    phi_of_frame10 = (p-1)*(q-1)
    d = gmpy2.invert(e, phi_of_frame10)
    m = gmpy2.powmod(c, d, n)
    print("Frame10:",hex_to_text(int_to_hex(m)[-16:]))

def attack_by_pq(p,i):
    ns, es, cs = get_nec()
    n = hex_to_int(ns[i])
    c = hex_to_int(cs[i])
    e = hex_to_int(es[i])
    q = n//p
    phi_of_frame10 = (p-1)*(q-1)
    d = gmpy2.invert(e, phi_of_frame10)
    m = gmpy2.powmod(c, d, n)
    return hex_to_text(int_to_hex(m)[-16:])
def attack_2619():
    p2 = 1719620105458406433483340568317543019584575635895742560438771105058321655238562613083979651479555788009994557822024565226932906295208262756822275663694111
    p6 =  920724637201
    p19 = 1085663496559
    print("Frame2:",attack_by_pq(p2,2))
    print("Frame6:",attack_by_pq(p6,6))
    print("Frame19:",attack_by_pq(p19,19))


def pp1(n):
    B=2**20
    a=2
    start_time = time.time()
    for i in range(2,B+1):
        if  time.time() - start_time > 5:
            start_time = time.time()
            continue
            #return None
        a=pow(a,i,n)
        d=gmpy2.gcd(a-1,n)
        if (d>=2)and(d<=(n-1)):
            q=n//d
            n=q*d
    return d
def try_find_pq_2():
    ns, es, cs = get_nec()
    for i in range(len(ns)):
        if pollard_p1_with_timeout(hex_to_int(ns[i])) != None:
            d = pollard_p1_with_timeout(hex_to_int(ns[i]))
            print(f"Frame{i}的n有因子{d}")


def attack_118():
    ns, es, cs = get_nec()
    n_list = [hex_to_int(ns[1]),hex_to_int(ns[18])]
    e_list = [hex_to_int(es[1]),hex_to_int(es[18])]
    c_list = [hex_to_int(cs[1]),hex_to_int(cs[18])]

    re = factor_collision_attack(n_list,e_list,c_list)
    print("Frame1:",hex_to_text(int_to_hex(re[0])[-16:]))
    print("Frame18:",hex_to_text(int_to_hex(re[1])[-16:]))

def find_c_from_m(m):
    ns, es, cs = get_nec()
    for i in range(len(ns)):
        if pow(hex_to_int(string_to_hex(m)),hex_to_int(es[i]),hex_to_int(ns[i])) == hex_to_int(cs[i]):
            print(f"Frame{i}:{m}")


if __name__ == "__main__":
    attack_04()
    attack_71115()
    attack_38121620()
    #try_find_pq()
    attack_10()
    #try_find_pq_2()
    attack_2619()
    attack_118()
    find_c_from_m(" you fro")