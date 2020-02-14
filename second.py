from PIL import Image
from scipy import stats
import numpy as np
import sys
import util
import math

def main():
    while(True):
        manipulacao = False
        try:
            op = int(input("Menu principal\nOpções:\n1 - Rotação (sem mapeamento reverso)\n0 - Sair\nOpção = "))
        except:
            break
            
        if op == 0:
            break
            
        if op == 1: # rotacao (s/ mapeamento)
            img = util.escolherImagem()
            img_array = np.asarray(img)
            theta = float(input("Insira o valor de theta: "))
            ic = int(input("Insira o valor de ic: "))
            jc = int(input("Insira o valor de jc: "))
            print("Manipulando...")
            img2 = rotacaoSimples(img_array, theta, ic, jc)
            print("Feito!")
            manipulacao = True
        
        if manipulacao:
            util.visualizar_salvar(img2)

    
def rotacaoSimples(img_array, theta = 0, ic = 0, jc = 0):
    map = np.zeros((len(img_array), len(img_array[0]), 2), dtype = int)
    cos_theta = math.cos(math.radians(theta))
    sin_theta = math.sin(math.radians(theta))
    
    upper_bound = left_bound = right_bound = lower_bound = 0
    if(len(img_array) > 0 and len(img_array[0]) > 0):
        upper_bound = lower_bound = map[0][0][0] = round(((0 - ic) * cos_theta) - ((0 - jc) * sin_theta) + ic)
        left_bound = right_bound = map[0][0][1] = round(((0 - ic) * sin_theta) + ((0 - jc) * cos_theta) + jc)
    for i in range(1, len(img_array)):
        for j in range(1, len(img_array[0])):
                map_i = round(((i - ic) * cos_theta) - ((j - jc) * sin_theta) + ic)
                map_j = round(((i - ic) * sin_theta) + ((j - jc) * cos_theta) + jc)
                
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
    '''
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
        
    '''
    dummy_img_array = np.zeros((r + 1, c + 1, 3), dtype = int)
    for i in range(len(img_array)):
        for j in range(len(img_array[0])):
            dummy_img_array[map[i][j][0] + abs(upper_bound)][map[i][j][1] + abs(left_bound)] = img_array[i][j].copy()
    
    return Image.fromarray(np.uint8(dummy_img_array), mode = "RGB") # retorna a imagem transformada

if __name__ == "__main__":
    main()
