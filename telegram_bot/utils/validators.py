from datetime import datetime


def date_validator(date: str):
    for symb in ['-', '.']:
        date = date.replace(symb, " ")
    try:
        date = datetime.strptime(date, "%Y %m %d").date()
        print('SUCCESS')
        return date
    except ValueError as e:
        print(e)
        return None


if __name__ == '__main__':
    print(date_validator(input("Type a date: ")))