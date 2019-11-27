#!/usr/bin/env python
# * coding: utf8 *
'''
load_and_replace.py
A module that replaces data with minimal interruption
'''


import os
from textwrap import dedent

import arcpy


def delete_locks(fc_owner, fc_name):
    dbo_owner = r'L:\sgid_to_agol\ConnectionFilesSGID\SGID10\SGID10_sde.sde'
    db_connect = arcpy.ArcSDESQLExecute(dbo_owner)

    sql = dedent(
        f'''SELECT * FROM sde.SDE_process_information
        WHERE SDE_ID IN(SELECT SDE_ID FROM sde.SDE_table_locks
        WHERE registration_id = (SELECT registration_id FROM sde.SDE_table_registry
        WHERE table_name = '{fc_name}' AND owner = UPPER('{fc_owner}')));
        ''')

    db_return = db_connect.execute(sql)

    if db_return is True:
        print('no locks to delete')

        return

    for user in db_return:
        print (f'deleted lock {user[0]}')
        arcpy.DisconnectUser(dbo_owner, user[0])


def copy_and_replace(fc):
    sgid_connections_path = r'L:\sgid_to_agol\ConnectionFilesSGID\SGID_internal'
    sgid10_connections_path = r'L:\sgid_to_agol\ConnectionFilesSGID\SGID10'

    owner = fc.split('.')[1].upper()
    fc_name = fc.split('.')[2].strip()

    sgid_connection_file = f'SGID_{owner.title()}.sde'
    sgid10_connection_file = f'SGID10_{owner.title()}.sde'

    if not os.path.exists(os.path.join(sgid_connections_path, sgid_connection_file)):
        print(f'{sgid_connection_file} does not exist')

    if not os.(os.path.join(sgid10_connections_path, sgid10_connection_file)):
        print(f'{sgid10_connection_file} does not exist')

    with arcpy.EnvManager(workspace=os.path.join(sgid_connections_path, sgid_connection_file)):
        if not arcpy.Exists(fc):
            print(f'{fc} does not exist in Internal SGID')

            return None

    with arcpy.EnvManager(workspace=os.path.join(sgid10_connections_path, sgid10_connection_file)):
        output_fc_sgid10 = f'{fc_name}_temp'

        if arcpy.Exists(output_fc_sgid10):
            print(f'{output_fc_sgid10} already exists in SGID10')

            return None

        input_fc_sgid = os.path.join(sgid_connections_path, sgid_connection_file, fc_name)
        print(input_fc_sgid)

        try:
            arcpy.CopyFeatures_management(input_fc_sgid, output_fc_sgid10)
            print(f'copied {input_fc_sgid} to {output_fc_sgid10}')
        except:
            print (f'could not copy to sgid10')

        try:
            delete_locks(owner, fc_name)
        except:
            print (f'could not delete table locks')

        try:
            arcpy.Delete_management(fc_name)
            print (f'deleted {sgid10_connection_file}\{fc_name}')
        except:
            print (f'could not delete {sgid10_connection_file}\{fc_name}')

        try:
            renamed_fc_sgid10 = output_fc_sgid10.strip('_temp')
            print (f'renamed {output_fc_sgid10}')
            arcpy.Rename_management(output_fc_sgid10, renamed_fc_sgid10)
        except:
            print (f'could not rename {output_fc_sgid10}')

        try:
            user_list = ['agrc', 'SearchAPI']
            for user in user_list:
                arcpy.ChangePrivileges_management(renamed_fc_sgid10, user, 'GRANT', 'AS_IS')
        except:
            print (f'could not update privileges to {renamed_fc_sgid10}')

copy_and_replace('SGID.HEALTH.SmallAreas_ObesityAndActivity')
