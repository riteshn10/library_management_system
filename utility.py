from tabulate import tabulate


def print_table(rows, headers):
    print(tabulate(rows, headers=headers, tablefmt='grid'))