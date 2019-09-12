from functools import reduce
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
    return ls1(bit_array[4:8]) + ls1(bit_array[:4])

def ls1(bit_array):
    new_bit_array = bit_array
    
    for index,value in enumerate(bit_array):
        new_bit_array[index-1] = bit_array[index] 

    return new_bit_array

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

def bit_array_value(bit_array):
    byte = ""

    for i in bit_array:
        if i == 1:
            byte += '1'
        else:
            byte += '0'

    return int(byte,2)

def fk(bit_array,key):
    left = bit_array[:3]
    right = bit_array[4:]
    
    ep = permutation(right,"ep")
    xor = ep ^ key

    s0 = s_box(xor[:3],"s0")
    s1 = s_box(xor[4:],"s1")
    p4 = permutation(s0 + s1,"p4")
    
    return (left ^ p4)

def cipher(value,key):
    bit_array = value_bit_array(value)
    perm = permutation(bit_array,"init")

    k1 = permutation(sw(permutation(key,"p10"),"p8"))  
    k2 = permutation(sw(sw(permutation(key,"p10")),"p8"))

    return permutation(fk(sw(fk(perm,key)),k2),"inv_init")

def decipher(value,key):
    ip = permutation(value,"init")
    k1 = permutation(sw(permutation(key,"p10"),"p8"))  
    k2 = permutation(sw(sw(permutation(key,"p10")),"p8"))
    
    return permutation(fk(sw(fk(ip,k2)),k1),"inv_init")

if __name__ == "__main__":

    print(1022)
    print(cipher(1022,1024))
    print(decipher(cipher(1022)),1024)
    #print(permutation(1022,"p10"))
    #print(permutation(1022,"p8"))
    #print(bit_array_value(value_bit_array(1022)))
    #for i in range(256):
    #    init = permutation(i, "init")
    #    print("#######")
    #    print(init)
    #    print(sw(init))
    #    print("#######")
