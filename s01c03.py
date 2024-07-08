#CHALLENGE 3: Single-byte XOR cipher

# Hex encoded string
hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

# Convert hex string to bytes
bytes_data = bytes.fromhex(hex_string)

def score_text(text):
    """Scores text based on the number of printable ASCII characters."""
    return sum([32 <= byte < 127 for byte in text])

def single_byte_xor_decrypt(data):
    """Finds the single-byte XOR key and decrypts the message."""
    potential_messages = []
    
    for key in range(256):
        decrypted = bytes([byte ^ key for byte in data])
        score = score_text(decrypted)
        potential_messages.append((score, key, decrypted))
    
    best_score, best_key, best_message = max(potential_messages, key=lambda item: item[0])
    return best_key, best_message

# Find the key and the decrypted message
key, decrypted_message = single_byte_xor_decrypt(bytes_data)
print(f"Key: {chr(key)} (0x{key:02x})")
print(f"Decrypted message: {decrypted_message.decode('utf-8')}")