import argparse
import csv
from connectChecker import ConnectChecker

parser = argparse.ArgumentParser(
    prog="Приложение для отслеживания состояния сайтов",
    description="Алгоритм, который проверяет доступность сайтов по данным доменным именам"
    + "или IP-адресам",
)

parser.add_argument(
    "filename",
    type=str,
    help='местоположенеи csv файла с заголовком ""Host;Ports"" и разделителем ";"'
    + 'если портов несколько, то их следует разделять через ",", без пробелов',
)
args = parser.parse_args()

def show(connect):
    # вывод результатов проверки
    print(connect)
    for result in connect.checkConnection():
        print(result)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


try:
    with open(args.filename, "r", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            if row["Host"] == "":
                continue
            try:
                connect = ConnectChecker(row["Host"], row["Ports"])
                show(connect)
            except ValueError:
                print(f"{row['Host']}, {row['Ports']} недоступен")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

except FileNotFoundError:
    print("Файл не найден")

except Exception as e:
    print("Неизвестная ошиибка: ", e)
