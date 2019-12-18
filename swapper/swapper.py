#!/usr/bin/env python
# * coding: utf8 *
'''
swapper.py
Main module for swapper package.
'''
import os
from textwrap import dedent

from dotenv import load_dotenv

import arcpy

load_dotenv()


def delete_locks(fc_owner, fc_name):
    dbo_owner = os.path.join(os.getenv('SWAPPER_CONNECTION_FILE_PATH'), 'SGID10', 'SGID10_sde.sde')

    if not os.path.exists(dbo_owner):
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

    internal = os.path.join(os.getenv('SWAPPER_CONNECTION_FILE_PATH'), 'SGID_internal', f'SGID_{owner.title()}.sde')
    sgid10 = os.path.join(os.getenv('SWAPPER_CONNECTION_FILE_PATH'), 'SGID10', f'SGID10_{owner.title()}.sde')

    if not os.path.exists(internal):
        print(f'{internal} does not exist')

    if not os.path.exists(sgid10):
        print(f'{sgid10} does not exist')

    with arcpy.EnvManager(workspace=internal):
        if not arcpy.Exists(fc):
            print(f'{fc} does not exist in Internal SGID')

            return None

    with arcpy.EnvManager(workspace=sgid10):
        output_fc_sgid10 = f'{fc_name}_temp'

        if arcpy.Exists(output_fc_sgid10):
            print(f'{output_fc_sgid10} already exists in SGID10')

            return None

        input_fc_sgid = os.path.join(internal, fc_name)
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
            print(f'deleted {sgid10_connection_file}\\{fc_name}')
        except:
            print(f'could not delete {sgid10}\\{fc_name}')

        try:
            renamed_fc_sgid10 = output_fc_sgid10.replace('_temp', '')
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
