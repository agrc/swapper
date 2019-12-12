#!/usr/bin/env python
# * coding: utf8 *
'''
swapper

Usage:
    swapper swap <tables>...

Arguments:
    table: the fully qualified table name DB.SCHEMA.Table e.g., SGID.HEALTH.SmallAreas_ObesityAndActivity

Examples:
    swapper swap sgid.health.health_areas sgid.boundaries.counties
'''
from .swapper import copy_and_replace
from docopt import docopt


def main():
    '''Main entry point for program. Parse arguments and route to top level methods.
    '''
    args = docopt(__doc__, version='1.0.0')

    if args['<tables>']:
        for table in args['<tables>']:
            print(f'updating single table: {table}')
            copy_and_replace(table)


if __name__ == '__main__':
    main()
