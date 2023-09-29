import numpy as np
import matplotlib.pyplot as plt

# Classe de configuração para cores e resoluções padrão
class Config:
    colors = {
        'azul': (0, 0, 255),
        'vermelho': (255, 0, 0),
        'amarelo': (255, 255, 0),
        'verde': (0, 255, 0),
        'branco': (255, 255, 255),
        'rosa': (255, 20, 147)
    }

    resolutions = [(100, 100), (300, 300), (600, 600), (600, 800), (1080, 1920)]

# Classe de matriz com funções para limpar e acessar
class Matriz:
    def __init__(self, resolutions):
        self.matriz = [np.zeros(res + (3,), dtype=np.uint8) for res in resolutions]

    def clear(self):
        self.matriz = [np.zeros(res + (3,), dtype=np.uint8) for res in self.matriz[0].shape[:2]]

    def get(self):
        return self.matriz

# Função para ajustar coordenadas para a resolução da matriz
def ajustar_res(x_antigo, y_antigo, l, a):
    x_novo = int(((l - 1) * (x_antigo + 1)) / 2)
    y_novo = int(((a - 1) * (y_antigo + 1)) / 2)
    return x_novo, y_novo

# Classe base para elementos gráficos
class ElementoGrafico:
    def __init__(self, pontos, color='branco'):
        self.pontos = pontos
        self.color = Config.colors[color]

# Classe de reta
class Reta(ElementoGrafico):
    def draw(self, matriz):
        for matriz_desenho in matriz:
            for i in range(len(self.pontos) - 1):
                x1, y1 = ajustar_res(*self.pontos[i], *matriz_desenho.shape[:2])
                x2, y2 = ajustar_res(*self.pontos[i + 1], *matriz_desenho.shape[:2])
                pontos_rasterizados = rasterizar(x1, y1, x2, y2)
                for p in pontos_rasterizados:
                    if 0 <= p[0] < matriz_desenho.shape[0] and 0 <= p[1] < matriz_desenho.shape[1]:
                        matriz_desenho[p[0], p[1]] = self.color

# Classe de polígono
class Poligono(ElementoGrafico):
    def draw(self, matriz):
        for matriz_desenho in matriz:
            for i in range(len(self.pontos)):
                x1, y1 = ajustar_res(*self.pontos[i], *matriz_desenho.shape[:2])
                x2, y2 = ajustar_res(*self.pontos[(i + 1) % len(self.pontos)], *matriz_desenho.shape[:2])
                pontos_rasterizados = rasterizar(x1, y1, x2, y2)
                for p in pontos_rasterizados:
                    if 0 <= p[0] < matriz_desenho.shape[0] and 0 <= p[1] < matriz_desenho.shape[1]:
                        matriz_desenho[p[0], p[1]] = self.color
            preenche_poligono(matriz_desenho, self.color)

# Função para rasterizar reta
def rasterizar(x1, y1, x2, y2):
    lista = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    if dy == 0:
        steps = dx or 1
    elif dx >= dy:
        steps = dx
    else:
        steps = dy

    x_inc = (x2 - x1) / steps
    y_inc = (y2 - y1) / steps

    x = x1
    y = y1

    for i in range(steps):
        xm, ym = produz_fragmento(x, y)
        lista.append((xm, ym))
        x += x_inc
        y += y_inc

    xm, ym = produz_fragmento(x2, y2)
    lista.append((xm, ym))

    return lista

# Função para produzir fragmento
def produz_fragmento(x, y):
    xm = round(x)
    ym = round(y)
    return xm, ym

# Função para preencher polígono
def preenche_poligono(matriz, cor):
    # lista para guardar as posições horizontais
    horizontal = []
    # ler a matriz horizontalmente e guardar as posições internas
    for i in range(matriz.shape[0]):
        dentro = False
        horizontalLinha = []
        counter = 0
        for j in range(matriz.shape[1]):
            if all(matriz[i][j] == cor):
                if all(matriz[i][min(matriz.shape[1] - 1, j + 1)] == [0, 0, 0]): 
                    counter += 1
                    dentro = not dentro
            elif dentro and (all(matriz[i][j] == cor) or (any(matriz[i][j] != [0, 0, 0]) and all(matriz[i][j] != cor) and all(matriz[i][j] != [255, 255, 255]))):
                # encontrou outra cor, continua procurando até achar a cor original novamente
                while j < matriz.shape[1] and (all(matriz[i][j] != cor) or (any(matriz[i][j] != [0, 0, 0]) and all(matriz[i][j] != cor) and all(matriz[i][j] != [255, 255, 255]))):
                    j += 1
                if j < matriz.shape[1]:
                    dentro = not dentro
            elif dentro:
                horizontalLinha.append((j, i))
        if counter == 1 or counter == 0:
            horizontalLinha.clear()
        else:
            for elemento in horizontalLinha:
                horizontal.append(elemento)

    # pintar os pontos internos na matriz
    for point in horizontal:
        matriz[point[1]][point[0]] = cor


# Classe de tela para gerenciar elementos gráficos

class Tela:
    def __init__(self):
        self.elementos = []

    def add_elemento(self, elemento):
        self.elementos.append(elemento)

    def remove_elemento(self):
        if self.elementos:
            self.elementos.pop()

    def draw_tela(self, matriz):
        for elemento in self.elementos:
            elemento.draw(matriz)

# Criação da matriz de desenho
matriz_desenho = Matriz(Config.resolutions)

# Criação da tela
tela = Tela()

# Exemplo de adição de elementos (retas e polígonos)
tela.add_elemento(Reta([(-0.8, -0.8), (-0.6, -0.8), (-0.6, -0.6), (-0.8, -0.6)], color='azul'))
tela.add_elemento(Poligono([(0.7, 0.7), (0.9, 0.7), (0.9, 0.9), (0.7, 0.9)], color='vermelho'))

# Limpa a matriz de desenho
matriz_desenho.clear()

# Desenha a tela
tela.draw_tela(matriz_desenho.get())

# Exibe a imagem resultante
for i, matriz in enumerate(matriz_desenho.get()):
    plt.subplot(2, 3, i + 1)
    plt.imshow(matriz)
    plt.title(f"{Config.resolutions[i][0]}x{Config.resolutions[i][1]}")
    plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()
