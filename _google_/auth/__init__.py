from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle

import _logging_ as _log
import _config_ as _cfg


def google_oauth_creds():
    """Returns Google auth creds object.
    Persisted in a pickle on first generation, if missing gets created.

    Args: None

    Returns:
        Google credentials object.
    """
    creds = None
    oauth_scopes = _cfg.scopes()
    oauth_pickle = _cfg.gmail_auth_picklepath()
    gmail_credential_jsonpath = _cfg.gmail_credential_jsonpath()

    if os.path.exists(oauth_pickle):
        with open(oauth_pickle, 'rb') as token:
            creds = pickle.load(token)
    elif not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                gmail_credential_jsonpath, oauth_scopes)
            creds = flow.run_local_server(port=0)
        with open(oauth_pickle, 'wb') as token:
            pickle.dump(creds, token)
    return creds


def __gmail_v1__():
    creds = google_oauth_creds()
    service = build('gmail', 'v1', credentials=creds, cache_discovery=False)
    return service.users()


def gmail_messages():
    """Returns GMail messages object exposing message API.

    Args: None

    Returns:
        GMail message object.
    """
    return __gmail_v1__().messages()


def gmail_labels():
    """Returns GMail labels object exposing labels API.

    Args: None

    Returns:
        GMail labels object.
    """
    return __gmail_v1__().labels()


def gmail_filters():
    """Returns GMail labels object exposing labels API.

    Args: None

    Returns:
        GMail labels object.
    """
    return __gmail_v1__().settings().filters()
