#!/usr/bin/env python
# * coding: utf8 *
'''
swapper

Usage:
    swapper swap <tables>...
    swapper compare [--swap]

Arguments:
    tables: One or more fully qualified table names DB.SCHEMA.Table (e.g. SGID.HEALTH.SmallAreas_ObesityAndActivity)
            separated by spaces.

Examples:
    swapper swap sgid.health.health_areas sgid.boundaries.counties      Swaps the health_areas and counties tables from
                                                                        SGID to SGID10.
    swapper compare --swap                                              Compares tables between SGID & SGID10 and swaps
                                                                        them if needed.
'''
from .swapper import copy_and_replace, compare
from docopt import docopt


def main():
    '''Main entry point for program. Parse arguments and route to top level methods.
    '''
    args = docopt(__doc__, version='1.0.0')

    def swap_tables(tables):
        for table in tables:
            print(f'updating table: {table}')
            copy_and_replace(table)

    if args['swap']:
        if args['<tables>']:
            swap_tables(args['<tables>'])
    elif args['compare']:
        tables_needing_update = compare()
        print(f'tables_needing_update: {(tables_needing_update)}')

        if args['--swap']:
            swap_tables(tables_needing_update)


if __name__ == '__main__':
    main()
