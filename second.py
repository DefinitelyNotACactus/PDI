from PIL import Image
from scipy import stats
import numpy as np
import sys
import util
import math

def main():
    print("Bem vindo ao T2 de PDI 2019.2")
    while(True):
        manipulacao = False
        try:
            op = int(input("Menu principal\nOpções:\n1 - Rotação\n2 - DCT\n3 - Aproximação usando coeficientes\n4 - Filtro passa-baixas\n0 - Sair\nOpção = "))
        except:
            break
            
        if op == 0: # sair
            break
        
        if op >= 1 and op <= 4:
            img = util.escolherImagem()
            img_array = np.asarray(img)
            
        if op == 1: # rotacao
            try:
                theta = float(input("Insira o valor de theta: "))
            except:
                theta = -1
                
            if(theta < 0 or theta > 360):
                print("Theta precisa estar entre 0 e 360!")
            else:
                try:
                    op2 = int(input("Opções:\n1 - Mapeamento direto\n2 - Mapeamento reverso\nQualquer outra coisa - retornar\nOpção = "))
                except:
                    op2 = -1
                
                if op2 >= 1:
                    img2 = rotacaoMapeamentoDireto(img_array, theta) if op == 1 else rotacaoMapeamentoReverso(img_array, theta)
                    print("Feito!")
                    manipulacao = True
                    
        elif op == 2: #dct
            img2 = DCT(img_array)
            manipulacao = True
            
        elif op == 3: # aproximacao usando n coeficientes + dc
            print("TODO!")
            
        elif op == 4: # filtro passa-baixas
            print("TODO!")

        if manipulacao:
            util.visualizar_salvar(img2)

# Rotação por mapeamento direto, IC = JC = 0
def rotacaoMapeamentoDireto(img_array, theta = 0):
    map = np.zeros((len(img_array), len(img_array[0]), 2), dtype = int) # array contendo as posições mapeadas
    cos_theta = math.cos(math.radians(theta))
    sin_theta = math.sin(math.radians(theta))
    
    upper_bound = left_bound = right_bound = lower_bound = 0
    for i in range(0, len(img_array)):
        for j in range(0, len(img_array[0])):
                map_i = round((i * cos_theta) - (j * sin_theta))
                map_j = round((i * sin_theta) + (j  * cos_theta))
                
                if map_i < upper_bound:
                    upper_bound = map_i
                elif map_i > lower_bound:
                    lower_bound = map_i
                if map_j < left_bound:
                    left_bound = map_j
                elif map_j > right_bound:
                    right_bound = map_j

                map[i][j][0] = map_i
                map[i][j][1] = map_j
                
    r = abs(lower_bound - upper_bound)
    c = abs(right_bound - left_bound)
    dummy_img_array = np.zeros((r + 1, c + 1, 3), dtype = int)
    for i in range(len(img_array)):
        for j in range(len(img_array[0])):
            dummy_img_array[map[i][j][0] + abs(upper_bound)][map[i][j][1] + abs(left_bound)] = img_array[i][j].copy()
    
    return Image.fromarray(np.uint8(dummy_img_array), mode = "RGB") # retorna a imagem transformada

def rotacaoMapeamentoReverso(img_array, theta = 45.0, ic = 0, jc = 0):
    cos_theta = math.cos(math.radians(theta))
    sin_theta = math.sin(math.radians(theta))

    c = 0
    r = 0
    if theta < 90:
        r = round((len(img_array) * sin_theta) + (len(img_array[0]) * cos_theta))
        c = round((len(img_array) * cos_theta) + (len(img_array[0]) * sin_theta))
    elif theta > 90:
        r_theta = math.radians(theta - 90)
        ar = len(img_array[0])
        ac = len(img_array)
        c = round((ac * math.cos(r_theta)) + (ar * math.sin(r_theta)))
        r = round((ac * math.sin(r_theta)) + (ar * math.cos(r_theta)))
    else: # theta = 90
        r = len(img_array[0])
        c = len(img_array)

    print("r: " + str(r) + "c: " + str(c)) 

    dummy_img_array = np.zeros((r + 1, c + 1, 3), dtype = int)
    for ir in range(1, r + 1):
      for jr in range(1, c + 1):
        x = (ir - ic) * cos_theta + (jr - jc) * sin_theta + ic
        y = -(ir - ic) * sin_theta + (jr - jc) * cos_theta + jc

        print("x: " + str(x) + "y: " + str(y))        

        if (x > 0 and x < len(img_array) and y > 0 and y < len(img_array[0])):
          lower_i = int(x // 1)
          upper_i = int((x // 1) + 1)
          lower_j = int(y // 1)
          upper_j = int((y // 1) + 1)

          f_iy = img_array[lower_i][lower_j] + (y - lower_j) * (img_array[lower_i][upper_j] - img_array[lower_i][lower_j])
          f_i1y = img_array[upper_i][lower_j] + (y - lower_j) * (img_array[upper_i][upper_j] - img_array[upper_i][lower_j])
          f_xy = f_iy + (x - lower_i) * (f_i1y - f_iy)

          f_xy[0] = round(f_xy[0])
          f_xy[1] = round(f_xy[1])
          f_xy[2] = round(f_xy[2])

          dummy_img_array[ir][jr] = f_xy.copy()
        else:
          dummy_img_array[ir][jr][0] = 0
          dummy_img_array[ir][jr][1] = 0
          dummy_img_array[ir][jr][1] = 0

    return Image.fromarray(np.uint8(dummy_img_array), mode = "RGB") # retorna a imagem transformada

# Realiza a DCT da imagem e exibe o módulo da DCT da mesma, sem o nível DC, e o valor do nível DC.
def DCT(img_array):
    pi = math.pi
    c0 = math.sqrt(1/2)
    r = len(img_array)
    c = len(img_array[0])
    dct_array = np.zeros((r, c, 1))
    
    #dct linha a linha
    for row in range(r):
        for k in range(c):
            for n in range(c):
                dct_array[row][k] += img_array[row][n][0] * math.cos((2 * pi * n * (k / (2 * c))) + ((k * pi) / (2 * c)))
                
            if k == 0:
                dct_array[row][k] *= c0
                
            dct_array[row][k] *= math.sqrt(2 / c)
            
    #dct coluna a coluna
    for column in range(c):
        for k in range(r):
            for n in range(r):
                dct_array[k][column] += dct_array[n][column] * math.cos((2 * pi * n * (k / (2 * r))) + ((k * pi) / (2 * r)))
                
            if k == 0:
                dct_array[k][column] *= c0
                
            dct_array[k][column] *= math.sqrt(2 / c)

    # TODO: Ajeitar escalonamento
    dummy_img_array = dct_array.copy()
    dc = dct_array[0][0]
    dummy_img_array[0][0] = 0 # tirar o dc da dct
    max = 0
    for i in range(r):
        for j in range(c):
            dummy_img_array[i][j] = abs(dummy_img_array[i][j])
            if dummy_img_array[i][j] > max:
                max = dummy_img_array[i][j]
                print("New max", max)
                
    for i in range(r):
        for j in range(c):
            dummy_img_array[i][j] = np.round(dummy_img_array[i][j] / max)
            dummy_img_array[i][j] = np.round(dummy_img_array[i][j])
            if dummy_img_array[i][j] > 255 or dummy_img_array[i][j] < 0:
                print(dummy_img_array[i][j] * max)
                
    return Image.fromarray(np.uint8(dummy_img_array)) # retorna a imagem transformada
                
if __name__ == "__main__":
    main()
