# -*- coding: utf-8 -*-

import argparse

if __name__ == '__main__':

    agParser = argparse.ArgumentParser(add_help=False)

    agParser.add_argument('--a',default=1,type=int)
    agParser.add_argument('--b',default='haha',type=str)

    m = agParser.parse_args()

    print(m.a,m.b)