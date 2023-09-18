import re
import argparse
from pathlib import Path
import camelot

descr = {"1530": "доходы, полученные по операциям с ценными бумагами, обращающимися на организованном рынке ценных бумаг",
         "1538": "Доходы в виде процентов, полученные в налоговом периоде по совокупности договоров займа",
         "1532": "Доходы по операциям с фин.инстр. срочных сделок, обр-ся на орг.рынке, базисным активом кот. явл. ценные бумаги, фондовые индексы или иные фин.инстр",
         "1535": "Доходы по операциям с фин.инстр. срочных сделок, обр-ся на орг.рынке, базисным активом кот. не яв. ценные бумаги, фондовые индексы или иные фин.инстр.",
         "1010": "Дивиденды"}


def split_txt_row(line):
    return re.split("^(\d{2})\s(\d{4})\s([1-9][\d\s]+,\d{2}|0|0,\d{2})\s(?:(\d{3})\s([\d\s]+,\d{2})\s)?(\d{2})\s(\d{4})\s([\d\s]+,\d{2})(?:\s(\d{3})\s([\d\s]+,\d{2}))?$", line)


def get_row_balance(line, cred_index, deb_index):
    credit = "".join(line[cred_index].split()).replace(
        ",", ".") if line[cred_index] else "0"
    debet = "".join(line[deb_index].split()).replace(
        ",", ".") if line[deb_index] else "0"
    return float(credit) - float(debet)


def parse_txt(file):
    balance = {}

    with open(file, "rt") as f:
        for line in f.readlines():
            line = split_txt_row(line)
            balance[line[2]] = balance.get(
                line[2], 0) + get_row_balance(line, 3, 5)
            balance[line[7]] = balance.get(
                line[7], 0) + get_row_balance(line, 8, 10)

    return balance


def parse_one_table(table, balance):
    previous_code = ''
    for line in table.df.itertuples():
        if line[0] == 0:
            continue
        code = line[2] if line[2] != '' else previous_code
        balance[code] = balance.get(code, 0) + get_row_balance(line, 3, 5)
        previous_code = code
        if len(line) < 11 or line[7] == '':
            continue
        balance[line[7]] = balance.get(
            line[7], 0) + get_row_balance(line, 8, 10)
    return balance


def parse_pdf(file):
    balance = {}
    abc = camelot.read_pdf(file)
    for i in range(0, len(abc)-1):
        balance = parse_one_table(abc[i], balance)
    return balance


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", default="1.txt")
    args = parser.parse_args()
    try:
        balance = parse_txt(args.file) if Path(
            args.file).suffix == ".txt" else parse_pdf(args.file) if Path(
            args.file).suffix == ".pdf" else {}
        if len(balance) == 0:
            print("Нет данных или неверный формат файла")
        else:
            for key, value in balance.items():
                print("{key}, {descr}, {v:.2f}".format(
                    key=key, descr=descr[key], v=value))
    except Exception as e:
        print(e)
