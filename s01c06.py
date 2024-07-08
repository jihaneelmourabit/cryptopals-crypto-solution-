# CHALLNEG 06 .Break repeating-key XOR
#import base64
from itertools import cycle

# Hamming distance function
def hamming_distance(s1, s2):
    assert len(s1) == len(s2)
    distance = 0
    for b1, b2 in zip(s1, s2):
        diff = b1 ^ b2
        distance += bin(diff).count('1')
    return distance

# Function to compute the average normalized Hamming distance for a given KEYSIZE
def average_hamming_distance(ciphertext, keysize):
    chunks = [ciphertext[i:i + keysize] for i in range(0, len(ciphertext), keysize)]
    num_chunks = len(chunks)
    
    distances = []
    for i in range(num_chunks - 1):
        distances.append(hamming_distance(chunks[i], chunks[i + 1]) / keysize)
    
    return sum(distances) / len(distances)

# Function to break repeating-key XOR
def break_repeating_key_xor(ciphertext):
    # Step 1: Find the best KEYSIZE
    normalized_distances = []
    for keysize in range(2, 41):
        normalized_distances.append((keysize, average_hamming_distance(ciphertext, keysize)))
    best_keysize = min(normalized_distances, key=lambda x: x[1])[0]
    
    # Step 2: Transpose blocks
    blocks = [ciphertext[i:i + best_keysize] for i in range(0, len(ciphertext), best_keysize)]
    transposed_blocks = list(zip(*blocks))
    
    # Step 3: Solve each transposed block as single-character XOR
    key = bytearray()
    for block in transposed_blocks:
        key.append(single_byte_xor_key(block))
    
    # Step 4: Decrypt the ciphertext with the found key
    decrypted = xor_with_key(ciphertext, key)
    
    return key, decrypted

# Function to find the single-byte XOR key for a given block
def single_byte_xor_key(block):
    # Simple scoring based on printable characters and spaces
    best_key = None
    best_score = float('-inf')
    
    for k in range(256):
        decrypted = bytearray(b ^ k for b in block)
        current_score = sum(1 for byte in decrypted if 32 <= byte <= 126)  # Count printable characters
        if current_score > best_score:
            best_score = current_score
            best_key = k
            
    return best_key

# Function to XOR a ciphertext with a key
def xor_with_key(ciphertext, key):
    return bytearray(b ^ k for b, k in zip(ciphertext, cycle(key)))

# The provided base64 encoded ciphertext
base64_ciphertext = '''HUIfTQsPAh9PE048GmllH0kcDk4TAQsHThsBFkU2AB4BSWQgVB0dQzNTTmVS
BgBHVBwNRU0HBAxTEjwMHghJGgkRTxRMIRpHKwAFHUdZEQQJAGQmB1MANxYG
DBoXQR0BUlQwXwAgEwoFR08SSAhFTmU+Fgk4RQYFCBpGB08fWXh+amI2DB0P
QQ1IBlUaGwAdQnQEHgFJGgkRAlJ6f0kASDoAGhNJGk9FSA8dDVMEOgFSGQEL
QRMGAEwxX1NiFQYHCQdUCxdBFBZJeTM1CxsBBQ9GB08dTnhOSCdSBAcMRVhI
CEEATyBUCHQLHRlJAgAOFlwAUjBpZR9JAgJUAAELB04CEFMBJhAVTQIHAh9P
G054MGk2UgoBCVQGBwlTTgIQUwg7EAY
