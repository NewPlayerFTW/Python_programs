__author__ = 'student'
import random

class Matrix_engine:
    def __init__(self):
        self.matrix_list = [];

    def add_matrix(self, lines, columns):
        matrix = []
        for i in range(lines):
            line = [random.randint(1, 100) for r in range(columns)]
            matrix.append(line)
        self.matrix_list.append(matrix)


    def display_matrix(self, number):
        size = self.matrix_size(self.matrix_list[number])
        for i in range(size[0]):
            print self.matrix_list[number][i]

    def transposition(self, number):
        size = self.matrix_size(self.matrix_list[number])
        result_matrix = self.create_empty_matrix(size[1], size[0])

        for i in range(size[0]):
            for j in range(size[1]):
                result_matrix[j][i] = self.matrix_list[number][i][j]
        self.matrix_list[number] = result_matrix

    def multiplication(self, number1, number2):
        matrix1_size = self.matrix_size(self.matrix_list[number1])
        matrix2_size = self.matrix_size(self.matrix_list[number2])
        if matrix1_size[0] == matrix2_size[1]:
            result_matrix = self.create_empty_matrix(matrix1_size[0], matrix2_size[1])
            for i in range(matrix1_size[0]):
                for j in range(matrix2_size[1]):
                    for k in range(matrix1_size[1]):
                        result_matrix[i][j] += self.matrix_list[number1][i][k] * self.matrix_list[number2][k][j]
            self.matrix_list.append(result_matrix)

    def matrix_inversion(self, number):
        #matrix = [[3, -2], [1, 3]] # RESULT: [[3, 2][-1, 3]]
        matrix = [[2, -1, 2], [-1, 3, 0], [1, 2, 3]] #RESULT: [[9, 3, -5],[7, 4, -5], [-6, -2, 5]]
        #matrix = [[3, 3, -4, -3],[0, 6, 1, 1], [5, 4, 2, 1], [2, 3, 3, 2]]
        #matrix = self.matrix_list[number]
        size = self.matrix_size(matrix)
        if size[0] is not size[1]:
            return None

        identity = self.create_identity_matrix(size[0])
        print matrix
        for i in range(size[0]):
            divider = float(matrix[i][i])
            for j in range(size[0]):
                matrix[i][j] /= divider #dzielenie wiersza przez [i][i] element
                identity[i][j] /= divider

            #ten wiersz pomnozony przez wiersze pod/nad nim odejmujemy od wszystkich innych wierszy
            for j in range(size[0]):
                if i is not j:
                    mult = matrix[j][i]
                    for k in range(size[0]):
                        matrix[j][k] -= matrix[i][k] * mult
                        identity[j][k] -= identity[i][k] * mult
        print identity

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
m.add_matrix(5, 5)
m.matrix_inversion(0)

# klasa z lista macierzy
# mnozenie macierzy (3 indeksy)
# transponowanie macierzy       ok
# odwracanie macierzy
# wypisz                        ok
# zaloz macierz                 ok
# losuj macierz                 ok