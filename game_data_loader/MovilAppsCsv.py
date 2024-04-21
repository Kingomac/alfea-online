from .BaseCsvFile import BaseCsvFile


class MovilAppsCsv(BaseCsvFile):
    def __init__(self):
        super().__init__("game_data/movil_apps.csv")


movil_apps_csv = MovilAppsCsv()

if __name__ == '__main__':
    print(movil_apps_csv.rows)
