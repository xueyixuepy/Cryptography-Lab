import base64

def base64_to_hex_simple(base64_string):
    """简化版本的Base64转十六进制函数"""
    decoded_bytes = base64.b64decode(base64_string)
    return decoded_bytes.hex()

# 使用示例
base64_str = "9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI"  # "Hello" 的Base64编码
hex_str = base64_to_hex_simple(base64_str)
print(hex_str)  # 输出: 48656c6c6f