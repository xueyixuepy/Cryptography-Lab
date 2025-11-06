import random
import math
def fast_modular_exponentiation(base, exponent, modulus):
    """
    快速模指数算法
    
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


def fermat_primality_test(m, k):
    """
    费马素性检验算法
    
    参数:
    m: 待检验的奇整数 (m ≥ 3)
    k: 安全参数，决定检验的重复次数
    
    返回:
    (is_prime, probability): 是否为素数的布尔值和对应的概率
    """

    for i in range(1, k + 1):

        # 步骤1: 随机选取整数 a，2 ≤ a ≤ m-2
        a = random.randint(2, m - 2)
        
        # 步骤2: 计算 gcd(a, m)
        g = math.gcd(a, m)
        
        if g != 1:
            #print(f"第{i}轮步骤2结果:取a = {a} gcd ≠ 1，确定 {m} 为合数")
            return False, 0  # 确定是合数
        
        # 步骤3: 计算 r = a^(m-1) mod m
        r = fast_modular_exponentiation(a,m-1,m)  
        
        if r != 1:
            #print(f"第{i}轮步骤3结果:取a = {a} r ≠ 1，确定 {m} 为合数")
            return False, 0  # 确定是合数
    
    # 步骤4: 所有k轮检验都通过
    probability = 1 - (1 / (2 ** k))
    # print(f"经过 {k} 轮检验全部通过")
    # print(f"{m} 为素数的概率为: {probability:.6f} (1 - 1/2^{k})")
    
    return True, probability


if __name__ == "__main__":
    print("1.txt:")
    m = 22490786032581252653804293372291364645793557622287483794068059729599436319187521960324376683054347547395671386744086304692805374658648276530158598830663512870986923640594114549663000096751913376039100650176712055134178408046056400964911986174124229526467624088905614261746469069937028178301104012511912404648628120254278975297142512552917260023114679553
    k = 10
    result,pro = fermat_primality_test(m,k)
    print("3.txt:")
    m = 1559876147742992673125957404768949712978720573116974723188491435550196169965040848206868200084918233743662847668000971402407461887306389122707315529364807593342507936022301657320206278702095378618110195051280478534126716517153056984269659532882692418682262081495725304483536777013188527470348249542840277926802938912332306310470632601156641005608958891
    result,pro = fermat_primality_test(m,k)

