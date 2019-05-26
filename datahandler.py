from urllib.request import urlopen
import csv
import sqlite3


class DataHandler:
    def __init__(self, filename=None):
        with sqlite3.connect('matura.db') as conn:
            c = conn.cursor()

            # check if table exists
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='matura'")
            exists = c.fetchone()
            if not exists:

                if not filename:
                    print("Downloading data from dane.gov.pl...")
                    url = 'https://www.dane.gov.pl/media/resources/20190520/Liczba_os%C3%B3b_kt%C3%B3re_przystapi%C5%82y_lub_zda%C5%82y_egzamin_maturalny.csv'
                    # url = 'https://www.dane.gov.pl/media/resources/20190513/Liczba_os%C3%B3b_kt%C3%B3re_przystapi%C5%82y_lub_zda%C5%82y_egzamin_maturalny.csv'
                    with urlopen(url) as response:
                        response = response.read().decode('cp1250')
                else:
                    print("Reading from file " + filename + "...")
                    with open(filename) as f:
                        response = f.read()

                c.execute('''CREATE TABLE matura(
                                territory text,
                                type text,
                                gender text,
                                year integer,
                                count integer)''')

                reader = csv.reader(response.split('\n'), delimiter=';')

                # Skip header
                next(reader, None)

                for row in reader:
                    if row and row[0] != "Polska":
                        c.execute("INSERT INTO matura VALUES(?,?,?,?,?)", row)
                conn.commit()

    def raw_select(self, sql, arg=None):
        with sqlite3.connect('matura.db') as conn:
            c = conn.cursor()
            if (arg):
                c.execute(sql, arg)
            else:
                c.execute(sql)
            return c.fetchall()
