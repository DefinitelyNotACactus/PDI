from PIL import Image
from scipy import stats
import numpy as np
import sys

def main():
    print("Bem vindo ao T1 de PDI 2019.2")
    while(True):
        manipulacao = False
        try:
            op = int(input("Menu principal\nOpções:\n1 - Conversão RGB -> YIQ -> RGB\n2 - Exibição de banda individual\n3 - Negativo\n4 - Controle de brilho multiplicativo\n5 - Convolução m x n\n6 - Filtro mediana e moda m x n\n0 - Sair\nOpção = "))
        except:
            break
            
        if op == 0:
            break
            
        if op >= 1 and op <= 6:
            img = escolherImagem()
            img_array = np.asarray(img)
            img2 = None
            
        if op == 1: # conversao
            try:
                op = int(input("Opções:\n 1 - RGB -> YIQ \n 2 - YIQ -> RGB \n 3 - RGB -> YIQ -> RGB\n Qualquer outra coisa - retornar\nOpção = "))
            except:
                op = -1
                
            if op == 1 or op == 2:
                print("Convertendo...")
                dummy_array = conversor(img_array, True if op == 1 else False)
                print("Feito!")
                #manipulacao = False
            elif op == 3:
                print("Convertendo...")
                dummy_array = conversor(img_array, True)
                dummy_array = conversor(dummy_array, False)
                print("Feito!")
                #manipulacao = False
                
        elif op == 2: # banda individual
            try:
                op = int(input("Opções:\n1 - R \n2 - G \n3 - B\nQualquer outra coisa - retornar\nOpção = "))
            except:
                op = -1
            if op >= 1 and op <= 3:
                try:
                    op2 = int(input("Monocromático:\n1 - Sim \nQualquer outra coisa - Não\nMonocromático = "))
                except:
                    op2 = -1
                    
                print("Manipulando...")
                if op == 1:
                    img2 = banda_individual("R", img_array, True if op2 == 0 else False)
                elif op == 2:
                    img2 = banda_individual("G", img_array, True if op2 == 0 else False)
                elif op == 3:
                    img2 = banda_individual("B", img_array, True if op2 == 0 else False)
                print("Feito!")
                manipulacao = True
            
        elif op == 3: # negativo
            try:
                op = int(input("Opções:\n1 - Operação em RGB \n2 - Operação em Y\nQualquer outra coisa - retornar\nOpção = "))
            except:
                op = -1
                
            print("Manipulando...")
            if op == 1:
                img2 = negativo("RGB", img_array)
            elif op == 2:
                img2 = negativo("Y", img_array)
            print("Feito!")
            manipulacao = True
            
        elif op == 4: # brilho multiplicativo
            try:
                c = float(input("Insira o valor de c: "))
            except:
                c = 1.0
            try:
                op = int(input("Opções:\n1 - Operação em RGB \n2 - Operação em Y\nQualquer outra coisa - retornar\nOpção = "))
            except:
                op = -1
                
            print("Manipulando...")
            if op == 1:
                img2 = brilho_multiplicativo(img_array, True, c)
            elif op == 2:
                img2 = brilho_multiplicativo(img_array, False, c)
            print("Feito!")
            manipulacao = True
            
        elif op == 5: # convolucao
            mascara = lerMascara()
            print("Manipulando...")
            img2 = convolucao(img_array, mascara)
            print("Feito!")
            manipulacao = True
            
        elif op == 6: # mediana e moda
            #try:
                m = int(input("Insira o valor de m: "))
                n = int(input("Insira o valor de n: "))
                op = int(input("Opções:\n1 - Mediana \n2 - Moda\nQualquer outro número - retornar\nOpção = "))
                print("Manipulando...")
                if op == 1: # mediana
                    img2 = filtro_moda_mediana(img_array, m, n, True)
                elif op == 2: # moda
                    img2 = filtro_moda_mediana(img_array, m, n, False)
                print("Feito!")
                manipulacao = True
            #except:
            #    print("Insira valores válidos!")
                    
        if manipulacao:
            visualizar_salvar(img2)
            
def lerMascara():
    arq = str(input("Insira o endereço da mascara: "))
    try:
        f = open(arq, "r")
        txt = f.readlines()
        m, n, i = 0, 0, 0
        mascara = []
        for line in txt:
            s = line.split()
            if i == 0:
                m = int(s[0])
                n = int(s[1])
            else:
                ml = []
                for x in range(n):
                    ml.append(float(s[x]))
                mascara.append(ml)
            i += 1
        return mascara
    except:
        print("Erro ao abrir a máscara, abortando...")
        sys.exit()
        
def visualizar_salvar(img):
    try:
        op = int(input("Deseja visualizar a imagem manipulada?\n1 - Sim \nQualquer outra coisa - Não\nVisualizar = "))
    except:
        op = -1
    if op == 1:
        img.show()
        try:
            op = int(input("Deseja salvar a imagem manipulada?\n1 - Sim \nQualquer outra coisa - Não\nSalvar = "))
        except:
            op = -1
        if op == 1:
            nome_img = str(input("Insira o nome da imagem para ser salva: "))
            try:
                img.save(nome_img)
                print("A imagem foi salva no diretório atual")
            except:
                print("Erro ao salvar a imagem, abortando...")
                sys.exit()
                
def escolherImagem():
    try:
        img = Image.open(str(input("Insira o endereço da imagem: ")))
        return img
    except:
        print("Não foi possível abrir a imagem, abortando...")
        sys.exit()

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

def filtro_moda_mediana(img_array, m, n, mediana = True):
    if m > 1 and n > 1:
        pivo_i = int(m % 2 == 0)
        pivo_j = int(n % 2 == 0)
        limite_i = m//2
        limite_j = n//2
        dummy_img_array = np.zeros((len(img_array) - (2 * limite_i) + pivo_i, len(img_array[0]) - (2 * limite_j) + pivo_j, 3), dtype = int)
        x = 0
        for i in range(limite_i - pivo_i, len(img_array) - limite_i): # s/ extensao
            y = 0
            for j in range(limite_j - pivo_j, len(img_array[0]) - limite_j):
                vizinhosR = img_array[i - limite_i + pivo_i : i + limite_i + 1 , j - limite_j + pivo_j : j + limite_j + 1, 0]
                vizinhosG = img_array[i - limite_i + pivo_i : i + limite_i + 1 , j - limite_j + pivo_j : j + limite_j + 1, 1]
                vizinhosB = img_array[i - limite_i + pivo_i : i + limite_i + 1 , j - limite_j + pivo_j : j + limite_j + 1, 2]
                if mediana:
                    g = [np.median(vizinhosR), np.median(vizinhosG), np.median(vizinhosB)]
                else:
                    g = [stats.mode(vizinhosR)[0][0][0], stats.mode(vizinhosG)[0][0][0], stats.mode(vizinhosB)[0][0][0]]
                dummy_img_array[x][y] = g
                y += 1
            x += 1
        return Image.fromarray(np.uint8(dummy_img_array), mode = "RGB") # retorna a imagem transformada
    else:
        return img_array

def convolucao(img_array, filtro_array):
    conv1 = []
    for i in range(len(filtro_array)):
        conv1.append(list(reversed(filtro_array[i])))

    conv2 = list(reversed(conv1))
    print(conv2)

    m = len(conv2)
    n = len(conv2[0])

    if m >= 1 and n >= 1:
        pivo_i = int(m % 2 == 0)
        pivo_j = int(n % 2 == 0)
        limite_i = m//2
        limite_j = n//2
        dummy_img_array = np.zeros((len(img_array) - (2 * limite_i) + pivo_i, len(img_array[0]) - (2 * limite_j) + pivo_j, 3), dtype = int)
        x = 0
        for i in range(limite_i - pivo_i, len(img_array) - limite_i): # s/ extensao
            y = 0
            for j in range(limite_j - pivo_j, len(img_array[0]) - limite_j):
                pixel = [0, 0, 0]
                xm = 0
                for k in range(i - limite_i + pivo_i, i + limite_i + 1):
                    ym = 0
                    for l in range(j - limite_j + pivo_j, j + limite_j + 1):
                        pixel[0] += img_array[k][l][0] * conv2[xm][ym]
                        pixel[1] += img_array[k][l][1] * conv2[xm][ym]
                        pixel[2] += img_array[k][l][2] * conv2[xm][ym]
                        ym += 1
                    xm += 1

                for k in range(3):
                        if pixel[k] > 255: # verificar limites
                            pixel[k] = 255
                        elif pixel[k] < 0:
                            pixel[k] = 0

                dummy_img_array[x][y] = pixel
                y += 1
            x += 1
    
        return Image.fromarray(np.uint8(dummy_img_array), mode = "RGB") # retorna a imagem transformada


if __name__ == "__main__":
    main()
