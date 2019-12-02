from PIL import Image
from scipy import stats
import numpy as np

def main():
    img = Image.open("./images/lula_rindo.jpg") # abre o arquivo de imagem
    img_array = np.asarray(img) # transforma a imagem em array
    #img2 = banda_individual("G", img_array, True)
    #img2 = brilho_multiplicativo(img_array, False, c = 2)
    #img2 = negativo("RGB", img_array)
    #img2 = filtro_mediana(img_array, 3, 3)
    img2 = filtro_moda(img_array, 3, 3)
    img2.show() # mostra a imagem nova
    #dummy_array = conversor(img_array, True)
    #dummy_array = conversor(dummy_array, False)
    '''
    erros = 0
    erros_possiveis = len(img_array) * len(img_array[0]) * 3
    for i in range(len(img_array)):
        for j in range(len(img_array[0])):
            for k in range(3):
                if dummy_array[i][j][k] != img_array[i][j][k]:
                    print("(I = ", i, ", J = ", j, ", K = ", k, ") Dummy: ", dummy_array[i][j][k], " Original: ", img_array[i][j][k])
                    erros += 1
    print("Total erros: ", erros, "Erros possiveis: ", erros_possiveis, "(PCT: ", erros/erros_possiveis, "%)")
    '''
    
# Interface para conversão RGB-YIQ-RGB
def conversor(img_array, rgb = True):
    if rgb:
        return rgb_yiq(img_array)
    else:
        return yiq_rgb(img_array)

# Conversão de RGB para YIQ
# Y = 0.299R + 0.587G + 0.114B
# I = 0.596R – 0.274G – 0.322B
# Q = 0.211R – 0.523G + 0.312B
def rgb_yiq(img_array):
    dummy_img_array = img_array.copy().astype(float)
    for i in range(len(img_array)): # itera pelas linhas
        for j in range(len(img_array[0])): # itera pelas colunas
            dummy_img_array[i][j][0] = 0.299 * img_array[i][j][0] + 0.587 * img_array[i][j][1] + 0.114 * img_array[i][j][2]
            dummy_img_array[i][j][1] = 0.596 * img_array[i][j][0] - 0.274 * img_array[i][j][1] - 0.322 * img_array[i][j][2]
            dummy_img_array[i][j][2] = 0.211 * img_array[i][j][0] - 0.523 * img_array[i][j][1] + 0.312 * img_array[i][j][2]
            
    return dummy_img_array
    
# Conversão de YIQ para RGB
# R = 1.000 Y + 0.956 I + 0.621 Q
# G = 1.000 Y – 0.272 I – 0.647 Q
# B = 1.000 Y – 1.106 I + 1.703 Q
def yiq_rgb(img_array):
    dummy_img_array = img_array.copy().astype(int)
    for i in range(len(img_array)): # itera pelas linhas
        for j in range(len(img_array[0])): # itera pelas colunas
            dummy_img_array[i][j][0] = int(round(1 * img_array[i][j][0] + 0.956 * img_array[i][j][1] + 0.621 * img_array[i][j][2]))
            dummy_img_array[i][j][1] = int(round(1 * img_array[i][j][0] - 0.272 * img_array[i][j][1] - 0.647 * img_array[i][j][2]))
            dummy_img_array[i][j][2] = int(round(1 * img_array[i][j][0] - 1.106 * img_array[i][j][1] + 1.703 * img_array[i][j][2]))
            for k in range(3): # verificar limites
                if dummy_img_array[i][j][k] > 255:
                    dummy_img_array[i][j][k] = 255
                elif dummy_img_array[i][j][k] < 0:
                    dummy_img_array[i][j][k] = 0
    
    return np.uint8(dummy_img_array)
    
# Exibição de bandas individuais (R, G e B) como imagens monocromáticas ou coloridas (em tons de R, G ou B, respectivamente)
def banda_individual(banda, img_array, colorido):
    dummy_img_array = img_array.copy() # copia o array da imagem
    if colorido:
        for i in range(len(img_array)): # itera pelas linhas
            for j in range(len(img_array[0])): # itera pelas colunas
                if banda == "R":
                    dummy_img_array[i][j][1] = 0 # G = 0
                    dummy_img_array[i][j][2] = 0 # B = 0
                elif banda == "G":
                    dummy_img_array[i][j][0] = 0 # R = 0
                    dummy_img_array[i][j][2] = 0 # B = 0
                elif banda == "B":
                    dummy_img_array[i][j][0] = 0 # R = 0
                    dummy_img_array[i][j][1] = 0 # G = 0
    else: # monocromatico
        for i in range(len(img_array)): # itera pelas linhas
            for j in range(len(img_array[0])): # itera pelas colunas
                if banda == "R":
                    dummy_img_array[i][j][1] = dummy_img_array[i][j][0]
                    dummy_img_array[i][j][2] = dummy_img_array[i][j][0]
                elif banda == "G":
                    dummy_img_array[i][j][0] = dummy_img_array[i][j][1]
                    dummy_img_array[i][j][2] = dummy_img_array[i][j][1]
                elif banda == "B":
                    dummy_img_array[i][j][0] = dummy_img_array[i][j][2]
                    dummy_img_array[i][j][1] = dummy_img_array[i][j][2]
                    
    return Image.fromarray(dummy_img_array, mode = "RGB") # retorna a imagem transformada

def negativo(banda, img_array):
    if banda == "Y": # negativo em Y
        dummy_img_array = conversor(img_array) # converter para YIQ
        for i in range(len(img_array)): # itera pelas linhas
            for j in range(len(img_array[0])): # itera pelas colunas
                    dummy_img_array[i][j][0] = 255 - dummy_img_array[i][j][0]
        dummy_img_array = conversor(dummy_img_array, False) # converter para RGB de volta
    else:
        dummy_img_array = img_array.copy() # copia o array da imagem
        if banda == "R":
            for i in range(len(img_array)): # itera pelas linhas
                for j in range(len(img_array[0])): # itera pelas colunas
                        dummy_img_array[i][j][0] = 255 - dummy_img_array[i][j][0]
        elif banda == "G":
            for i in range(len(img_array)): # itera pelas linhas
                for j in range(len(img_array[0])): # itera pelas colunas
                        dummy_img_array[i][j][1] = 255 - dummy_img_array[i][j][1]
        elif banda == "B":
            for i in range(len(img_array)): # itera pelas linhas
                for j in range(len(img_array[0])): # itera pelas colunas
                        dummy_img_array[i][j][2] = 255 - dummy_img_array[i][j][2]
        elif banda == "RGB":
            for i in range(len(img_array)): # itera pelas linhas
                for j in range(len(img_array[0])): # itera pelas colunas
                        dummy_img_array[i][j][0] = 255 - dummy_img_array[i][j][0]
                        dummy_img_array[i][j][1] = 255 - dummy_img_array[i][j][1]
                        dummy_img_array[i][j][2] = 255 - dummy_img_array[i][j][2]

    return Image.fromarray(dummy_img_array, mode = "RGB") # retorna a imagem transformada

def brilho_multiplicativo(img_array, rgb = True, c = 1.0):
    if c < 0:
        return img_array
    else:
        if rgb:
            dummy_img_array = img_array.copy()
            for i in range(len(img_array)): # itera pelas linhas
                for j in range(len(img_array[0])): # itera pelas colunas
                    pixel = dummy_img_array[i][j].copy()
                    for k in range(3):
                        banda = pixel[k] * c
                        if banda > 255: # verificar limites
                            banda = 255
                        elif banda < 0: # imagino que isso nao ocorre pois c >= 0
                            banda = 0
                        dummy_img_array[i][j][k] = banda
        else:
            dummy_img_array = conversor(img_array) # converter para yiq
            for i in range(len(img_array)): # itera pelas linhas
                for j in range(len(img_array[0])): # itera pelas colunas
                    y = dummy_img_array[i][j][0].copy()
                    y = y * c
                    dummy_img_array[i][j][0] = y
            dummy_img_array = conversor(dummy_img_array, False) # retornar para rgb
            
        return Image.fromarray(dummy_img_array, mode = "RGB") # retorna a imagem transformada

def filtro_mediana(img_array, m, n):
    if m >= 1 and n >= 1:
        pivo_i = int(m % 2 == 0)
        pivo_j = int(n % 2 == 0)
        limite_i = m//2
        limite_j = n//2
        dummy_img_array = np.zeros((len(img_array) - limite_i, len(img_array[0]) - limite_j, 3), dtype = int)
        x = 0
        y = 0
        for i in range(limite_i - pivo_i, len(img_array) - limite_i + 1): # s/ extensao
            y = 0
            for j in range(limite_j - pivo_j, len(img_array[0]) - limite_j + 1):
                vizinhosR = img_array[i - limite_i + pivo_i : i + limite_i + 1 , j - limite_j + pivo_j : j + limite_j + 1, 0]
                vizinhosG = img_array[i - limite_i + pivo_i : i + limite_i + 1 , j - limite_j + pivo_j : j + limite_j + 1, 1]
                vizinhosB = img_array[i - limite_i + pivo_i : i + limite_i + 1 , j - limite_j + pivo_j : j + limite_j + 1, 2]
                mediana = [np.median(vizinhosR), np.median(vizinhosG), np.median(vizinhosB)]
                dummy_img_array[x][y] = mediana
                y += 1
            x += 1
        return Image.fromarray(np.uint8(dummy_img_array), mode = "RGB") # retorna a imagem transformada
    else:
        return img_array
    
def filtro_moda(img_array, m, n):
    if m >= 1 and n >= 1:
        pivo_i = int(m % 2 == 0)
        pivo_j = int(n % 2 == 0)
        limite_i = m//2
        limite_j = n//2
        dummy_img_array = np.zeros((len(img_array) - limite_i, len(img_array[0]) - limite_j, 3), dtype = int)
        x = 0
        y = 0
        for i in range(limite_i - pivo_i, len(img_array) - limite_i + 1): # s/ extensao
            y = 0
            for j in range(limite_j - pivo_j, len(img_array[0]) - limite_j + 1):
                vizinhosR = img_array[i - limite_i + pivo_i : i + limite_i + 1 , j - limite_j + pivo_j : j + limite_j + 1, 0]
                vizinhosG = img_array[i - limite_i + pivo_i : i + limite_i + 1 , j - limite_j + pivo_j : j + limite_j + 1, 1]
                vizinhosB = img_array[i - limite_i + pivo_i : i + limite_i + 1 , j - limite_j + pivo_j : j + limite_j + 1, 2]
                moda = [stats.mode(vizinhosR)[0][0][0], stats.mode(vizinhosG)[0][0][0], stats.mode(vizinhosB)[0][0][0]]
                dummy_img_array[x][y] = moda
                y += 1
            x += 1

        return Image.fromarray(np.uint8(dummy_img_array), mode = "RGB") # retorna a imagem transformada
    else:
        return img_array
        
if __name__ == "__main__":
    main()
