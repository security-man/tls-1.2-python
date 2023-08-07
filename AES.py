# AES 128, 192, 256 routines
# 128 = 10 rounds
# 192 = 12 rounds
# 256 = 14 rounds

import copy
import math

# preliminaries: switching input text to vector of bytes

def byte_block(plaintext_string):
    print('')
    print(plaintext_string)
    byte_array = bytearray(plaintext_string,'utf-8') # using utf-8 encoding, form bytearray
    print(byte_array)

    # OPERATION MODE CODE BELOW FOR PADDING (left in for simple debugging)
    padding = 16 - (len(byte_array) % 16)
    byte_array.extend([0] * padding)
    sublists = int(len(byte_array)/16)
    byte_array_2d = []
    for i in range(0,sublists):
        byte_array_2d.append(byte_array[i*16:(i*16) + 15])
    
    return byte_array

def check_array_length(byte):
    if len(byte) == 16:
        return True
    else:
        raise Exception("Byte array not length 16 (not 4x4 array)")

def most_significant_nibble(byte):
    return ((byte & 0xF0) >> 4)

def least_significant_nibble(byte):
    return (byte & 0x0F)

def print_4x4_array(array):
    for i in range(4):
        print(array[i],array[i+4],array[i+8],array[i+12])
    print('')

# round definition
# 1) substitution of bytes via S-box

# plaintext must be 1 byte
def s_box_sub(byte_array):
    s_box = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    ]
    for i in range(len(byte_array)):
        byte_array[i] = (s_box[(most_significant_nibble(byte_array[i])*16 - 1 + least_significant_nibble(byte_array[i]))])
        i = i + 1
    return byte_array

# ciphertext must be 1 byte
def inv_s_box_sub(byte_array):
    inv_s_box = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
    ]
    for i in range(len(byte_array)):
        byte_array[i] = (inv_s_box[(most_significant_nibble(byte_array[i])*16 - 1 + least_significant_nibble(byte_array[i]))])
        i = i + 1
    return byte_array

# 2) Mix rows by defined pattern

def shift_row(byte_array):
    assert check_array_length(byte_array)
    array_copy = copy.copy(byte_array)
    # shift row 1 (2nd row)
    byte_array[4] = array_copy[5]
    byte_array[5] = array_copy[6]
    byte_array[6] = array_copy[7]
    byte_array[7] = array_copy[4]
    # shift row 2 (3rd row)
    byte_array[8] = array_copy[10]
    byte_array[9] = array_copy[11]
    byte_array[10] = array_copy[8]
    byte_array[11] = array_copy[9]
    # shift row 3 (4th row)
    byte_array[12] = array_copy[15]
    byte_array[13] = array_copy[12]
    byte_array[14] = array_copy[13]
    byte_array[15] = array_copy[14]
    return byte_array

# Mix columns using Galois field with pre-defined matrices (forwards and backwards shift)

# Galois field multiplication by 2
def g_field_x2(byte):
    byte_copy = copy.copy(byte)
    if ((byte_copy >> 7) & 255) & 1:
        byte = ((byte << 1) & 255) ^ 0x1B
    else:
        byte = (byte << 1) & 255
    return byte

# Galois field forward column mixing (encrypting)
def mix_columns_forwards(byte_array):
    assert check_array_length(byte_array)
    array_copy = copy.copy(byte_array)
    for i in range(4):
        array_copy[i] = g_field_x2(byte_array[i]) ^ (g_field_x2(byte_array[4+i]) ^ byte_array[4+i]) ^ byte_array[8+i] ^ byte_array[12+i]
        array_copy[4+i] = byte_array[i] ^ g_field_x2(byte_array[4+i]) ^ (g_field_x2(byte_array[8+i]) ^ byte_array[8+i]) ^ byte_array[12+i]
        array_copy[8+i] = byte_array[i] ^ byte_array[4+i] ^ g_field_x2(byte_array[8+i]) ^ (g_field_x2(byte_array[12+i]) ^ byte_array[12+i])
        array_copy[12+i] = (g_field_x2(byte_array[i]) ^ byte_array[i]) ^ byte_array[4+i] ^ byte_array[8+i] ^ g_field_x2(byte_array[12+i])
    
    return array_copy

# Galois field backwards column mixing (decrypting)
def mix_columnds_backwards(byte_array):
    assert check_array_length(byte_array)
    array_copy = copy.copy(byte_array)
    for i in range(4):
        array_copy[i] = g_field_x2(g_field_x2(g_field_x2(byte_array[i]) ^ byte_array[i]) ^ byte_array[i]) \
        ^ (g_field_x2(g_field_x2(g_field_x2(byte_array[4+i])) ^ byte_array[4+i]) ^ byte_array[4+i]) \
              ^ (g_field_x2(g_field_x2(g_field_x2(byte_array[8+i]) ^ byte_array[8+i])) ^ byte_array[8+i]) \
                  ^ ((g_field_x2(g_field_x2(g_field_x2(byte_array[12+i])))) ^ byte_array[12+i])

        array_copy[4+i] = ((g_field_x2(g_field_x2(g_field_x2(byte_array[i])))) ^ byte_array[i]) \
             ^ g_field_x2(g_field_x2(g_field_x2(byte_array[4+i]) ^ byte_array[4+i]) ^ byte_array[4+i]) \
            ^ (g_field_x2(g_field_x2(g_field_x2(byte_array[8+i])) ^ byte_array[8+i]) ^ byte_array[8+i]) \
                  ^ (g_field_x2(g_field_x2(g_field_x2(byte_array[12+i]) ^ byte_array[12+i])) ^ byte_array[12+i])

        array_copy[8+i] = (g_field_x2(g_field_x2(g_field_x2(byte_array[i]) ^ byte_array[i])) ^ byte_array[i]) \
             ^ ((g_field_x2(g_field_x2(g_field_x2(byte_array[4+i])))) ^ byte_array[4+i]) \
                 ^ g_field_x2(g_field_x2(g_field_x2(byte_array[8+i]) ^ byte_array[8+i]) ^ byte_array[8+i]) \
        ^ (g_field_x2(g_field_x2(g_field_x2(byte_array[12+i])) ^ byte_array[12+i]) ^ byte_array[12+i])

        array_copy[12+i] = (g_field_x2(g_field_x2(g_field_x2(byte_array[i])) ^ byte_array[i]) ^ byte_array[i]) \
             ^ (g_field_x2(g_field_x2(g_field_x2(byte_array[4+i]) ^ byte_array[4+i])) ^ byte_array[4+i]) \
                 ^ ((g_field_x2(g_field_x2(g_field_x2(byte_array[8+i])))) ^ byte_array[8+i]) \
                     ^ g_field_x2(g_field_x2(g_field_x2(byte_array[12+i]) ^ byte_array[12+i]) ^ byte_array[12+i])

    return array_copy

def key_rounds(initial_key):
    if (len(initial_key) == 16):
        return 10
    elif (len(initial_key) == 24):
        return 12
    elif  (len(initial_key) == 32):
        return 14
    else:
        raise Exception("Private key invalid bit length. Key must be 128, 192, or 256 bits")
    
def rot_word(array):
    rotated_array = bytearray(4)
    rotated_array[0] = array[1]
    rotated_array[1] = array[2]
    rotated_array[2] = array[3]
    rotated_array[3] = array[0]
    return rotated_array

def key_expansion(initial_key):
    # define number of rounds for AES based on key length
    rounds = key_rounds(initial_key) + 1
    print(rounds)
    round_constant = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]
    # define number of initial 32-bit key words based on key length
    N = int(len(initial_key) / 4)
    # split initial key into 8-bit words
    K0 = bytearray(initial_key,'utf-8') # using utf-8 encoding, form bytearray    
    W = bytearray(4*(4*rounds - 1))
    for i in range(4*rounds - 1):
        if math.floor(i / 4) < N:
            W[4*i:4*i+4] = K0[4*i:4*i+4]
        elif ((i % N) == 0) and (i >= N):
            rotated_word = rot_word(W[4*(i-N):4*(i-N)+4])
            print(rotated_word)
            print(rotated_word[0])
            for j in range(4):
                W[4*i:4*i+j] = W[4*(i-N):4*(i-N)+j] ^ s_box_sub(rotated_word[j]) ^ round_constant[i/N]
        elif ((i % N) == 4) and (N > 6) and (i >= N):
            W[4*i:4*i+4] = W[4*(i-N):4*(i-N)+4] ^ s_box_sub(W[4*(i-N):4*(i-N)+4])
        else:
            W[4*i:4*i+4] = W[4*(i-N):4*(i-N)+4] ^ W[4*(i-1):4*(i-1)+4]
    return W

key_expansion("0000111122223333")

# ptext = 'Beepbeep'
# array_2d = byte_block(ptext)

# print_4x4_array(array_2d)
# mix_cols = mix_columns_forwards(array_2d)
# print_4x4_array(mix_cols)
# mix_cols_bwds = mix_columnds_backwards(mix_cols)
# print_4x4_array(mix_cols_bwds)

# 4) XOR with the respective key element of the key matrix