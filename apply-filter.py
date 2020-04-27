# Copyright 2020 abhishekkr <abhikumar163@gmail.com>
"""
How to use:
    * to apply a filter from provided json and save it's definition as json under configured `filters_json_basepath`
        python3 apply-filter.py config-yaml/apply-filter-config.yaml --from-json data/filters/this_would_be_filter_id_in_name_of_file.json
    * to apply multiple filter from provided json and save it's definition as json under configured `filters_json_basepath`
        python3 apply-filter.py config-yaml/apply-filter-config.yaml --from-json data/filters/this_would_be_filter_id_in_name_of_file.json --from-json data/filters/this_would_be_filter_id_in_name_of_file_2.json
    * to apply a filter from provided json, save filter created and delete the exisiting filter using switch '--remove-older'
        python3 apply-filter.py config-yaml/apply-filter-config.yaml --from-json data/filters/this_would_be_filter_id_in_name_of_file.json --remove-older


How to configure:

* using "apply-filter-config.yaml", update all values to required configuration

> * 'gmail_credential_jsonpath' is file path for OAuth2 credential json file downloaded from Google by following step from README
> * 'gmail_auth_picklepath' need to be file paths where Google credentials can be stored for reuse
> * 'scopes' is a list of GMail API scopes made available to Google Auth
> * 'data_basepath' is under which all DBs would be created
> * 'filters_json_basepath' is directory path where filters json will be saved
>
> would be better if all above mentioned file paths should be at a secure location r/w only by your user


* using env variables

> all above mentioned config names prefixed with 'GMAIL_HELPER_' formulate their env var name
"""

from __future__ import print_function
import base64
import email
import os
import sys

import _logging_ as _log
import _config_ as _cfg
import _google_.auth as _gauth
import _google_.gmail as _gmail
import _dbms_ as _db


def main():
    """Helps make a local backup of all lables."""
    filters_obj = _gauth.gmail_filters()
    for json_path in flag_import_from_json():
        if not os.path.isfile(json_path):
            _log.logger.error("missing json file: %s" % (json_path))
            continue
        new_filter = _gmail.create_filter_from_json(filters_obj, json_path, "me")
        _log.logger.debug(new_filter)
        filter_path = os.path.join(
            _cfg.filters_json_basepath(),
            "%s.json" % (new_filter['id']))
        if not _db.check_and_write_json(filter_path, new_filter):
            print("~ skipping removal as failed saving json for filter id: %s" % (new_filter['id']))
            continue
        if flag_override_filter():
            delete_filter_of_json(filters_obj, json_path)


def delete_filter_of_json(filters_obj, json_path):
    filter = _db.load_json(json_path)
    _gmail.delete_filter(filters_obj, filter['id'], "me")
    _log.logger.debug("deleted gmail filter %s" % (filter['id']))
    os.remove(json_path)
    _log.logger.debug("deleted old filter json %s" % (json_path))


def flag_override_filter():
    if "--remove-older" in sys.argv:
        return True
    return False


def flag_import_from_json():
    idx = 0
    filter_json_list = []
    while idx < len(sys.argv):
        if "--from-json" == sys.argv[idx]:
            idx += 1
            if idx < len(sys.argv):
                filter_json_list.append(sys.argv[idx])
            else:
                break
        idx += 1
    return filter_json_list


if __name__ == '__main__':
    main()
