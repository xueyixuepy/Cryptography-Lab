import hashlib
import base64
def gcd(a, b):
    """计算最大公约数"""
    while b:
        a, b = b, a % b
    return a
def extended_gcd(a, b):
    """
    扩展欧几里得算法
    返回 (g, x, y) 使得 a*x + b*y = g = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1
    
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return g, x, y
def hex_to_int(hex_str):
    """十六进制转十进制"""
    return int(hex_str,16)
def int_to_hex(int_num):
    """十进制转十六进制"""
    return hex(int_num)
def hex_to_text(hex_string):

    #将十六进制字符串转换为文本

    # 移除可能存在的空格
    hex_string = hex_string.replace(' ', '')
    
    try:
        # 将十六进制字符串转换为字节，然后解码为文本
        bytes_obj = bytes.fromhex(hex_string)
        text = bytes_obj.decode('utf-8')
        return text
    except ValueError as e:
        print(f"转换错误: {e}")
        return None
def hex_to_ascii(hex_string):
    """
    将十六进制字符串转换为ASCII字符串
    str: 转换后的ASCII字符串
    """
    # 移除字符串中的空格
    hex_string = hex_string.replace(' ', '')
    
    # 检查字符串长度是否为偶数
    if len(hex_string) % 2 != 0:
        raise ValueError("十六进制字符串长度必须为偶数")
    
    try:
        # 将十六进制字符串转换为字节对象，然后解码为ASCII
        ascii_string = bytes.fromhex(hex_string).decode('ascii')
        return ascii_string
    except ValueError as e:
        raise ValueError(f"无效的十六进制字符串或无法转换为ASCII: {e}")

def hex_to_bytes(hex_string):
    """
    将十六进制字符串转换为字节类型
    """
    try:
        # 移除可能存在的空格或前缀
        hex_string = hex_string.strip().replace(' ', '').replace('0x', '')
        
        # 确保十六进制字符串长度为偶数
        if len(hex_string) % 2 != 0:
            hex_string = '0' + hex_string
        
        # 转换为字节
        byte_data = bytes.fromhex(hex_string)
        return byte_data
    except ValueError as e:
        print(f"转换错误: {e}")
        return None

def string_to_hex(text):
    # 将字符串编码为字节，然后转换为十六进制
    hex_string = text.encode('utf-8').hex()
    return hex_string

def bytes_to_hex_string(data):
    #将字节数据转换为十六进制字符串
    return data.hex()

def sha1_hash(text):
    #计算sha-1的hash值，以十六进制字符串形式返回
    return hashlib.sha1(text.encode()).hexdigest()

def encode_base64(hex_string):
    #将十六进制字符串转换为Base64编码
    try:
        byte_data = bytes.fromhex(hex_string)
        base64_encoded = base64.b64encode(byte_data)
        return base64_encoded.decode('utf-8')
        
    except ValueError as e:
        raise ValueError(f"无效的十六进制字符串: {str(e)}")
    except Exception as e:
        raise ValueError(f"编码失败: {str(e)}")

def decode_base64(encoded_str):
    #解码得十六进制字符串
    return bytes_to_hex_string(base64.b64decode(encoded_str))
def CRT(item_list):
    N_product = 1
    for a_val, n_val in item_list:
        N_product *= n_val
    final_result = 0
    for a_val, n_val in item_list:
        m_val = N_product // n_val
        d_val, r_val, s_val = extended_gcd(n_val, m_val)
        if d_val != 1:
            N_product = N_product // n_val
            continue
        final_result += a_val * s_val * m_val
    return final_result % N_product, N_product


if __name__ == "__main__":
    sha1 = "12345678<811101821111167"
    ebase64 = ""
    dbase64 = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    print(len(sha1_hash(sha1)))
    print(f"SHA-1: {sha1_hash(sha1)[:32]}")
    print(f"Base64编码: {encode_base64(ebase64)}")
    print(f"Base64解码: {decode_base64(dbase64)}")