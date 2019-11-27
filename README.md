# load-and-replace

This tool will:

1. Take a sgid-internal feature class name (ie SGID.OWNER.FeatureClass) as input.
1. Parse the name to get the corresponding connection files in L:\sgid_to_agol\ConnectionFilesSGID
1. Check if the input sgid-internal connection file exists
1. Check if the output sgid10 connection file exists
1. Check if the sgid-internal input feature class exists
1. Copy the feature class to sgid10 named fc_temp
1. Run a function to delete the table locks on the old sgid10 feature class that's being replaced
1. Delete the sgid10 feature class that's being replaced
1. Rename the new copied feature class from fc_temp to fc
1. Update the privileges for the agrc and SearchAPI users
