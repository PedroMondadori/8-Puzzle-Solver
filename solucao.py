# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Descrição : Script que implementa diversos algoritmos de busca em grafos
# Autor     : Pedro Lago Mondadori, Bruno Corrêa
# Data      : 17/08/2021
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


import queue
import time
from dataclasses import dataclass, field
from typing import Any

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Estruturas de dados
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


class Nodo():
    def __init__(self, estado, pai, acao, custo):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

    def __str__(self):
        return f"Estado: {self.estado} | Ação: {self.acao} | Custo: {self.custo}"

    def __repr__(self):
        return self.__str__()


class Stack():
    def __init__(self):
        self.stack = []

    def put(self, item):
        self.stack.append(item)

    def get(self):
        return self.stack.pop()

    def empty(self):
        return self.stack == []


class HammingPriorityQueue():
    def __init__(self):
        self.queue = queue.PriorityQueue()

    def put(self, item):
        self.queue.put(PrioritizedItem(
            self.misplaced_pieces(item.estado) + item.custo, item))

    def get(self):
        return self.queue.get().item

    def empty(self):
        return self.queue.empty()

    def misplaced_pieces(self, estado):
        n = 0
        for i in range(9):
            if estado[i] != '_' and int(estado[i]) != i+1:
                n = n + 1
        return n


class ManhattanPriorityQueue():
    def __init__(self):
        self.queue = queue.PriorityQueue()

    def put(self, item):
        self.queue.put(PrioritizedItem(
            self.manhattan_distance_heuristic(item.estado) + item.custo, item))

    def get(self):
        return self.queue.get().item

    def empty(self):
        return self.queue.empty()

    def manhattan_distance(self, board, i):
        if board[i] == '_':
            return 0

        x_goal = (int(board[i])-1) % 3
        y_goal = (int(board[i])-1) // 3
        x_value = i % 3
        y_value = i//3
        return abs(x_value - x_goal) + abs(y_value - y_goal)

    def manhattan_distance_heuristic(self, estado):
        sum = 0
        board = estado
        for i in range(9):
            sum = sum + self.manhattan_distance(board, i)
        return sum


class explored_set(set):
    def append(self, item):
        self.add(item)
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Implementação
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Descrição : Printa o tabuleiro no terminal
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def print_board(board):
    print('')
    for i in range(9):
        print(board[i], end=" ")
        if (i+1) % 3 == 0:
            print('')
    print('')

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Descrição : Printa o caminho no terminal
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def print_caminho(caminho):
    for acao in caminho:
        print(str(acao) + ', ', end="")

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Descrição : Dado um estado do tabuleiro retorna todos os possíveis estados
#             alcançáveis a partir dele
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def sucessor(estado):
    moves = ["esquerda", "direita", "acima", "abaixo"]
    pos = estado.find('_')
    successors = []

    for move in moves:

        if (move == "esquerda") and (pos not in (0, 3, 6)):
            aux = estado[pos-1]
            aux_board = estado.replace("_", "x")
            aux_board = aux_board.replace(aux, "_")
            aux_board = aux_board.replace("x", aux)
            successors.append((move, aux_board))
        if (move == "direita") and (pos not in (2, 5, 8)):
            aux = estado[pos+1]
            aux_board = estado.replace("_", "x")
            aux_board = aux_board.replace(aux, "_")
            aux_board = aux_board.replace("x", aux)
            successors.append((move, aux_board))
        if (move == "acima") and (pos > 2):
            aux = estado[pos-3]
            aux_board = estado.replace("_", "x")
            aux_board = aux_board.replace(aux, "_")
            aux_board = aux_board.replace("x", aux)
            successors.append((move, aux_board))
        if (move == "abaixo") and (pos < 6):
            aux = estado[pos+3]
            aux_board = estado.replace("_", "x")
            aux_board = aux_board.replace(aux, "_")
            aux_board = aux_board.replace("x", aux)
            successors.append((move, aux_board))

    return successors

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Descrição : Calcula os sucessores de um nodo e os retorna
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def expande(node):
    successors = sucessor(node.estado)
    return_nodes = []
    for succ in successors:
        new_node = Nodo(succ[1], node, succ[0], node.custo + 1)
        return_nodes.append(new_node)
    return return_nodes

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Descrição : Retorna o caminho feito no grafo para chegar até o nodo a partir
#             da origem
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def caminho(node):
    if node.pai == None:
        return None
    caminho = [node.acao]
    while node.pai is not None:
        node = node.pai
        if node.acao != None:
            caminho.append(node.acao)

    caminho.reverse()
    return caminho

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Descrição : Determina se o estado é resolvível
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def isSolvable(arr):
    inv_count = 0
    for i in range(9):
        for j in range(i + 1, 9):
            if (arr[j] != '_' and arr[i] < arr[j]):
                inv_count += 1
    return inv_count % 2 == 0

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Descrição : Algoritmo genérico de busca em grafo
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def busca_grafo(estado, frontier_data_structure, explored_data_structure):
    t_start = time.time()
    explored = explored_data_structure()
    nodes_explored = 0
    frontier = frontier_data_structure()
    frontier.put(Nodo(estado, None, None, 0))

    if not isSolvable(estado):
        return None

    while True:
        if frontier.empty():
            return None
        node = frontier.get()
        # print(node.estado)
        if node.estado == "12345678_":
            #print(f'Nodos explorados: {nodes_explored}, tempo: {time.time() - t_start}')
            return caminho(node)
        if node.estado not in explored:
            explored.append(node.estado)
            vizinhos = expande(node)
            nodes_explored += 1
            for vizinho in vizinhos:
                frontier.put(vizinho)

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Descrição : busca em largura
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def bfs(estado):
    return busca_grafo(estado, queue.Queue, explored_set)

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Descrição : busca em profundidade
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def dfs(estado):
    return busca_grafo(estado, Stack, explored_set)

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Descrição : busca A* utilizando a heurística de Hamming
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def astar_hamming(estado):
    return busca_grafo(estado, HammingPriorityQueue, list)

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Descrição : busca A* utilizando a heurística de distância Manhattan
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def astar_manhattan(estado):
    return busca_grafo(estado, ManhattanPriorityQueue, list)


def execute_all_algs():
    algs = [(bfs, "BFS"),
            (dfs, "DFS"),
            (astar_manhattan, "A*M"),
            (astar_hamming, "A*H")]
    states = ['4365_1278', '1234567_8', '12345678_']
    for state in states:
        #print(f"========== '{state}' ==========")
        for alg in algs:
            print(f'{alg[1]}: ', end="")
            alg[0](state)
    import time
    start_time = time.time()
    # astar_hamming('8_6547231')
    print("--- %s seconds ---" % (time.time() - start_time))


execute_all_algs()

#print(expande(Nodo("2_3541687", None, None, 0)))
