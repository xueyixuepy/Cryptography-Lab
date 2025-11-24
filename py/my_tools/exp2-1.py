import hashlib
import base64
from Crypto.Cipher import AES
import binascii

def calculate_verification_number():
    """计算验证数字 """
    total_sum = 0
    number_sequence = "111116"
    multiplier_pattern = "731"
    
    for position in range(len(number_sequence)):
        total_sum += int(number_sequence[position]) * int(multiplier_pattern[position % 3])
    
    return total_sum % 10

def produce_seed_value():
    """生成种子值 """
    mrz_info = "12345678<811101821111167"
    hash_output = hashlib.sha1(mrz_info.encode())
    seed_output = hash_output.hexdigest()[:32]
    return seed_output

def derive_encryption_keys(seed_input):
    """派生加密密钥"""
    extension = "00000001"
    merged_data = seed_input + extension
    hash_value = hashlib.sha1(binascii.unhexlify(merged_data)).hexdigest()
    key_part_a = hash_value[:16]
    key_part_b = hash_value[16:32]
    return key_part_a, key_part_b

def modify_parity_bits(input_data):
    """修改奇偶校验位"""
    output_binary = []
    binary_data = bin(int(input_data, 16))[2:].zfill(64)
    
    for byte_index in range(0, len(binary_data), 8):
        seven_bits = binary_data[byte_index:byte_index+7]
        parity_value = '0' if seven_bits.count('1') % 2 == 1 else '1'
        output_binary.append(seven_bits + parity_value)
    
    modified_hex = hex(int(''.join(output_binary), 2))[2:]
    return modified_hex

if __name__ == "__main__":

    seed_value = produce_seed_value()
    print(f"种子：{seed_value}")
    key_a, key_b = derive_encryption_keys(seed_value)
    
    adjusted_key_a = modify_parity_bits(key_a)
    adjusted_key_b = modify_parity_bits(key_b)
    
    complete_key = adjusted_key_a + adjusted_key_b
    print(f"加密密钥: {complete_key}")

    encoded_message = base64.b64decode(
        "9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI")
    
    initial_vector = '0' * 32

    decryptor = AES.new(binascii.unhexlify(complete_key), AES.MODE_CBC, binascii.unhexlify(initial_vector))
    decrypted_content = decryptor.decrypt(encoded_message)
    print(f"解密结果: {decrypted_content}")