#Biblioteca para plotar os gráficos
import matplotlib.pyplot as plt
#Operações com as matrizes
import numpy as np
import matplotlib.gridspec as gridspec

import math
import random 
   

def funcao_produz_fragmento(intMINCor, intMAXCor, matriz, resolucaoX, resolucaoY, x, y):
    xm = math.floor(x) 
    ym = math.floor(y) 

    if (x >= resolucaoX):
        xm = int(math.floor(x)) - 1 
    if (y >= resolucaoY):
        ym = int(math.floor(y)) - 1 

        
    matriz[ym,xm] = random.randint(intMINCor,intMAXCor)

def algoritmo_rasterização_de_retas(intMINCor, intMAXCor, matriz, resolucao_x, resolucao_y, x1, y1, x2, y2):

    # Conversão das coordenadas no SRN (0 - 1) para o SRD
    coordenada_de_origem_x_SRD = x1 * resolucao_x 
    coordenada_de_origem_y_SRD = y1 * resolucao_y 

    coordenada_de_destino_x_SRD = x2 * resolucao_x 
    coordenada_de_destino_y_SRD = y2 * resolucao_y 

    # Cálculo do Δx e Δy apartir das coordenadas no SRD
    deltaX = coordenada_de_destino_x_SRD - coordenada_de_origem_x_SRD 
    deltaY = coordenada_de_destino_y_SRD - coordenada_de_origem_y_SRD 

    # Chamada da função responsável pela construção dos fragmentos da reta rasterizada no SRD
    funcao_produz_fragmento(intMINCor, intMAXCor , matriz, resolucao_x, resolucao_y, coordenada_de_origem_x_SRD, coordenada_de_origem_y_SRD)

    if (abs(deltaX) > abs(deltaY)): # Trabalha o caso em que Δx > Δy
        if coordenada_de_origem_x_SRD < coordenada_de_destino_x_SRD:

            while coordenada_de_origem_x_SRD < coordenada_de_destino_x_SRD:

                if deltaY == 0:
                    """
                    *********************************************
                    * Para o caso de Δy = 0 podemos concluir que:
                    *********************************************
                    *   1- m = 0.
                    *   2- b = coordenada_de_origem_y_SRD.
                    *********************************************
                    """

                    coordenada_de_origem_x_SRD = coordenada_de_origem_x_SRD + 1.0

                else:
                    m = deltaY/deltaX 
                    b = coordenada_de_origem_y_SRD - (m*coordenada_de_origem_x_SRD) 

                    coordenada_de_origem_x_SRD = coordenada_de_origem_x_SRD + 1.0 
                    coordenada_de_origem_y_SRD = (m*coordenada_de_origem_x_SRD) + b 

                funcao_produz_fragmento(intMINCor, intMAXCor, matriz, resolucao_x, resolucao_y, coordenada_de_origem_x_SRD, coordenada_de_origem_y_SRD)
    elif (abs(deltaY) > abs(deltaX)): # Trabalha o caso em que Δy > Δx 

        if coordenada_de_origem_y_SRD < coordenada_de_destino_y_SRD:

            while coordenada_de_origem_y_SRD < (coordenada_de_destino_y_SRD - 1.0):

                if deltaX == 0:
                    """
                    *********************************************
                    * Para o caso de Δy = 0 podemos concluir que:
                    ******************************************************************
                    *   1- m = None (Pois qualquer valor dividido por 0 é indefinido).
                    *   2- b = coordenada_de_origem_y_SRD.
                    ******************************************************************
                    """

                    coordenada_de_origem_y_SRD = coordenada_de_origem_y_SRD + 1.0

                else:
                    m = deltaY/deltaX
                    b = coordenada_de_origem_y_SRD - (m*coordenada_de_origem_x_SRD)

                    coordenada_de_origem_y_SRD = coordenada_de_origem_y_SRD + 1.0
                    coordenada_de_origem_x_SRD = (coordenada_de_origem_y_SRD - b)/m

                funcao_produz_fragmento(intMINCor, intMAXCor, matriz, resolucao_x, resolucao_y, coordenada_de_origem_x_SRD, coordenada_de_origem_y_SRD)

        elif coordenada_de_origem_y_SRD > coordenada_de_destino_y_SRD:

            while coordenada_de_origem_y_SRD > coordenada_de_destino_y_SRD:

                if deltaX == 0:
                    """
                    *********************************************
                    * Para o caso de Δy = 0 podemos concluir que:
                    ******************************************************************
                    *   1- m = None (Pois qualquer valor dividido por 0 é indefinido).
                    *   2- b = coordenada_de_origem_y_SRD.
                    ******************************************************************
                    """

                    coordenada_de_origem_y_SRD = coordenada_de_origem_y_SRD - 1.0

                else:
                    m = deltaY/deltaX                
                    b = coordenada_de_origem_y_SRD - (m*coordenada_de_origem_x_SRD)

                    coordenada_de_origem_y_SRD = coordenada_de_origem_y_SRD - 1.0
                    coordenada_de_origem_x_SRD = (coordenada_de_origem_y_SRD - b)/m

                funcao_produz_fragmento(intMINCor, intMAXCor, matriz, resolucao_x, resolucao_y, coordenada_de_origem_x_SRD, coordenada_de_origem_y_SRD)
    elif (abs(deltaY) == abs(deltaX)): # Trabalha o caso em que Δx = Δy

        if (coordenada_de_origem_x_SRD > coordenada_de_destino_x_SRD) and (coordenada_de_origem_y_SRD < coordenada_de_destino_y_SRD):

            while (coordenada_de_origem_x_SRD > coordenada_de_destino_x_SRD) and (coordenada_de_origem_y_SRD < coordenada_de_destino_y_SRD):

                if deltaX == 0 and deltaY == 0:
                    """
                    *********************************************
                    * Para o caso de Δy = 0 podemos concluir que:
                    ******************************************************************
                    *   1- m = None (Pois qualquer valor dividido por 0 é indefinido).
                    *   2- b = coordenada_de_origem_y_SRD.
                    ******************************************************************
                    """

                    coordenada_de_origem_x_SRD = coordenada_de_origem_x_SRD
                    coordenada_de_origem_y_SRD = coordenada_de_origem_y_SRD

                else:
                    m = 1 #Pois ambos os valores de Δx e Δy são iguais nesse caso.
                    b = coordenada_de_origem_y_SRD - coordenada_de_origem_x_SRD

                    coordenada_de_origem_x_SRD = coordenada_de_origem_x_SRD - 1.0
                    coordenada_de_origem_y_SRD = coordenada_de_origem_y_SRD + 1.0 

                funcao_produz_fragmento(intMINCor, intMINCor, matriz, resolucao_x, resolucao_y, coordenada_de_origem_x_SRD, coordenada_de_origem_y_SRD)

        elif (coordenada_de_origem_x_SRD < coordenada_de_destino_x_SRD) and (coordenada_de_origem_y_SRD > coordenada_de_destino_y_SRD):

            while (coordenada_de_origem_x_SRD < coordenada_de_destino_x_SRD) and (coordenada_de_origem_y_SRD > coordenada_de_destino_y_SRD):

                if deltaX == 0 and deltaY == 0:
                    """
                    *********************************************
                    * Para o caso de Δy = 0 podemos concluir que:
                    ******************************************************************
                    *   1- m = None (Pois qualquer valor dividido por 0 é indefinido).
                    *   2- b = coordenada_de_origem_y_SRD.
                    ******************************************************************
                    """

                    coordenada_de_origem_x_SRD = coordenada_de_origem_x_SRD
                    coordenada_de_origem_y_SRD = coordenada_de_origem_y_SRD

                else:
                    m = 1 #Pois ambos os valores de Δx e Δy são iguais nesse caso.
                    b = coordenada_de_origem_y_SRD - coordenada_de_origem_x_SRD

                    coordenada_de_origem_x_SRD = coordenada_de_origem_x_SRD + 1.0
                    coordenada_de_origem_y_SRD = coordenada_de_origem_y_SRD - 1.0

                funcao_produz_fragmento(intMINCor, intMAXCor, matriz, resolucao_x, resolucao_y, coordenada_de_origem_x_SRD, coordenada_de_origem_y_SRD)

        elif (coordenada_de_origem_x_SRD > coordenada_de_destino_x_SRD) and (coordenada_de_origem_y_SRD > coordenada_de_destino_y_SRD):

            while (coordenada_de_origem_x_SRD > coordenada_de_destino_x_SRD) and (coordenada_de_origem_y_SRD > coordenada_de_destino_y_SRD):

                if deltaX == 0 and deltaY == 0:
                    """
                    *********************************************
                    * Para o caso de Δy = 0 podemos concluir que:
                    ******************************************************************
                    *   1- m = None (Pois qualquer valor dividido por 0 é indefinido).
                    *   2- b = coordenada_de_origem_y_SRD.
                    ******************************************************************
                    """

                    coordenada_de_origem_x_SRD = coordenada_de_origem_x_SRD
                    coordenada_de_origem_y_SRD = coordenada_de_origem_y_SRD

                else:
                    m = 1 #Pois ambos os valores de Δx e Δy são iguais nesse caso.
                    b = coordenada_de_origem_y_SRD - coordenada_de_origem_x_SRD

                    coordenada_de_origem_x_SRD = coordenada_de_origem_x_SRD - 1.0
                    coordenada_de_origem_y_SRD = coordenada_de_origem_y_SRD - 1.0

                funcao_produz_fragmento(intMINCor, intMAXCor, matriz, resolucao_x, resolucao_y, coordenada_de_origem_x_SRD, coordenada_de_origem_y_SRD)

        elif (coordenada_de_origem_x_SRD < coordenada_de_destino_x_SRD) and (coordenada_de_origem_y_SRD < coordenada_de_destino_y_SRD):

            while (coordenada_de_origem_x_SRD < coordenada_de_destino_x_SRD) and (coordenada_de_origem_y_SRD < coordenada_de_destino_y_SRD):

                if deltaX == 0 and deltaY == 0:
                    """
                    *********************************************
                    * Para o caso de Δy = 0 podemos concluir que:
                    ******************************************************************
                    *   1- m = None (Pois qualquer valor dividido por 0 é indefinido).
                    *   2- b = coordenada_de_origem_y_SRD.
                    ******************************************************************
                    """

                    coordenada_de_origem_x_SRD = coordenada_de_origem_x_SRD
                    coordenada_de_origem_y_SRD = coordenada_de_origem_y_SRD

                else:
                    m = 1 #Pois ambos os valores de Δx e Δy são iguais nesse caso.
                    b = coordenada_de_origem_y_SRD - coordenada_de_origem_x_SRD

                    coordenada_de_origem_x_SRD = coordenada_de_origem_x_SRD + 1.0
                    coordenada_de_origem_y_SRD = coordenada_de_origem_y_SRD + 1.0

                funcao_produz_fragmento(intMINCor, intMAXCor, matriz, resolucao_x, resolucao_y, coordenada_de_origem_x_SRD, coordenada_de_origem_y_SRD)


def teste():
    fig, axs = plt.subplots(1, 1, squeeze=False)
    fig.suptitle('[Quadro Comparativo - Diferentes Resoluções entre um Ponto e Retas Rasterizadas de Tamanho Mínimo(=1)] - No SRD', y=0.99, fontsize=7, fontweight="bold")
    fig.canvas.manager.set_window_title('Diferentes Resoluções entre um Ponto e Retas Rasterizadas de Tamanho Mínimo(=1)')
    gs1 = gridspec.GridSpec(1, 1) #verifica os valores dentro da matriz

    resolucao_x = 1920
    resolucao_y = 1080

    #Preenche toda a matriz com uma cor variando de 0 a 1 RGB
    matriz_de_entrada = np.random.randint(0,25,(resolucao_y,resolucao_x)) 

    coordenada_x1_SRN = 0.0
    coordenada_y1_SRN = 0.0

    coordenada_x2_SRN = 0.6
    coordenada_y2_SRN = 0.8


    algoritmo_rasterização_de_retas(151,180,matriz_de_entrada,resolucao_x,resolucao_y,coordenada_x1_SRN,coordenada_y1_SRN,coordenada_x2_SRN,coordenada_y2_SRN)

    axs[0,0].imshow(matriz_de_entrada, #(M, N): an image with scalar data. The values are mapped to colors using normalization and a colormap. See parameters norm, cmap, vmin, vmax.
                    interpolation='nearest', #'nearest' interpolation is used if the image is upsampled by more than a factor of three (i.e. the number of display pixels is at least three times the size of the data array).
                    aspect='equal', #'equal': Ensures an aspect ratio of 1. Pixels will be square (unless pixel sizes are explicitly made non-square in data coordinates using extent).
                    origin='lower', #Place the [0, 0] index of the array in the upper left or lower left corner of the Axes. The convention (the default) 'upper' is typically used for matrices and images. Note that the vertical axis points upward for 'lower' but downward for 'upper'.
                    cmap='viridis') #gist_stern #gist_ncar #Padrão de cor 
    
    axs[0,0].set_title('Resolução ' + str(resolucao_x) + ' x ' + str(resolucao_y) + ' - ' + str(resolucao_x*resolucao_y) + ' pixels - '+
                        "Ponto: ("+str(coordenada_x1_SRN*resolucao_x)+","+str(coordenada_y1_SRN*resolucao_y)+")",fontsize=6)
    plt.show()

teste()
