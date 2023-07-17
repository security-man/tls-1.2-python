# AES 128, 192, 256 routines
# 128 = 10 rounds
# 192 = 12 rounds
# 256 = 14 rounds

# round definition
# 1) substitution of bytes via S-box

# plaintext must be 1 byte
def s_box_sub(plaintext):
    S1 = [1,0,0,0,1,1,1,1]
    S2 = [1,1,0,0,0,1,1,1]
    S3 = [1,1,1,0,0,0,1,1]
    S4 = [1,1,1,1,0,0,0,1]
    S5 = [1,1,1,1,1,0,0,0]
    S6 = [0,1,1,1,1,1,0,0]
    S7 = [0,0,1,1,1,1,1,0]
    S8 = [0,0,0,1,1,1,1,1]
    S = [S1,S2,S3,S4,S5,S6,S7,S8]
    S_add = [1,1,0,0,0,1,1,0]
    shifted_plaintext = [0,0,0,0,0,0,0,0]
    plaintext_bits = int(bin(plaintext),2)
    print(plaintext_bits)
    print(S[0][0])
    shifted_plaintext[0] = (S[0][0]*plaintext_bits[0] + S[0][1]*plaintext_bits[1] + 
                            S[0][2]*plaintext_bits[2] + S[0][3]*plaintext_bits[3] + 
                             S[0][4]*plaintext_bits[4] + S[0][5]*plaintext_bits[5] +
                              S[0][6]*plaintext_bits[6] + S[0][7]*plaintext_bits[7] + S_add[0])
    
    shifted_plaintext[1] = (S[1][0]*plaintext_bits[0] + S[1][1]*plaintext_bits[1] + 
                            S[1][2]*plaintext_bits[2] + S[1][3]*plaintext_bits[3] + 
                             S[1][4]*plaintext_bits[4] + S[1][5]*plaintext_bits[5] +
                              S[1][6]*plaintext_bits[6] + S[1][7]*plaintext_bits[7] + S_add[1])
    
    shifted_plaintext[2] = (S[2][0]*plaintext_bits[0] + S[2][1]*plaintext_bits[1] + 
                            S[2][2]*plaintext_bits[2] + S[2][3]*plaintext_bits[3] + 
                             S[2][4]*plaintext_bits[4] + S[2][5]*plaintext_bits[5] +
                              S[2][6]*plaintext_bits[6] + S[2][7]*plaintext_bits[7] + S_add[2])
    
    shifted_plaintext[3] = (S[3][0]*plaintext_bits[0] + S[3][1]*plaintext_bits[1] + 
                            S[3][2]*plaintext_bits[2] + S[3][3]*plaintext_bits[3] + 
                             S[3][4]*plaintext_bits[4] + S[3][5]*plaintext_bits[5] +
                              S[3][6]*plaintext_bits[6] + S[3][7]*plaintext_bits[7] + S_add[3])
    
    shifted_plaintext[4] = (S[4][0]*plaintext_bits[0] + S[4][1]*plaintext_bits[1] + 
                            S[4][2]*plaintext_bits[2] + S[4][3]*plaintext_bits[3] + 
                             S[4][4]*plaintext_bits[4] + S[4][5]*plaintext_bits[5] +
                              S[4][6]*plaintext_bits[6] + S[4][7]*plaintext_bits[7] + S_add[4])
    
    shifted_plaintext[5] = (S[5][0]*plaintext_bits[0] + S[5][1]*plaintext_bits[1] + 
                            S[5][2]*plaintext_bits[2] + S[5][3]*plaintext_bits[3] + 
                             S[5][4]*plaintext_bits[4] + S[5][5]*plaintext_bits[5] +
                              S[5][6]*plaintext_bits[6] + S[5][7]*plaintext_bits[7] + S_add[5])
    
    shifted_plaintext[6] = (S[6][0]*plaintext_bits[0] + S[6][1]*plaintext_bits[1] + 
                            S[6][2]*plaintext_bits[2] + S[6][3]*plaintext_bits[3] + 
                             S[6][4]*plaintext_bits[4] + S[6][5]*plaintext_bits[5] +
                              S[6][6]*plaintext_bits[6] + S[6][7]*plaintext_bits[7] + S_add[6])
    
    shifted_plaintext[7] = (S[7][0]*plaintext_bits[0] + S[7][1]*plaintext_bits[1] + 
                            S[7][2]*plaintext_bits[2] + S[7][3]*plaintext_bits[3] + 
                             S[7][4]*plaintext_bits[4] + S[7][5]*plaintext_bits[5] +
                              S[7][6]*plaintext_bits[6] + S[7][7]*plaintext_bits[7] + S_add[7])
    
    return shifted_plaintext

# ciphertext must be 1 byte
def inv_s_box_sub(ciphertext):
    Sinv1 = [0,0,1,0,0,1,0,1]
    Sinv2 = [1,0,0,1,0,0,1,0]
    Sinv3 = [0,1,0,0,1,0,0,1]
    Sinv4 = [1,0,1,0,0,1,0,0]
    Sinv5 = [0,1,0,1,0,0,1,0]
    Sinv6 = [0,0,1,0,1,0,0,1]
    Sinv7 = [1,0,0,1,0,1,0,0]
    Sinv8 = [0,1,0,0,1,0,1,0]
    Sinv = [[Sinv1],[Sinv2],[Sinv3],[Sinv4],[Sinv5],[Sinv6],[Sinv7],[Sinv8]]
    S_inv_add = [1,0,1,0,0,0,0,0]
    shifted_ciphertext = [0,0,0,0,0,0,0,0]
    ciphertext_bits = bin(ciphertext)[2:]
    shifted_ciphertext[0] = (Sinv[0][0]*ciphertext_bits[0] + Sinv[0][1]*ciphertext_bits[1] + 
                            Sinv[0][2]*ciphertext_bits[2] + Sinv[0][3]*ciphertext_bits[3] + 
                             Sinv[0][4]*ciphertext_bits[4] + Sinv[0][5]*ciphertext_bits[5] +
                              Sinv[0][6]*ciphertext_bits[6] + Sinv[0][7]*ciphertext_bits[7] + S_inv_add[0])
    
    shifted_ciphertext[1] = (Sinv[1][0]*ciphertext_bits[0] + Sinv[1][1]*ciphertext_bits[1] + 
                            Sinv[1][2]*ciphertext_bits[2] + Sinv[1][3]*ciphertext_bits[3] + 
                             Sinv[1][4]*ciphertext_bits[4] + Sinv[1][5]*ciphertext_bits[5] +
                              Sinv[1][6]*ciphertext_bits[6] + Sinv[1][7]*ciphertext_bits[7] + S_inv_add[1])
    
    shifted_ciphertext[2] = (Sinv[2][0]*ciphertext_bits[0] + Sinv[2][1]*ciphertext_bits[1] + 
                            Sinv[2][2]*ciphertext_bits[2] + Sinv[2][3]*ciphertext_bits[3] + 
                             Sinv[2][4]*ciphertext_bits[4] + Sinv[2][5]*ciphertext_bits[5] +
                              Sinv[2][6]*ciphertext_bits[6] + Sinv[2][7]*ciphertext_bits[7] + S_inv_add[2])
    
    shifted_ciphertext[3] = (Sinv[3][0]*ciphertext_bits[0] + Sinv[3][1]*ciphertext_bits[1] + 
                            Sinv[3][2]*ciphertext_bits[2] + Sinv[3][3]*ciphertext_bits[3] + 
                             Sinv[3][4]*ciphertext_bits[4] + Sinv[3][5]*ciphertext_bits[5] +
                              Sinv[3][6]*ciphertext_bits[6] + Sinv[3][7]*ciphertext_bits[7] + S_inv_add[3])
    
    shifted_ciphertext[4] = (Sinv[4][0]*ciphertext_bits[0] + Sinv[4][1]*ciphertext_bits[1] + 
                            Sinv[4][2]*ciphertext_bits[2] + Sinv[4][3]*ciphertext_bits[3] + 
                             Sinv[4][4]*ciphertext_bits[4] + Sinv[4][5]*ciphertext_bits[5] +
                              Sinv[4][6]*ciphertext_bits[6] + Sinv[4][7]*ciphertext_bits[7] + S_inv_add[4])
    
    shifted_ciphertext[5] = (Sinv[5][0]*ciphertext_bits[0] + Sinv[5][1]*ciphertext_bits[1] + 
                            Sinv[5][2]*ciphertext_bits[2] + Sinv[5][3]*ciphertext_bits[3] + 
                             Sinv[5][4]*ciphertext_bits[4] + Sinv[5][5]*ciphertext_bits[5] +
                              Sinv[5][6]*ciphertext_bits[6] + Sinv[5][7]*ciphertext_bits[7] + S_inv_add[5])
    
    shifted_ciphertext[6] = (Sinv[6][0]*ciphertext_bits[0] + Sinv[6][1]*ciphertext_bits[1] + 
                            Sinv[6][2]*ciphertext_bits[2] + Sinv[6][3]*ciphertext_bits[3] + 
                             Sinv[6][4]*ciphertext_bits[4] + Sinv[6][5]*ciphertext_bits[5] +
                              Sinv[6][6]*ciphertext_bits[6] + Sinv[6][7]*ciphertext_bits[7] + S_inv_add[6])
    
    shifted_ciphertext[7] = (Sinv[7][0]*ciphertext_bits[0] + Sinv[7][1]*ciphertext_bits[1] + 
                            Sinv[7][2]*ciphertext_bits[2] + Sinv[7][3]*ciphertext_bits[3] + 
                             Sinv[7][4]*ciphertext_bits[4] + Sinv[7][5]*ciphertext_bits[5] +
                              Sinv[7][6]*ciphertext_bits[6] + Sinv[7][7]*ciphertext_bits[7] + S_inv_add[7])

    return shifted_ciphertext

abytes=(bytearray('zachary','utf-8'))
print(s_box_sub(abytes[0]))

# 2) shifting rows by one

# 3) Hill cipher used to jumble the message by mixing the block's columns

# 4) XOR with the respective key element of the key matrix