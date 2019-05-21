from urllib.request import urlopen
import csv
import sqlite3


class DataHandler:
    def __init__(self, filename = None):
        with sqlite3.connect('matura.db') as conn:
            c = conn.cursor()

            #check if table exists
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='matura'")
            exists = c.fetchone()
            if not exists:
         
                if not filename:
                    print("Downloading data from dane.gov.pl...")
                    url = 'https://www.dane.gov.pl/media/resources/20190513/Liczba_os%C3%B3b_kt%C3%B3re_przystapi%C5%82y_lub_zda%C5%82y_egzamin_maturalny.csv'
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

                #Skip header
                next(reader, None)

                for row in reader:
                    if row:
                        c.execute("INSERT INTO matura VALUES(?,?,?,?,?)", row)
                conn.commit()

    def raw_select(self, sql, arg = None):
        with sqlite3.connect('matura.db') as conn:
            c = conn.cursor()
            if(arg):
                c.execute(sql,arg)
            else:
                c.execute(sql)
            return c.fetchall()


class Matura:

    def __init__(self, filename = None):
        self.dataHandler = DataHandler(filename)
     

    """ def calculate_mean(self, territory, year):
        results = self.dataHandler.select(["SUM(count)"], 
                                        {"territory": territory,
                                         "type"     : "przystąpiło",
                                         "year"     : year})
        print(territory, year, results[0][0])
    """

    def calculate_yearly_pass_rate(self, territory, mf=None):
        modifier = ''
        if(mf):
            modifier = 'AND A.gender = "' + mf +'" '
        
        sql= ('SELECT A.year, CAST(SUM(A.count) AS REAL)/SUM(B.count) '
              'FROM matura A, matura B ' 
              'WHERE A.type="zdało" ' 
              'AND B.type="przystąpiło" ' 
              'AND A.territory=B.territory ' 
              'AND A.year = B.year ' 
              'AND A.gender = B.gender '+modifier+' AND A.territory=? '
              'GROUP BY A.year')
        result = self.dataHandler.raw_select(sql, (territory,))
        print(territory)
        for row in result:
            print(row)  

    def find_best_territory(self, mf=None):
        modifier = ''
        if(mf):
            modifier = 'AND A.gender= "' + mf + '"'

        sql=('SELECT year, territory, MAX(x) '
            'FROM '
            '(SELECT A.year, A.territory, CAST(SUM(A.count) AS REAL)/SUM(B.count) AS x '
                'FROM matura A, matura B '
                'WHERE A.type="zdało" ' 
                'AND B.type="przystąpiło" '
                'AND A.territory = B.territory '
                'AND A.year = B.year '
                'AND A.gender = B.gender '+modifier+' '
            'GROUP BY A.year, A.territory) X '
            'GROUP BY year ')
        result = self.dataHandler.raw_select(sql)
        
        for row in result:
            print(row)  
                                              
    def find_regressive_territories(self, mf=None):
        modifier = ''
        if(mf):
            modifier = 'AND A.gender= "' + mf + '"'

        sql=('SELECT X.year AS prev_year, Y.year AS  next_year , X.territory, X.x AS prev_rate, Y.x AS next_rate '
            'FROM '
            '(SELECT A.year, A.territory, CAST(SUM(A.count) AS REAL)/SUM(B.count) AS x '
                'FROM matura A, matura B '
                'WHERE A.type="zdało" '
                'AND B.type="przystąpiło" '
                'AND A.territory = B.territory '
                'AND A.year = B.year '
                'AND A.gender = B.gender '+modifier+' '
                'GROUP BY A.year, A.territory) X, '
            '(SELECT A.year, A.territory, CAST(SUM(A.count) AS REAL)/SUM(B.count) AS x '
                'FROM matura A, matura B '
                'WHERE A.type="zdało" '
                'AND B.type="przystąpiło" '
                'AND A.territory = B.territory '
                'AND A.year = B.year '
                'AND A.gender = B.gender '+modifier+' '
                'GROUP BY A.year, A.territory) Y '
            'WHERE X.year + 1 = Y.year '
            'AND X.territory = Y.territory '
            'AND X.x > Y.x')
        result = self.dataHandler.raw_select(sql)

        for row in result:
            print(row)

    def compare_two_territories(self, territoryA, territoryB, mf=None):
        modifier = ''
        if(mf):
            modifier = 'AND A.gender= "' + mf + '"'

        sql=('SELECT year, territory, MAX(X.x) ' 
            'FROM '
            '(SELECT A.year, A.territory, CAST(SUM(A.count) AS REAL)/SUM(B.count) as x '
                'FROM matura A, matura B '
                'WHERE A.type="zdało" '
                'AND B.type="przystąpiło" '
                'AND A.territory = B.territory '
                'AND A.year = B.year '
                'AND A.gender = B.gender '+modifier+' '
                'AND (A.territory=? OR A.territory=?) ' 
                'GROUP BY A.year, A.territory) X '
            'GROUP BY year')
        result = self.dataHandler.raw_select(sql, (territoryA, territoryB))
        for row in result:
            print(row)  

def main():
    m = Matura('tttest.csv')
    #m.calculate_mean('Polska', 2010)
    m.calculate_yearly_pass_rate('Pomorskie')
    print('\n')
    m.find_best_territory()
    print('\n')
    m.find_regressive_territories()
    print('\n')
    m.compare_two_territories('Pomorskie', 'Podlaskie')

main()
