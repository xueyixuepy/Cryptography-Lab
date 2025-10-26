from hashlib import sha1
import codecs
import base64
from Crypto.Cipher import AES
import binascii
 

def Unknown_Number() -> int:
    Unknown_Number = 0
    number = "111116" 
    weight = "731"  
    for i in range(0, len(number)):
        Unknown_Number += int(number[i]) * int(weight[i % 3])
    return Unknown_Number % 10  
 
# 计算k_seed
def cal_Kseed() -> str:
    MRZ_information = "12345678<811101821111167"  # 护照信息
    H_information = sha1(MRZ_information.encode()).hexdigest()  # 使用SHA1进行哈希
    K_seed = H_information[0:32]  # 取哈希值的前32位作为K_seed
    #print(f"K_seed={K_seed}")
    return K_seed
 
def cal_Ka_Kb(K_seed):
    c = "00000001"
    d = K_seed + c
    H_d = sha1(codecs.decode(d, "hex")).hexdigest()  # 对K_seed进行哈希
    ka = H_d[0:16]  # 取前16位作为ka
    kb = H_d[16:32]  # 取后16位作为kb
    return ka, kb
 
def Parity_Check(x):
    k_list = []
    a = bin(int(x, 16))[2:]  
    for i in range(0, len(a), 8):
 
        if (a[i:i + 7].count("1")) % 2 == 0:
            k_list.append(a[i:i + 7])
            k_list.append('1')
        else:
            k_list.append(a[i:i + 7])
            k_list.append('0')
    k = hex(int(''.join(k_list), 2))  # 将2进制转为16进制
    return k
 
if __name__ == "__main__":
    K_seed = cal_Kseed()  # 计算K_seed
    ka, kb = cal_Ka_Kb(K_seed)  
    k_1 = Parity_Check(ka) 
    k_2 = Parity_Check(kb)  
    key = k_1[2:] + k_2[2:]  
    print(f"key={key}")  # 输出密钥
 
    # 待解密的密文
    ciphertext = base64.b64decode(
        "9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI")
    IV = '0' * 32 
 
    # 使用AES进行解密
    m = AES.new(binascii.unhexlify(key), AES.MODE_CBC, binascii.unhexlify(IV)).decrypt(ciphertext)
    print(f"明文：{m}")  