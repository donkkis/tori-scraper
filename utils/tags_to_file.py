import argparse
from nlp.nlp import get_tags

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='../data/tags.csv')
    args = parser.parse_args()
    tags = get_tags()
    tags.to_csv(args.path)