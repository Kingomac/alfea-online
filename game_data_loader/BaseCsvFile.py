import csv


class BaseCsvFile:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as f:
            self.__rows = tuple(csv.DictReader(f, delimiter=';'))

    @property
    def rows(self):
        return self.__rows
