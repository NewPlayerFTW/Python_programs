from __future__ import print_function
from threading import Thread
import random
import time

class Matrix_engine:
    def __init__(self, threads_amount):
        self.matrix_list = []
        self.threads_amount = threads_amount

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

    def mult(self, number_1, number_2):
        matrix_1 = self.matrix_list[number_1]
        matrix_2 = self.matrix_list[number_2]
        size_1 = self.matrix_size(matrix_1)
        size_2 = self.matrix_size(matrix_2)
        if size_1[1] == size_2[0]:
            result_matrix = self.create_empty_matrix(size_1[0], size_2[1])
            self.matrix_list.append(result_matrix)
            threads = []
            for i in range(self.threads_amount):
                threads.append(Thread(target=self.mult_index, args=(matrix_1, matrix_2, size_1, size_2, i)))
            for i in range(self.threads_amount):
                threads[i].start()
                #threads[i].join()


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

    #THREADS FUNCTIONS
    def mult_index(self, source_1, source_2, size_1, size_2, start):
        result_matrix = self.matrix_list[len(self.matrix_list) - 1]
        line = start
        index = [line, 0]
        while line < size_1[0]:
            for i in range(size_1[0]):
                for j in range(size_2[1]):
                    result_matrix[line][i] += source_1[line][j] * source_2[j][i]
                    #print("thread", start, "working")
            line += self.threads_amount


start = time.time()

m = Matrix_engine(4)
m.add(10, 10)
m.add(10, 10)
m.mult(0, 1)
#m.display(2)

end = time.time()
print (end - start)
# klasa z lista macierzy
# mnozenie macierzy (3 indeksy)
# transponowanie macierzy       ok
# odwracanie macierzy
# wypisz                        ok
# zaloz macierz                 ok
# losuj macierz                 ok