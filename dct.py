import math
import numpy as np
import multiprocessing as mp

# Função que realiza a DCT sobre um vetor de 1 dimensão
def DCT1D(x):
    N = len(x) # tamanho do vetor
    X = np.zeros(N) # criar um vetor de tamanho N
    
    # variaveis auxiliares de aceleracao
    c0 = math.sqrt(0.5) # valor de ck para k = 0
    coef2 = math.sqrt(2 / N) # valor do outro coeficiente externo ao somatorio
    pi = math.pi # valor de pi
    
    for k in range(N):
        sum = 0 # variavel do resultado do somatorio
        # termos do cosseno
        term1 = (pi * k) / N # primeiro termo, a ser multiplicado por n
        term2 = (k * pi) / (N << 1) # segundo termo do valor do cosseno, constante dentro do somatorio, (N << 1) equivale a (N * 2)
        for n in range(N): # laco do somatorio
            sum += x[n] * math.cos(term1 * n + term2)
        
        if k == 0: # multiplicar por c0 caso k seja 0, caso contrario, fazer nada uma vez que ck = 1 p/ k != 0
            sum *= c0
        
        sum *= coef2 # multiplicar pelo outro coeficiente
        X[k] = sum # atribuir a X[k] resultado do somatorio
        
    return X
    
# Função que realiza a DCT inversa sobre um vetor de 1 dimensão
def IDCT1D(X):
    N = len(X) # tamanho do vetor
    x = np.zeros(N) # aloca o vetor
    
    # variaveis auxiliares
    c0 = math.sqrt(0.5) # valor de ck para k = 0
    coef2 = math.sqrt(2 / N) # valor do outro coeficiente externo ao somatorio
    pi = math.pi # valor de pi
    
    for n in range(N):
        sum = 0
        # termos do cosseno
        term1 = (pi * n) / N
        term2 = pi / (N << 1)
        for k in range(N):
            if X[k] != 0: # economia de operacoes
                if k == 0:
                    sum += (c0 * X[k] * math.cos(term1 * k + term2 * k))
                else:
                    sum += X[k] * math.cos(term1 * k + term2 * k)
                    
        sum *= coef2
        x[n] = sum
        
    return x
    
# Função que realiza a DCT (ou a inversa) sobre uma imagem (na realidade poderia ser um vetor de duas dimensões qualquer)
def DCT2D(img_array, inverse = False):
    # Pool de threads, paralelizar a exeução utilizando o número de cpus da máquina
    pool = mp.Pool(mp.cpu_count())
    
    # Aplicar DCT linha a linha
    if inverse is False:
        dct_img_array = pool.map(DCT1D, img_array)
    else: # DCT Inversa
        dct_img_array = pool.map(IDCT1D, img_array)
            
    # fazer a matriz transposta da imagem, assim permitindo que as colunas virem linhas e possam ser usadas em DCT1D
    dct_img_array = np.array(dct_img_array).T.tolist()
    
    # Aplicar DCT coluna a coluna
    if inverse is False:
        dct_img_array = pool.map(DCT1D, dct_img_array)
    else: # DCT Inversa
        dct_img_array = pool.map(IDCT1D, dct_img_array)
        
    # retornar ao formato R x C original
    dct_img_array = np.array(dct_img_array).T
    
    return dct_img_array # retornar a matriz transformada
