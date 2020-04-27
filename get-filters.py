# Copyright 2020 abhishekkr <abhikumar163@gmail.com>
"""
How to use:
    * for db persistence
        python3 get-labels.py ./config-yamls/get-filters-config.yaml
    * to export as json to filters_json_basepath configured dir
        python3 get-labels.py ./config-yamls/get-filters-config.yaml --to-json


How to configure:

* using "get-filters-config.yaml", update all values to required configuration

> * 'gmail_credential_jsonpath' is file path for OAuth2 credential json file downloaded from Google by following step from README
> * 'gmail_auth_picklepath' need to be file paths where Google credentials can be stored for reuse
> * 'scopes' is a list of GMail API scopes made available to Google Auth
> * 'data_basepath' is under which all DBs would be created
> * 'filters_json_basepath' is directory path where filters json will be saved if chosen to
>
> would be better if all above mentioned file paths should be at a secure location r/w only by your user


* using env variables

> all above mentioned config names prefixed with 'GMAIL_HELPER_' formulate their env var name
"""

from __future__ import print_function
import base64
import email
import sys

import _logging_ as _log
import _config_ as _cfg
import _google_.auth as _gauth
import _google_.gmail as _gmail
import _dbms_ as _db


def main():
    """Helps make a local backup of all lables."""
    filters_obj = _gauth.gmail_filters()
    if flag_export_to_json():
        _gmail.get_filters_to_json(filters_obj, "me")
        return
    db = _db.connection_by_feature("filters")
    _db.create_schema_filters(db)
    _gmail.get_filters(db, filters_obj, 'me')
    db.close()
    del db


def flag_export_to_json():
    if "--to-json" in sys.argv:
        return True
    return False


if __name__ == '__main__':
    main()
