from apiclient import errors

import _config_ as _cfg
import _dbms_ as _db
import _logging_ as _log


def get_labels(db, labels_obj, user_id='me'):
    results = labels_obj.list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        _log.logger.info("No labels found.")
        return

    print('Labels:')
    for label in labels:
        if _db.add_label(db, label):
            print("~ added: %s" % (label['name']))


def get_mail(db, messages_obj, msg_id, user_id='me'):
    """Fetch a message from GMail by id and adds it to passed db.

    Args:
        db: Local db connection object.
        messages_obj: Authenticated GMail user object.
        msg_id: Id of Gmail message.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
    """
    message = messages_obj.get(
        userId=user_id, id=msg_id, format='full'
    ).execute()

    if set.intersection(set(_cfg.labels_to_skip()), set(message['labelIds'])) != set():
        return False
    _log.logger.debug("adding message: %s" % (message['id']))
    if not _db.add_message(db, message):
        return False
    return True


def delete_mail(messages_obj, msg_id, user_id='me'):
    """Delete a message from GMail by id.

    Args:
      messages_obj: Authenticated GMail user object.
      msg_id: ID of Message to delete.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
    """
    try:
      messages_obj.delete(userId=user_id, id=msg_id).execute()
      _log.logger.info('Message with id: %s deleted successfully.' % msg_id)
    except Exception as e:
        _log.logger.error('An error occurred: %s' % str(e))


def mails_by_query(messages_obj, user_id='me', query=''):
  """List all Messages of the user's mailbox matching the query.

  Args:
    messages_obj: Authenticated GMail user object.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = messages_obj.list(userId=user_id,
                                               q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = messages_obj.list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except Exception as e:
    _log.logger.error('An error occurred: %s' % str(e))
    return []


def get_delete_mails_by_query(db, messages_obj, user_id='me', query=''):
    """Get and Delete a list of messages from GMail by Query.

    Args:
        db: Local db connection object.
        messages_obj: Authenticated GMail user object.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.
    """
    message_ids_to_skip = _cfg.message_ids_to_skip()
    for message in mails_by_query(messages_obj, user_id, query):
        if message['id'] in message_ids_to_skip: continue
        _log.logger.debug(message['id'])
        if get_mail(db, messages_obj, message['id']):
            delete_mail(messages_obj, message['id'])
        else:
            _log.logger.error("not deleting mail: %s" % (message['id']))
