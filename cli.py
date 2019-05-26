import argparse, matura
parser = argparse.ArgumentParser()


class UserInterface:
    def __init__(self):
        self.parser = self.createParser()
    
    def createParser(self):
        gender_group = parser.add_mutually_exclusive_group()
        gender_group.add_argument("-m", "--male", action="store_const", dest="gender", const="Mężczyźni", help="Calculate statistics only for the males.", default=None)

        gender_group.add_argument("-f", "--female", action="store_const", dest="gender", const="Kobiety", help="Calculate statistics only for the females.", default=None)

        parser.add_argument("--filename", action="store", type=str, dest="filename", help="Specify filename with data.", required=False, default=None)


        subparsers = parser.add_subparsers(dest='command', required=True)

        mean_subparser = subparsers.add_parser('mean', description="Calculate the mean matura pass rate for voivodeships across the years")
        mean_subparser.add_argument('voivodeship', type=str,  help='Voivodeship name')
        mean_subparser.add_argument('year', type=int)
        mean_subparser.set_defaults(func=self.calculate_mean)

        yearly_subparser = subparsers.add_parser('yearly', description="Calculate the yearly pass rate for a target voivodeship ")
        yearly_subparser.add_argument('voivodeship', type=str,  help='Voivodeship name.')
        yearly_subparser.set_defaults(func=self.calculate_yearly)

        best_subparser = subparsers.add_parser('best', description="Find the voivodeship with the best pass rate across the years.")
        best_subparser.set_defaults(func=self.calculate_best)

        regressive_subparser = subparsers.add_parser('regressive', description="Find voivodeships that have regressive pass rate.")
        regressive_subparser.set_defaults(func=self.calculate_regressive)

        compare_subparser = subparsers.add_parser('compare', description="Compare the yearly pass rates in the two voivodeships.")
        compare_subparser.add_argument('voivodeship1', type=str,  help='First voivodeship name.')
        compare_subparser.add_argument('voivodeship2', type=str,  help='Scond voivodeship name.')
        compare_subparser.set_defaults(func=self.calculate_compare)
        return parser

    def parse(self):
        args = parser.parse_args()
        self.m = matura.Matura(args.filename)
        args.func(args)


    def calculate_mean(self, args):
    	print('MEAN')
    	self.m.calculate_mean(args.voivodeship, args.year, args.gender)

    def calculate_yearly(self, args):
    	print('YEARLY')
    	self.m.calculate_yearly_pass_rate(args.voivodeship, args.gender)


    def calculate_best(self, args):
        print('BEST')
        self.m.find_best_territory(args.gender)
   

    def calculate_regressive(self, args):
        print('REGRESSIVE')
        self.m.find_regressive_territories(args.gender)
       

    def calculate_compare(self, args):
        print('COMPARE')
        self.m.compare_two_territorues(args.voivodeship1, args.voivodeship2, args.gender)

 
def main():
    ui = UserInterface()
    ui.parse()

main()
