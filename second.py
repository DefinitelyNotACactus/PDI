from PIL import Image
import numpy as np
import seaborn as sns
import sys
import util # leitura e escrita de imagens
import dct # implementacao da dct
import math
import time

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
            img = util.escolherImagem().convert('L') # Converter pra monocromatico, caso não seja
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
                
                if op2 == 1 or op2 == 2:
                    print("Trabalhando...")
                    start = time.time()
                    img2 = (rotacaoMapeamentoDireto(img_array, theta) if op2 == 1 else rotacaoMapeamentoReverso(img_array, theta))
                    end = time.time()
                    print("Concluído! (Operação realizada em %.2f segundos)" % (end - start))
                    manipulacao = True

        elif op == 2: #dct
            print("Trabalhando...")
            start = time.time()
            dc, img2 = moduloDCT(img_array) # imagem monocromatica
            end = time.time()
            print("Concluído! (Operação realizada em %.2f segundos)" % (end - start))
            print("Nível DC:", dc)
            manipulacao = True
            
        elif op == 3: # aproximacao usando n coeficientes + dc
            #try:
            n = int(input("Insira o número de coeficientes mais importantes que se deseja utilizar (n):\nn = "))
            print("Trabalhando...")
            start = time.time()
            img2 = aproximacaoImagem(img_array, n = n) # imagem monocromatica
            end = time.time()
            print("Concluído! (Operação realizada em %.2f segundos)" % (end - start))
            manipulacao = True
            #except:
                #print("Insira um valor válido para n!")
            
        elif op == 4: # filtro passa-baixas
            try:
                fc = int(input("Insira o valor da frequência de corte (fc):\nfc = "))
                print("Trabalhando...")
                start = time.time()
                img2 = passaBaixas(img_array, fc = fc) # imagem monocromatica
                end = time.time()
                print("Concluído! (Operação realizada em %.2f segundos)" % (end - start))
                manipulacao = True
            except:
                print("Insira um valor válido para fc!")
                
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
    print("r: " + str(r) + " c: " + str(c))

    dummy_img_array = np.zeros((r + 1, c + 1, 3), dtype = int)
    for i in range(len(img_array)):
        for j in range(len(img_array[0])):
            dummy_img_array[map[i][j][0] + abs(upper_bound)][map[i][j][1] + abs(left_bound)] = img_array[i][j].copy()
    
    return Image.fromarray(np.uint8(dummy_img_array), mode = "RGB") # retorna a imagem transformada

def rotacaoMapeamentoReverso(img_array, theta = 0):
    theta = math.radians(theta)
    width = len(img_array[0])
    height = len(img_array)
    diagonal = math.ceil(math.sqrt(width ** 2 + height ** 2))
    # Centro da imagem
    centerX = int(width / 2)
    centerY = int(height / 2)
    centerDest = diagonal / 2 # Centro da imagem de destino
    dummy_img_array = np.zeros((diagonal, diagonal))
    pi = math.pi
    for i in range(diagonal):
        for j in range(diagonal):
            # Converter os indices para coordenadas cartesianas
            x = j - centerDest
            y = centerDest - i
            # Converter cartesiano para polar
            distance = math.sqrt(x ** 2 + y ** 2) # raio
            polarAngle = 0
            if x == 0:
                if y == 0: # Centro da imagem, não precisa rotacionar
                    dummy_img_array[i][j] = img_array[centerY][centerX]
                    continue
                elif y < 0:
                    polarAngle = 1.5 * pi
                else:
                    polarAngle = 0.5 * pi
            else:
                polarAngle = math.atan2(y, x)
            # Rotação reversa
            polarAngle -= theta
            # Converter polar para cartesiano
            trueX = distance * math.cos(polarAngle)
            trueY = distance * math.sin(polarAngle)
            trueX = trueX + centerX
            trueY = centerY - trueY
            # Cartesiano para os indices da matriz
            floorX = int(trueX // 1)
            floorY = int(trueY // 1)
            ceilX = int(math.ceil(trueX))
            ceilY = int(math.ceil(trueY))
            # Verificação de limites
            if floorX < 0 or ceilX < 0 or floorX >= width or ceilX >= width or floorY < 0 or ceilY < 0 or floorY >= height or ceilY >= height:
                continue
            deltaX = trueX - floorX
            deltaY = trueY - floorY
            # Vizinhança
            topLeft = img_array[floorY][floorX]
            topRight = img_array[floorY][ceilX]
            bottomLeft = img_array[ceilY][floorX]
            bottomRight = img_array[ceilY][ceilX]
            # Interpolação linear pela horizontal superior
            topColor = (1 - deltaX) * topLeft + deltaX * topRight
            # Interpolação linear pela horizontal inferior
            bottomColor = (1 - deltaX) * bottomLeft + deltaX * bottomRight
            # Interpolação linear pela vertical
            color = round((1 - deltaY) * topColor + deltaY * bottomColor)
            # Checagem de limites da cor
            if color < 0:
                color = 0
            elif color > 255:
                color = 255
            dummy_img_array[i][j] = color
    return Image.fromarray(np.uint8(dummy_img_array))

# Função para exibir o módulo da DCT de I, sem o nível DC, e o valor do nível DC
def moduloDCT(img_array):
    dct_array = dct.DCT2D(img_array)
    
    dc = dct_array[0][0]
    dct_array[0][0] = 0

    # Exibir o modulo da dct como mapa de calor
    heatMap = sns.heatmap(abs(dct_array))
    
    return dc, heatMap.get_figure()

# Função para encontrar e exibir uma aproximação de I obtida preservando o coeficiente DC e os n coeficientes AC mais importantes de I, e zerando os demais.
# O parâmetro n é um inteiro no intervalo [0, RxC-1].
def aproximacaoImagem(img_array, n = 0):
    if(n >= (len(img_array) * len(img_array[0])) or n < 0):
        return None # n fora do intervalo permitido!
    
    dct_array = dct.DCT2D(img_array)
    list_coeff = []
    dc = dct_array[0][0] # obtem dc
    if n > 0: # mais de um coeficiente a ser mantido
        for i in range(len(dct_array)):
            for j in range(len(dct_array[0])):
                if(i != 0 and j != 0): # Nao adicionar dc a lista de coeficientes
                    list_coeff.append({"abs(Value)": abs(dct_array[i][j]), "Value": dct_array[i][j], "i": i, "j": j})
        # Ordenar a lista de coeficientes pelo valor absoluto e pegar os n maiores coeficientes
        list_coeff_sorted = sorted(list_coeff, key = lambda x : x['abs(Value)'])
        top_coeffs = list_coeff_sorted[-n : ]
        dct_array.fill(0) # zerar o array
        for coeff in top_coeffs: # recolocar os maiores coeficientes no array
            dct_array[coeff['i']][coeff['j']] = coeff['Value']
    else: # manter apenas DC, zerar o resto
        dct_array.fill(0) # zerar o array
        
    dct_array[0][0] = dc
        
    dummy_img_array = dct.DCT2D(dct_array, inverse = True) # voltar pro dominio do espaco
    
    # garantir que os limites sejam preservados
    for i in range(len(dummy_img_array)):
        for j in range(len(dummy_img_array[0])):
            dummy_img_array[i][j] = round(dummy_img_array[i][j])
            if dummy_img_array[i][j] < 0:
                dummy_img_array[i][j] = 0
            elif dummy_img_array[i][j] > 255:
                dummy_img_array[i][j] = 255
                
    return Image.fromarray(np.uint8(dummy_img_array))

# Função para encontrar a imagem resultante da filtragem de I por um filtro passa-baixas ideal quadrado,
# com frequência de corte fc (parâmetro especificado pelo usuário) igual à aresta do quadrado, em pixels.
def passaBaixas(img_array, fc = 4):
    if fc > len(img_array) and fc > len(img_array[0]):
        return None # fc maior que o tamanho da imagem em R e C

    dct_array = dct.DCT2D(img_array) # converter a imagem pro dominio da frequencia
    # Realizar o corte
    if fc < len(img_array[0]):
        dct_array[ : , fc + 1 : ] = 0 # zerar tudo em cada coluna que esteja de fc + 1 a c - 1
    if fc < len(img_array):
        dct_array[fc + 1 : , : ] = 0 # zerar tudo em cada linha que esteja de fc + 1 a r - 1
    
    dummy_img_array = dct.DCT2D(dct_array, inverse = True) # voltar pro dominio do espaco
        
    # garantir que os valores fiquem nos limites
    for i in range(len(dummy_img_array)):
        for j in range(len(dummy_img_array[0])):
            dummy_img_array[i][j] = round(dummy_img_array[i][j])
            if dummy_img_array[i][j] < 0:
                dummy_img_array[i][j] = 0
            elif dummy_img_array[i][j] > 255:
                dummy_img_array[i][j] = 255
                
    return Image.fromarray(np.uint8(dummy_img_array))
    
if __name__ == "__main__":
    main()
