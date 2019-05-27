import datahandler


class Controller:
    """A class for communication between the database and the user intrface.

    Specifies SQL queries and presents statistics

    Attributes:
    filename (str): file name of .csv file with data (default None)
    """

    def __init__(self, filename=None):
        self.dataHandler = datahandler.DataHandler(filename)

    def calculate_mean(self, territory, year, mf=None):
        """Calculate mean pass rate across the years.

        Arguments:
        territory (str): Name of territory
        year (int): Maximum year used to calculate statistics
        mf (str): "mężczyźni" or "kobiety" to specify filter (default None)
        """
        print('Calculating mean pass rate for', territory, 'from 2010 to', year)
        modifier = self.get_modifier(mf)

        sql = ('SELECT AVG(x) '
               'FROM (SELECT A.year, CAST(SUM(A.count) AS REAL)/SUM(B.count) AS x '
               'FROM matura A, matura B '
               'WHERE A.type="zdało" '
               'AND B.type="przystąpiło" '
               'AND A.territory=B.territory '
               'AND A.year = B.year '
               'AND A.gender = B.gender ' + modifier +
               ' AND A.territory=? '
               'AND A.year <=? '
               'GROUP BY A.year)')

        result = self.dataHandler.raw_select(sql, (territory, year))

        for row in result:
            print('{:.2f}%'.format(row[0] * 100))

    def calculate_yearly_pass_rate(self, territory, mf=None):
        """Calculate yearly pass rate for the target territory.

        Arguments:
        territory (str): Name of territory
        mf (str): "mężczyźni" or "kobiety" to specify filter (default None)
        """

        print('Calculating yearly pass rate for', territory)
        modifier = self.get_modifier(mf)

        sql = ('SELECT A.year, CAST(SUM(A.count) AS REAL)/SUM(B.count) '
               'FROM matura A, matura B '
               'WHERE A.type="zdało" '
               'AND B.type="przystąpiło" '
               'AND A.territory=B.territory '
               'AND A.year = B.year '
               'AND A.gender = B.gender ' + modifier +
               ' AND A.territory=? '
               'GROUP BY A.year')
        result = self.dataHandler.raw_select(sql, (territory,))

        for row in result:
            print('{:d} {:.2f}%'.format(row[0], row[1] * 100))

    def find_best_territory(self, mf=None):
        """Find the territory with the best pass rate across the years.

        Arguments:
        mf (str): "mężczyźni" or "kobiety" to specify filter (default None)
        """

        print('Finding voivodeship with the best pass rate across the years')
        modifier = self.get_modifier(mf)

        sql = ('SELECT year, territory, MAX(x) '
               'FROM '
               '(SELECT A.year, A.territory, CAST(SUM(A.count) AS REAL)/SUM(B.count) AS x '
                    'FROM matura A, matura B '
                    'WHERE A.type="zdało" '
                    'AND B.type="przystąpiło" '
                    'AND A.territory = B.territory '
                    'AND A.year = B.year '
                    'AND A.gender = B.gender ' + modifier + ' '
                    'GROUP BY A.year, A.territory) X '
               'GROUP BY year ')

        result = self.dataHandler.raw_select(sql)

        for row in result:
            print('{:d}: {:19} {:.2f}%'.format(row[0], row[1], row[2] * 100))

    def find_regressive_territories(self, mf=None):
        """Find regressive territories.

        Arguments:
        mf (str): "mężczyźni" or "kobiety" to specify filter (default None)
        """

        print('Finding regressive voivodeships')
        modifier = self.get_modifier(mf)

        sql = ('SELECT X.year AS prev_year, Y.year AS  next_year , X.territory, X.x AS prev_rate, Y.x AS next_rate '
               'FROM '
               '(SELECT A.year, A.territory, CAST(SUM(A.count) AS REAL)/SUM(B.count) AS x '
                    'FROM matura A, matura B '
                    'WHERE A.type="zdało" '
                    'AND B.type="przystąpiło" '
                    'AND A.territory = B.territory '
                    'AND A.year = B.year '
                    'AND A.gender = B.gender ' + modifier + ' '
                    'GROUP BY A.year, A.territory) X, '
                '(SELECT A.year, A.territory, CAST(SUM(A.count) AS REAL)/SUM(B.count) AS x '
                    'FROM matura A, matura B '
                    'WHERE A.type="zdało" '
                    'AND B.type="przystąpiło" '
                    'AND A.territory = B.territory '
                    'AND A.year = B.year '
                    'AND A.gender = B.gender ' + modifier + ' '
                    'GROUP BY A.year, A.territory) Y '
               'WHERE X.year + 1 = Y.year '
               'AND X.territory = Y.territory '
               'AND X.x > Y.x')

        result = self.dataHandler.raw_select(sql)

        for row in result:
            print('{:19}  {:d}: {:.2f}% -> {:d}: {:.2f}%'.format(row[2], row[0], row[3] * 100, row[1], row[4] * 100))

    def compare_two_territories(self, territoryA, territoryB, mf=None):
        """Compare two territories across the years.

        Arguments:
        territoryA (str): Name of the first territory
        territoryB (str): Name of the second territory
        mf (str): "mężczyźni" or "kobiety" to specify filter (default None)
        """


        print('Comparing', territoryA, 'and', territoryB, 'across the years')
        modifier = self.get_modifier(mf)

        sql = ('SELECT year, territory, MAX(X.x) '
               'FROM '
               '(SELECT A.year, A.territory, CAST(SUM(A.count) AS REAL)/SUM(B.count) as x '
               'FROM matura A, matura B '
               'WHERE A.type="zdało" '
               'AND B.type="przystąpiło" '
               'AND A.territory = B.territory '
               'AND A.year = B.year '
               'AND A.gender = B.gender ' + modifier + ' '
               'AND (A.territory=? OR A.territory=?) '
               'GROUP BY A.year, A.territory) X '
               'GROUP BY year')
        result = self.dataHandler.raw_select(sql, (territoryA, territoryB))

        for row in result:
            print('{} {:19} {:.2f}%'.format(row[0], row[1], row[2] * 100))

    def get_modifier(self, mf):
        if (mf):
            if mf == 'mężczyźni':
                print('For males only.')
            else:
                print('For females only.')
            return 'AND A.gender= "' + mf + '"'
        else:
            return ''
