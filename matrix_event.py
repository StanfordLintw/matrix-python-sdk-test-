from random import random

class MatrixEvent:

    Id = None
    Prev = None
    Next = None

    Content = ""
    ContentData = None

    def __init__(self):
        self.Id = random() * 1000000000000000
