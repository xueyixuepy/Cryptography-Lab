from AES_base64 import *
from normal_tools import *
#剧透
uk_str = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
#print(hex_to_text(decode_base64(uk_str)))
#预言机
def AES_128_ECB(my_string,unknown_string, random_key):
    true_str =  hex_to_text(decode_base64(unknown_string))
    aes_str = my_string + true_str
    return aes_ecb_encrypt(aes_str,random_key)

#随机密钥
random_key =    "0123456789ABCDEF"
#随机前缀
def AES_128_ECB2(my_string,unknown_string, random_key):
    random_prefix = "0123456789AB"
    true_str =  hex_to_text(decode_base64(unknown_string))
    aes_str = random_prefix + my_string + true_str
    return aes_ecb_encrypt(aes_str,random_key)
#可能字符
m_chars = bytes(range(128)).decode("ascii")
def find_block_size():
    my_string = ""
    len1 = len(decode_base64(AES_128_ECB(my_string,uk_str,random_key)))
    len2 = len(decode_base64(AES_128_ECB(my_string,uk_str,random_key))) 
    while True:
        my_string += "A"
        len1 = len(decode_base64(AES_128_ECB(my_string,uk_str,random_key)))
        if len1!= len2:
            break
        len2 =len1
    return int((len1 - len2)/2)



def test():
    a_k_str = "A"*15
    zhanwei_chars = "A"*15
    f_char = ''
    mes = "" 
    e_mse = hex_to_bytes(decode_base64(AES_128_ECB("",uk_str,random_key)))
    #print(e_mse)
    blocks_num = int(len(e_mse)/16)           
    ctr = 0                                                                                                                                                                                                                                                   
    i=0
    print(blocks_num)
    for i in range(blocks_num):
        for ctr in range(16):
            zhanwei_chars = a_k_str[:15-ctr]
            for t in m_chars:
                if hex_to_bytes(decode_base64(AES_128_ECB(a_k_str+t,uk_str,random_key)))[0:16]==hex_to_bytes(decode_base64(AES_128_ECB(zhanwei_chars,uk_str,random_key)))[i*16:16+i*16]:
                    #print(t)
                    #print(hex_to_bytes(decode_base64(AES_128_ECB(a_k_str+t,uk_str,random_key)))[0:16])
                    f_char = t
                    mes += f_char
                    break
                #print(hex_to_bytes(decode_base64(AES_128_ECB(a_k_str+t,uk_str,random_key)))[0:16])
            a_k_str = a_k_str[1:15] + f_char
            
    print(mes)

def hulue_fun(need,hulue,str):
    m_str = "A"*need
    return hex_to_bytes(decode_base64(AES_128_ECB2(m_str+str,uk_str,random_key)))[hulue*16:]

def find_repeated_blocks(hex_string, block_size=16):

    # 验证输入是否为有效的十六进制字符串
    if not all(c in '0123456789abcdefABCDEF' for c in hex_string):
        raise ValueError("输入字符串必须是有效的十六进制字符串")
    
    # 将字符串转换为大写以便比较
    hex_string = hex_string.upper()
    
    # 计算每个块在字符串中的字符数（十六进制中每个字节用2个字符表示）
    chars_per_block = block_size * 2
    
    # 检查字符串长度是否足够
    if len(hex_string) < chars_per_block * 2:
        return -1
    
    # 遍历所有可能的块位置
    for i in range(0, len(hex_string) - chars_per_block * 2 + 1, 2):
        # 提取第一个块
        block1 = hex_string[i:i + chars_per_block]
        
        # 在剩余字符串中查找相同的块
        for j in range(i + chars_per_block, len(hex_string) - chars_per_block + 1, 2):
            block2 = hex_string[j:j + chars_per_block]
            
            if block1 == block2:
                # 找到重复块，返回第一个块的起始位置
                return i
    
    return -1

def find_prefix_length(block_size):
    # A1 = "A"*block_size*2
    # print(decode_base64(AES_128_ECB(random_prefix+A1,uk_str,random_key)))
    my_string = ""
    len1 = len(decode_base64(AES_128_ECB(my_string,uk_str,random_key)))
    len2 = len(decode_base64(AES_128_ECB(my_string,uk_str,random_key))) 
    while True:
        my_string += "A"
        len1 = len(decode_base64(AES_128_ECB(my_string,uk_str,random_key)))
        if len1!= len2:
            break
        len2 =len1
    need1 = len(my_string)-1
    my_string = ""
    len1 = len(decode_base64(AES_128_ECB2(my_string,uk_str,random_key)))
    len2 = len(decode_base64(AES_128_ECB2(my_string,uk_str,random_key))) 
    while True:
        my_string += "A"
        len1 = len(decode_base64(AES_128_ECB2(my_string,uk_str,random_key)))
        if len1!= len2:
            break
        len2 =len1
    #print(f"还需要{len(my_string)-1}个字节才能对齐")
    need = len(my_string)-1 - need1
    my_string = "A"*(block_size*2+len(my_string)-1)
    hulue=int(find_repeated_blocks(decode_base64(AES_128_ECB2(my_string,uk_str,random_key)))/32)
    return (need,hulue)

def test2(tu):
    a_k_str = "A"*15
    zhanwei_chars = "A"*15
    f_char = ''
    mes = "" 
    e_mse = hulue_fun(tu[0],tu[1],"")
    #print(e_mse)
    blocks_num = int(len(e_mse)/16)           
    ctr = 0                                                                                                                                                                                                                                                   
    i=0
    print(blocks_num)
    for i in range(blocks_num):
        for ctr in range(16):
            zhanwei_chars = a_k_str[:15-ctr]
            for t in m_chars:
                if hulue_fun(tu[0],tu[1],a_k_str+t)[0:16]==hulue_fun(tu[0],tu[1],zhanwei_chars)[i*16:16+i*16]:
                    #print(t)
                    #print(hex_to_bytes(decode_base64(AES_128_ECB(a_k_str+t,uk_str,random_key)))[0:16])
                    f_char = t
                    mes += f_char
                    break
                #print(hex_to_bytes(decode_base64(AES_128_ECB(a_k_str+t,uk_str,random_key)))[0:16])
            a_k_str = a_k_str[1:15] + f_char
            
    print(mes)


#测试
if __name__ == "__main__":
    my_string = ""
    #块大小
    print(f"块大小为{find_block_size()}字节")
    #模式
    my_string = "A"*32
    #print(decode_base64(AES_128_ECB(my_string,uk_str,random_key)))
    #解密
    test()
    tu = find_prefix_length(16)
    # print(tu)
    # print(hulue_fun(tu[0],tu[1],""))
    # print(hex_to_bytes(decode_base64(AES_128_ECB("",uk_str,random_key))))
    test2(tu)