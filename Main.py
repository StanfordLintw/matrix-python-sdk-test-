import json

from matrix_client import MatrixClinet
from http_client import HttpClient

class Main:

    matrix_client = None

    def run(self):
        self.matrix_client = MatrixClinet()
        self.matrix_client.Login("test", "12345")
        self.matrix_client.Sync()
        print("AAAAA")

if __name__ == '__main__':
    main = Main()
    main.run()
