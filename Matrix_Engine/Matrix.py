from __future__ import print_function
import random

class Matrix_engine:
    def __init__(self):
        self.matrix_list = [];

    def add(self, lines, columns):
        matrix = []
        for i in range(lines):
            line = [random.randint(1, 9) for r in range(columns)]
            matrix.append(line)
        self.matrix_list.append(matrix)


    def display(self, number):
        size = self.matrix_size(self.matrix_list[number])
        for i in range(size[0]):
            print('|', end='')
            for j in range(size[1]):
                print("%.2f" % self.matrix_list[number][i][j], end=' ')
            print('|')
        print

    def transposition(self, number):
        size = self.matrix_size(self.matrix_list[number])
        result_matrix = self.create_empty_matrix(size[1], size[0])

        for i in range(size[0]):
            for j in range(size[1]):
                result_matrix[j][i] = self.matrix_list[number][i][j]
        self.matrix_list[number] = result_matrix

    def mult(self, number1, number2):
        matrix1_size = self.matrix_size(self.matrix_list[number1])
        matrix2_size = self.matrix_size(self.matrix_list[number2])
        if matrix1_size[0] == matrix2_size[1]:
            result_matrix = self.create_empty_matrix(matrix1_size[0], matrix2_size[1])
            for i in range(matrix1_size[0]):
                for j in range(matrix2_size[1]):
                    for k in range(matrix1_size[1]):
                        result_matrix[i][j] += self.matrix_list[number1][i][k] * self.matrix_list[number2][k][j]
            self.matrix_list.append(result_matrix)

    def inversion(self, number):
        matrix = self.matrix_list[number]
        size = self.matrix_size(matrix)
        if size[0] is not size[1]:
            return None

        identity = self.create_identity_matrix(size[0])
        for i in range(size[0]):
            divider = float(matrix[i][i])
            for j in range(size[0]):
                matrix[i][j] /= divider
                identity[i][j] /= divider

            for j in range(size[0]):
                if i is not j:
                    mult = matrix[j][i]
                    for k in range(size[0]):
                        matrix[j][k] -= matrix[i][k] * mult
                        identity[j][k] -= identity[i][k] * mult

    # ADDITIONAL FUNCTIONS
    def matrix_size(self, matrix):
        return len(matrix), len(matrix[0])

    def create_empty_matrix(self, lines, columns):
        result_matrix = []
        for i in range(lines):
            result_matrix.append([0] * columns)
        return result_matrix

    def create_identity_matrix(self, size):
        result_matrix = []
        for i in range(size):
            result_matrix.append([0] * size)
            for j in range(size):
                if i is j:
                    result_matrix[i][j] = 1
        return result_matrix

m = Matrix_engine()
m.add(10, 10)
m.display(0)

# klasa z lista macierzy
# mnozenie macierzy (3 indeksy)
# transponowanie macierzy       ok
# odwracanie macierzy
# wypisz                        ok
# zaloz macierz                 ok
# losuj macierz                 ok