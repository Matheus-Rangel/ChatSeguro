

from functools import reduce
def permutation(value, p_type):
    if(p_type == "init"):
        ip = [2, 6, 3, 1, 4 ,8 ,5, 7]
    elif(p_type == "inv_init"):
        ip = [4, 1, 3, 5, 7, 2, 8, 6]
    elif(p_type == "p10"):
        ip = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    elif(p_type == "p8"):
        ip = [6, 3, 7, 4, 8 , 5, 10, 9]
    
    bit_array = [0 for i in range(len(ip))]
    power = 2**(len(ip) - 1)
    for i in ip:
        bit_array[i-1] = (value & power)//power
        value <<= 1
    # r = 0
    # for i, bit in enumerate(bit_array[::-1]):
    #     r += bit*2**i
    return bit_array
def sw(bit_array):
    return bit_array[4:8] + bit_array[:4]

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
    
    return box[line][col]
def value_bit_array(value):
    bit_array = []
    while(value != 0):
        bit_array = [value%2] + bit_array
        value >>= 1
    return bit_array
def fk():
    pass
def cipher():
    pass
def decipher():
    pass
if __name__ == "__main__":
    for i in range(256):
        init = permutation(i, "init")
        print("#######")
        print(init)
        print(sw(init))