#!/usr/bin/env python
# * coding: utf8 *
'''
swapper.py
Main module for swapper package.
'''
from os import getenv
from pathlib import Path
from textwrap import dedent

from dotenv import load_dotenv
from xxhash import xxh64

import arcpy
import pyodbc

load_dotenv()


def delete_locks(fc_owner, fc_name):
    dbo_owner = Path(getenv('SWAPPER_CONNECTION_FILE_PATH')) / 'SGID10' / 'SGID10_sde.sde'

    if not Path(dbo_owner).exists():
        print(f'{dbo_owner} does not exist')

        return

    db_connect = arcpy.ArcSDESQLExecute(dbo_owner)

    sql = dedent(
        f'''SELECT * FROM sde.SDE_process_information
        WHERE SDE_ID IN(SELECT SDE_ID FROM sde.SDE_table_locks
        WHERE registration_id = (SELECT registration_id FROM sde.SDE_table_registry
        WHERE table_name = '{fc_name}' AND owner = UPPER('{fc_owner}')));
    '''
    )

    db_return = db_connect.execute(sql)

    if db_return is True:
        print('no locks to delete')

        return

    for user in db_return:
        print(f'deleted lock {user[0]}')
        arcpy.DisconnectUser(dbo_owner, user[0])


def copy_and_replace(fc):
    owner = fc.split('.')[1].upper()
    fc_name = fc.split('.')[2].strip()

    internal = Path(getenv('SWAPPER_CONNECTION_FILE_PATH')) / 'SGID_internal' / f'SGID_{owner.title()}.sde'
    sgid10 = Path(getenv('SWAPPER_CONNECTION_FILE_PATH')) / 'SGID10' / f'SGID10_{owner.title()}.sde'

    if not Path(internal).exists():
        print(f'{internal} does not exist')

    if not Path(sgid10).exists():
        print(f'{sgid10} does not exist')

    with arcpy.EnvManager(workspace=internal):
        if not arcpy.Exists(fc):
            print(f'{fc} does not exist in Internal SGID')

            return None

    temp_extension = '_temp'

    with arcpy.EnvManager(workspace=sgid10):
        output_fc_sgid10 = f'{fc_name}{temp_extension}'

        if arcpy.Exists(output_fc_sgid10):
            print(f'{output_fc_sgid10} already exists in SGID10')

            return None

        input_fc_sgid = Path(internal) / fc_name
        print(input_fc_sgid)

        try:
            arcpy.management.CopyFeatures(input_fc_sgid, output_fc_sgid10)
            print(f'copied {input_fc_sgid} to {output_fc_sgid10}')
        except:
            print(f'could not copy to sgid10')

        try:
            delete_locks(owner, fc_name)
        except:
            print(f'could not delete table locks')

        try:
            arcpy.management.Delete(fc_name)
            print(f'deleted {sgid10}\\{fc_name}')
        except:
            print(f'could not delete {sgid10}\\{fc_name}')

        try:
            renamed_fc_sgid10 = output_fc_sgid10[:-len(temp_extension)]
            print(f'renamed {output_fc_sgid10}')
            arcpy.management.Rename(output_fc_sgid10, renamed_fc_sgid10)
        except:
            print(f'could not rename {output_fc_sgid10}')

        try:
            user_list = ['agrc', 'SearchAPI']
            for user in user_list:
                arcpy.management.ChangePrivileges(renamed_fc_sgid10, user, 'GRANT', 'AS_IS')
        except:
            print(f'could not update privileges to {renamed_fc_sgid10}')


def compare():
    '''compares data sets between SGID and SGID10 and returns the tables that are different
    '''
    dbo_owner = Path(getenv('SWAPPER_CONNECTION_FILE_PATH')) / 'SGID10' / 'SGID10_sde.sde'

    if not Path(dbo_owner).exists():
        print(f'{dbo_owner} does not exist')

        return []

    tables_needing_update = []

    internal_connection = pyodbc.connect(getenv('SWAPPER_INTERNAL_DB_CONNECTION'))
    internal_hashes = get_hashes(internal_connection.cursor())
    sgid10_connection = pyodbc.connect(getenv('SWAPPER_EXTERNAL_DB_CONNECTION'))
    sgid10_hashes = get_hashes(sgid10_connection.cursor())

    tables_missing_from_internal = set(sgid10_hashes) - set(internal_hashes)
    if len(tables_missing_from_internal) > 0:
        print(f'tables_missing_from_internal: {tables_missing_from_internal}')

    tables_missing_from_sgid10 = set(internal_hashes) - set(sgid10_hashes)
    if len(tables_missing_from_sgid10) > 0:
        print(f'tables_missing_from_sgid10: {tables_missing_from_sgid10}')

    for table in set(internal_hashes) & set(sgid10_hashes):
        if internal_hashes[table] != sgid10_hashes[table]:
            tables_needing_update.append(table)

    return tables_needing_update


def get_hashes(cursor):
    table_field_map = discover_and_group_tables_with_fields(cursor)
    table_hash_map = {}

    for table in table_field_map:
        fields = table_field_map[table]

        hash = create_hash_from_table_rows(table, fields, cursor)

        table_hash_map[table.replace('sgid10', 'sgid')] = hash

    return table_hash_map


def create_hash_from_table_rows(table, fields, cursor):
    print(f'hashing: {table}')
    query = f'SELECT {",".join(fields)} FROM {table} ORDER BY OBJECTID'
    rows = cursor.execute(query).fetchall()

    hashes = ''

    for row in rows:
        hash_me = [str(value) for value in row]

        hash = xxh64(''.join(hash_me)).hexdigest()

        hashes += hash

    return xxh64(hashes).hexdigest()


def discover_and_group_tables_with_fields(cursor):
    skip_fields = ['gdb_geomattr_data', 'globalid', 'global_id', 'objectid_']

    table_meta_query = '''SELECT LOWER(table_name)
        FROM sde.sde_table_registry registry
        WHERE NOT (table_name like 'SDE_%' OR table_name like 'GDB_%') AND description IS NULL'''

    tables_rows = cursor.execute(table_meta_query).fetchall()
    tables = [table for table, in tables_rows]
    field_meta_query = f'''SELECT LOWER(table_catalog) as [db], LOWER(table_schema) as [schema], LOWER(table_name) as [table], LOWER(column_name) as [field], LOWER(data_type) as field_type
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_name IN ({join_strings(tables)}) AND LOWER(column_name) NOT IN ({join_strings(skip_fields)})'''
    field_meta = cursor.execute(field_meta_query).fetchall()

    table_field_map = {}

    for db, schema, table, field, field_type in field_meta:
        full_table_name = f'{db}.{schema}.{table}'
        if field_type == 'geometry':
            field = f'{field}.STAsText() as {field}'

        if full_table_name not in table_field_map:
            table_field_map[full_table_name] = [field]

            continue

        table_field_map[full_table_name].append(field)

    return table_field_map


def join_strings(strings):
    return "'" + "','".join(strings) + "'"
