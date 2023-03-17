import argparse
import csv
from connectChecker import ConnectChecker
from time import sleep

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

parser.add_argument(
    '-c',
    type=int,
    default=10,
    help='интервал между проверками в секундах. По умолчанию 10 с'
)

parser.add_argument(
    '-r',
    type=int,
    default=1,
    help='количество проверок. По умолчанию 1 проверка.'
)

args = parser.parse_args()

assert args.c >= 10
assert args.r >= 1

def show(connect):
    # вывод результатов проверки
    print(connect)
    for result in connect.checkConnection():
        print(result)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

def main():
    try:
        with open(args.filename, "r", newline="") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                if row["Host"] == "":
                    continue
                try:
                    connect = ConnectChecker(row["Host"], row["Ports"])
                    show(connect)
                except PermissionError:
                    print("Не хватает прав доступа для сетевых операций.")
                    exit()
                except:
                    print(f"{row['Host']}, {row['Ports']} недоступен")
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


    except FileNotFoundError:
        print("Файл не найден")

    except ValueError as e:
        print("Неизвестная ошиибка: ", e)


for i in range(args.r):
    main()
    sleep(args.c)