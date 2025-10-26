def strip_pkcs7_padding(plaintext):
    if len(plaintext) == 0:
        raise ValueError("Plaintext is empty")
    
    pad_len = plaintext[-1]
    if pad_len == 0 or pad_len > len(plaintext):
        raise ValueError("Invalid padding")
    
    for i in range(1, pad_len + 1):
        if plaintext[-i] != pad_len:
            raise ValueError("Invalid padding")
    
    return plaintext[:-pad_len]



if __name__ == "__main__":
    # 有效填充
    test1 = b"ICE ICE BABY\x04\x04\x04\x04"
    print(strip_pkcs7_padding(test1))  # b'ICE ICE BABY'
    # 无效填充
    test2 = b"ICE ICE BABY\x05\x05\x05\x05"
    try:
        strip_pkcs7_padding(test2)
    except ValueError as e:
        print(e)
    test3 = b"ICE ICE BABY\x01\x02\x03\x04"
    try:
        strip_pkcs7_padding(test3)
    except ValueError as e:
        print(e)