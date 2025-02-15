from argparse import ArgumentParser
from app.cli import main

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--i', type=str, required=False,
                        help="Enter import job name, import products for example.")
    parser.add_argument('-e', '--e', type=str, required=False,
                        help="Enter export job name, import documents for example.")
    args = parser.parse_args()
    main(args)
