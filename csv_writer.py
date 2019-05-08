import csv


class CSVWriter():
    def __init__(self, filename):
        self.file = open(filename, mode='w')
        self.writer = csv.writer(self.file, delimiter=',', quotechar='"',
                                 quoting=csv.QUOTE_MINIMAL)

    def write(self, *args):
        self.writer.writerow(args)

    def close():
        pass
