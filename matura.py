import argparse, controller

parser = argparse.ArgumentParser()

voivodeships_list = ['Dolnośląskie',
                     'Kujawsko-pomorskie',
                     'Lubelskie',
                     'Lubuskie',
                     'Łódzkie',
                     'Małopolskie',
                     'Mazowieckie',
                     'Opolskie',
                     'Podkarpackie',
                     'Podlaskie',
                     'Pomorskie',
                     'Śląskie',
                     'Świętokrzyskie',
                     'Warmińsko-Mazurskie',
                     'Wielkopolskie',
                     'Zachodniopomorskie']

years_list = range(2010, 2019)


class UserInterface:
    """ This is a class for the user interaction."""

    def __init__(self):
        self.parser = self.create_parser()

    def create_parser(self):
        """Creates parser for command line arguments."""

        gender_group = parser.add_mutually_exclusive_group()

        gender_group.add_argument("-m",
                                  "--male",
                                  action="store_const",
                                  dest="gender",
                                  const="mężczyźni",
                                  help="Calculate statistics only for the males.",
                                  default=None)

        gender_group.add_argument("-f",
                                  "--female",
                                  action="store_const",
                                  dest="gender",
                                  const="kobiety",
                                  help="Calculate statistics only for the females.",
                                  default=None)

        parser.add_argument("--filename",
                            action="store",
                            type=str,
                            dest="filename",
                            help="Specify filename with data.",
                            required=False,
                            default=None)

        subparsers = parser.add_subparsers(dest='command',
                                           help='Choose from {mean, yearly, best, regressive, compare}',
                                           required=True,
                                           metavar='COMMAND')

        mean_subparser = subparsers.add_parser('mean',
                                               description="Calculate the mean matura pass rate for voivodeships across the years")
        mean_subparser.add_argument('voivodeship',
                                    type=str,
                                    help='Voivodeship name',
                                    choices=voivodeships_list,
                                    metavar='VOIVODESHIP')

        mean_subparser.add_argument('year',
                                    type=int,
                                    help="Calculate data from 2010 to this year",
                                    choices=years_list,
                                    metavar='YEAR')

        mean_subparser.set_defaults(func=self.calculate_mean)

        yearly_subparser = subparsers.add_parser('yearly',
                                                 description="Calculate the yearly pass rate for a target voivodeship ")
        yearly_subparser.add_argument('voivodeship',
                                      type=str,
                                      help='Voivodeship name.',
                                      choices=voivodeships_list,
                                      metavar='VOIVODESHIP')

        yearly_subparser.set_defaults(func=self.calculate_yearly)

        best_subparser = subparsers.add_parser('best',
                                               description="Find the voivodeship with the best pass rate across the years.")
        best_subparser.set_defaults(func=self.calculate_best)

        regressive_subparser = subparsers.add_parser('regressive',
                                                     description="Find voivodeships that have regressive pass rate.")
        regressive_subparser.set_defaults(func=self.calculate_regressive)

        compare_subparser = subparsers.add_parser('compare',
                                                  description="Compare the yearly pass rates in the two voivodeships.")
        compare_subparser.add_argument('voivodeship1', type=str, help='First voivodeship name.',
                                       choices=voivodeships_list, metavar='VOIVODESHIP_1')
        compare_subparser.add_argument('voivodeship2', type=str, help='Scond voivodeship name.',
                                       choices=voivodeships_list, metavar='VOIVODESHIP_2')
        compare_subparser.set_defaults(func=self.calculate_compare)
        return parser

    def parse(self):
        """ Parse command line arguments."""

        args = parser.parse_args()
        self.c = controller.Controller(args.filename)
        args.func(args)

    def calculate_mean(self, args):
        self.c.calculate_mean(args.voivodeship, args.year, args.gender)

    def calculate_yearly(self, args):
        self.c.calculate_yearly_pass_rate(args.voivodeship, args.gender)

    def calculate_best(self, args):
        self.c.find_best_territory(args.gender)

    def calculate_regressive(self, args):
        self.c.find_regressive_territories(args.gender)

    def calculate_compare(self, args):
        self.c.compare_two_territories(args.voivodeship1, args.voivodeship2, args.gender)


def main():
    ui = UserInterface()
    ui.parse()


main()
