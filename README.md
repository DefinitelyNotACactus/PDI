# PDI
Trabalhos da disciplina de introdução ao processamento digital de imagens

## Dependências
```
$pip3 install pillow
$pip3 install numpy
$pip3 install scipy
$pip3 install seaborn
```

## Primeiro Trabalho

Introdução ao Processamento Digital de Imagens 

Módulo 1 do Trabalho Prático

Data de entrega: 09/12/2019

 

Desenvolva um sistema para abrir, exibir, manipular e salvar imagens RGB com 24 bits/pixel (8 bits/componente/pixel). O sistema deve ter a seguinte funcionalidade:

 

1 Conversão RGB-YIQ-RGB (cuidado com os limites de R, G e B na volta!)

2 Exibição de bandas individuais (R, G e B) como imagens monocromáticas ou coloridas (em tons de R, G ou B, respectivamente)

3 Negativo 

4 Controle de brilho multiplicativo (s = r.c, c real não negativo) (cuidado com os limites de R, G e B)

5 Convolução m x n com máscara especificada pelo usuário em arquivo texto. Testar com filtros Média e Sobel.

6 Filtro mediana e moda m x n.

 

O sistema deve ser desenvolvido em uma linguagem de programação de sua escolha. Não use bibliotecas ou funções dedicadas de processamento de imagens para desenvolver os tópicos contemplados nos itens 1 a 6. Para os itens 3 e 4, duas formas de aplicação devem ser testadas: em RGB (banda a banda) e na banda Y, com posterior conversão para RGB. 

 

Observações:

 

1.O trabalho pode ser feito em grupo, com até cinco componentes. 

2.Para integralização das notas, o trabalho deve ser apresentado na data e horário marcados, juntamente com um relatório impresso, contendo pelo menos as seguintes seções: introdução (contextualização e apresentação do tema, fundamentação teórica, objetivos), materiais e métodos (descrição das atividades desenvolvidas e das ferramentas e conhecimentos utilizados) resultados, discussão (problemas e dificuldades encontradas, comentários críticos sobre os resultados) e conclusão. Cada componente do grupo deve estar familiarizado com o trabalho desenvolvido pelos demais componentes do seu grupo, e todos devem comparecer à apresentação dos trabalhos.

## Segundo Trabalho

Neste trabalho, a rotação e a DCT (direta e inversa) devem ser desenvolvidas utilizando as equações estudadas em sala de aula, sem o uso de bibliotecas prontas para esse fim.
Dada uma imagem I em níveis de cinza, de dimensões RxC, desenvolva um programa para
1. Rotacionar I por um ângulo especificado (parâmetro entre 0 e 360 graus), utilizando (a) mapeamento direto; (b) mapeamento reverso com interpolação bilinear. A imagem rotacionada deve preservar todo o conteúdo da imagem original.
2. Exibir o módulo da DCT de I, sem o nível DC, e o valor do nível DC
3. Encontrar e exibir uma aproximação de I obtida preservando o coeficiente DC e os n coeficientes AC mais importantes de I, e zerando os demais. O parâmetro n é um inteiro no intervalo [0, RxC-1].
4. Encontrar a imagem resultante da filtragem de I por um filtro passa-baixas ideal quadrado, com frequência de corte fc (parâmetro especificado pelo usuário) igual à aresta do quadrado, em pixels.
  Entrega: 18/03/2020 
