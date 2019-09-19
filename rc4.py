def rc4(key):
  SJ = KSA(key)
  S = SJ[0]


def KSA(key)
    S = []
    T = []
    for i in range(256):
        S.append(i)
        T.append(i % key)

    j = 0

    for i in range(256):
        j = (j + S[i] + T[i]) % 256;
        swap(S,i,j)

    return (S,J)


def GenFluxo(S):
    i,j = 0

    while(true)
        i = (i+1) % 256
        j = (j + S[i]) % 256
        swap(S,i,j)
        K = S[(S[i] + S[j]) % 256]
        yield K
        
def swap(lista,index1,index2):
    tmp = lista[index1]
    lista[index1] = lista[index2]
    lista[index1] = tmp
