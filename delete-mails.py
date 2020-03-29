# Copyright 2018 abhishekkr <abhikumar163@gmail.com>
"""
How to configure:

* using "delete-mails-config.yaml", update all values to required configuration

> * 'gmail_credential_jsonpath' is file path for OAuth2 credential json file downloaded from Google by following step from README
> * 'gmail_auth_picklepath' need to be file paths where Google credentials can be stored for reuse
> * 'scopes' is a list of GMail API scopes made available to Google Auth
> * 'data_basepath' is under which all DBs would be created
> * 'since_year' and 'before_year' gets used to form year range
> * 'filters_to_delete' is list of filters to be used for query formation
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
    """Helps make a local backup of all messages in given year range,
    for given mail filters to query
    and then delete the read mail.
    """
    messages_obj = _gauth.gmail_messages()
    filters_to_delete = _cfg.filters_to_delete()
    since_year = _cfg.since_year()
    before_year = _cfg.before_year()

    for year in range(since_year, before_year):
        db = _db.connection_by_year(year)
        _db.create_schema_messages(db)
        for month in range(1,13):
            upto_year, upto_month = year, (month+1)
            if month == 12: upto_year, upto_month = (year+1), 1
            time_query = 'after:%s/%s/1 before:%s/%s/1' % (year, month, upto_year, upto_month)
            for filter in filters_to_delete:
                full_query = "%s %s" % (filter, time_query)
                _gmail.get_delete_mails_by_query(db, messages_obj, 'me', full_query)
        db.close()
        del db


if __name__ == '__main__':
    main()
