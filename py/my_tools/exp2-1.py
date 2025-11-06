import hashlib
import base64
from Crypto.Cipher import AES
import binascii

def compute_check_digit():
    result = 0
    digits = "111116"
    weights = "731"
    for idx in range(len(digits)):
        result += int(digits[idx]) * int(weights[idx % 3])
    return result % 10

def generate_k_seed():
    mrz_data = "12345678<811101821111167"
    hash_obj = hashlib.sha1(mrz_data.encode())
    k_seed = hash_obj.hexdigest()[:32]
    return k_seed

def compute_ka_kb(seed):
    suffix = "00000001"
    combined = seed + suffix
    hash_result = hashlib.sha1(binascii.unhexlify(combined)).hexdigest()
    ka = hash_result[:16]
    kb = hash_result[16:32]
    return ka, kb

def adjust_parity(data):
    result_bits = []
    binary_rep = bin(int(data, 16))[2:].zfill(64)
    
    for i in range(0, len(binary_rep), 8):
        byte_segment = binary_rep[i:i+7]
        parity_bit = '1' if byte_segment.count('1') % 2 == 0 else '0'
        result_bits.append(byte_segment + parity_bit)
    
    adjusted_hex = hex(int(''.join(result_bits), 2))[2:]
    return adjusted_hex

def main():
    k_seed = generate_k_seed()
    ka, kb = compute_ka_kb(k_seed)
    
    k1_adjusted = adjust_parity(ka)
    k2_adjusted = adjust_parity(kb)
    
    final_key = k1_adjusted + k2_adjusted
    print(f"key: {final_key}")

    encrypted_data = base64.b64decode(
        "9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI")
    
    initialization_vector = '0' * 32

    cipher = AES.new(binascii.unhexlify(final_key), AES.MODE_CBC, binascii.unhexlify(initialization_vector))
    decrypted_text = cipher.decrypt(encrypted_data)
    print(f"m: {decrypted_text}")

if __name__ == "__main__":
    main()