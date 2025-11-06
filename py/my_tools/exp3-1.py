from quick import *
import math
from collections import defaultdict
import math

def write_list_to_file(lst, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for item in lst:
            file.write(str(item) + '\n')

def count_mod_n(e,p,q):
    """
    计算满足 m^e ≡ m (mod n) 的整数 m 的数量(n = pq)
    
    参数:
        e: 指数
        n: 模数，为两个素数 p 和 q 的乘积
        
    返回:
        满足条件的 m 的数量 (0 ≤ m ≤ n-1)
    """
    # 计算模 p 和模 q 的解数
    count_p = count_mod_prime(e, p)
    count_q = count_mod_prime(e, q)
    
    # 使用中国剩余定理组合结果
    return count_p * count_q

def count_mod_prime(e, p):
    """
    计算在模素数 p 下满足 m^e ≡ m 的 m 的数量
    
    参数:
        e: 指数
        p: 素数
        
    返回:
        模 p 下的解数
    """
    if p == 1:
        return 1
    
    count = 1

    count += math.gcd(e - 1, p - 1)
    
    return count

def find_e(p,q):
    fai = (p-1)*(q-1)
    e_sum = 0
    e_dict = defaultdict(list)
    for e in range(2,fai):
        if math.gcd(e,fai) == 1:
            e_dict[count_mod_n(e,p,q)].append(e)
    e_dict_sorted = dict(sorted(e_dict.items()))
    lowest_num, e_list = next(iter(e_dict_sorted.items()))
    write_list_to_file(e_list,"exp3-1_elist.txt")
    for i in e_list:
        e_sum += i
    print(lowest_num)
    return e_sum

if __name__ == "__main__":
    p = 1009
    q = 3643
    print(f"所有满足未加密信息数最少的e和为{find_e(p,q)}")
    # test = 149
    # print(math.gcd(test,1008*3642))
    # print(count_mod_n(test,p,q))
    
