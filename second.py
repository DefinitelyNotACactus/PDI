from PIL import Image
from scipy import stats
import numpy as np
import sys
import util
import math

def main():
    img = util.escolherImagem()
    img_array = np.asarray(img)
    img2 = rotacaoSimples(img_array, 35, 25, 10)
    util.visualizar_salvar(img2)
    
def rotacaoSimples(img_array, theta = 0, ic = 0, jc = 0):
    map = np.zeros((len(img_array), len(img_array[0]), 2), dtype = int)
    cos_theta = math.cos(math.radians(theta))
    sin_theta = math.sin(math.radians(theta))
    
    lower_bound = left_bound = 0
    for i in range(len(img_array)):
        for j in range(len(img_array[0])):
                map_i = round(((i - ic) * cos_theta) - ((j - jc) * sin_theta) + ic)
                map_j = round(((i - ic) * sin_theta) + ((j - jc) * cos_theta) + jc)
                if map_i < lower_bound:
                    lower_bound = map_i
                if map_j < left_bound:
                    left_bound = map_j
                if (i == 0 and j == 0):
                    print(map_i)
                    print(map_j)
                map[i][j][0] = map_i
                map[i][j][1] = map_j
    r = c = 0
    left_bound = abs(left_bound)
    lower_bound = abs(lower_bound)
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
        
    dummy_img_array = np.zeros((r, c, 3), dtype = int)
    for i in range(len(img_array)):
        for j in range(len(img_array[0])):
            dummy_img_array[round(((i - ic) * cos_theta) - ((j - jc) * sin_theta) + ic)][round(((i - ic) * sin_theta) + ((j - jc) * cos_theta) + jc)] = img_array[i][j].copy()
    
    return Image.fromarray(np.uint8(dummy_img_array), mode = "RGB") # retorna a imagem transformada

if __name__ == "__main__":
    main()
