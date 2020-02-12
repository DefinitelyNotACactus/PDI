from PIL import Image
import numpy as np
import sys

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
