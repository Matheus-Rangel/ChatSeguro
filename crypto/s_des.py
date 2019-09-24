from functools import reduce
from math import log2
def permutation(bit_array, p_type):
    if(p_type == "init"):
        ip = [2, 6, 3, 1, 4 ,8 ,5, 7]
    elif(p_type == "inv_init"):
        ip = [4, 1, 3, 5, 7, 2, 8, 6]
    elif(p_type == "p10"):
        ip = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    elif(p_type == "p8"):
        ip = [6, 3, 7, 4, 8 , 5, 10, 9]
    elif(p_type == "p4"):
        ip = [2,4,3,1]
    elif(p_type == "ep"):
        ip = [4,1,2,3,4,2,3,4,1]
    
    result_bit_array = [0 for i in range(len(ip))]
    for index,value in enumerate(ip):
        result_bit_array[index] = bit_array[value-1]
    return result_bit_array

def sw(bit_array):
    size = len(bit_array)
    return ls1(bit_array[size//2:size]) + ls1(bit_array[:size//2])

def ls1(bit_array):
    return bit_array[-1:0:-1] + bit_array[:1]

def s_box(bit_array, box_type):
    if(box_type == "s0"):
        box = [
            [1, 0, 3, 2],
            [3, 2, 1, 0],
            [0, 2, 1, 3],
            [3, 1, 3, 2]
        ]
    elif(box_type == "s1"):
        box = [
            [1, 1, 2, 3],
            [2, 0, 1, 3],
            [3, 0, 1, 0],
            [2, 1, 0, 3]
        ]
    line = bit_array[0] & bit_array[3]
    col = bit_array[1] & bit_array[2] 

    boxValue = box[line][col]
    return_val = value_bit_array(boxValue) 
    if(len(return_val) == 1):
      return_val = [0] + return_val 
    return return_val

def value_bit_array(value,array_size=8):

    #if(int(log2(value)) >= array_size):
    #  raise ValueError("Input size in bits is bigger than expected, \
    #                   make sure that the second argument is bigger than log2(first_arg)") 

    bit_array = [0 for i in range(array_size)]
    array_index = -1
    if (value == 0):
      return [0]
    while(value != 0):
      bit_array[array_index] = value % 2
      array_index -= 1
    #    bit_array[] = [value%2] + bit_array
      value >>= 1
    return bit_array

def bit_array_value(bit_array):
    byte = ""

    for i in bit_array:
        if i == 1:
            byte += '1'
        else:
            byte += '0'

    return int(byte,2)

def fk(bit_array,key):
    left = bit_array[:4]
    right = bit_array[4:]
    ep = permutation(right,"ep")
    xor = [a ^ b for a,b in zip(ep,key)]

    s0 = s_box(xor[:4],"s0")
    s1 = s_box(xor[4:],"s1")
    p4 = permutation(s0 + s1,"p4")
    
    return [a ^ b for a,b in zip(left,p4)] + right

def cipher(value,key):
    bit_array = value_bit_array(value)
    chave = value_bit_array(key,10)
    perm = permutation(bit_array,"init")

    k1 = permutation(sw(permutation(chave,"p10")),"p8")  
    k2 = permutation(sw(sw(permutation(chave,"p10"))), "p8")
    firstFk = fk(perm,k1)
    firstSw = sw(firstFk)
    secondFk = fk(firstSw,k2)
    return bytearray([(bit_array_value(permutation(secondFk,"inv_init")))])

def decipher(value,key):
    bit_array = value_bit_array(value)
    chave = value_bit_array(key,10)
    perm = permutation(bit_array,"init")

    k1 = permutation(sw(permutation(chave,"p10")),"p8")  
    k2 = permutation(sw(sw(permutation(chave,"p10"))), "p8")

    return bytearray([(bit_array_value(permutation(fk(sw(fk(perm,k2)),k1),"inv_init")))])

def cipher_text(text, key):
    resultado = bytearray()
    for c in text:
        resultado += cipher(c, key)
    return resultado
def decipher_text(text, key):
    resultado = bytearray()
    for c in text:
        resultado += decipher(c, key)
    return resultado
    
if __name__ == "__main__":

    print(60)
    print(cipher(60,1023))
    print(decipher(cipher(60,1023),1023))
