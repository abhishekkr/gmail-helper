
## gmail-helper

> to allow helpful GMail tasks over OAuth2 API using Google's API Client

* generate and store `credentials.json` by creating an **OAuth client ID** credentials for your Google account by browsing [https://console.developers.google.com/apis/dashboard](https://console.developers.google.com/apis/dashboard) and clicking on `+ Create Credentials` button

* for creating mail filter queries [Google Support Reference](https://support.google.com/mail/answer/7190?ctx=gmail&hl=en&authuser=0) can be used

* if for some reason different scope need to be used in configuration, [Gmail Scope Reference](https://developers.google.com/gmail/api/auth/scopes#gmail_scopes) can be used


### Capabilities

* Permanently delete mails based on search criteria allowed by GMail such as partial match of `subject`, `to` or `from` e-mail address fields (also allowing just domain match). Ran for a range of years provided by config as `since_year` and `before_year`.

> by default it reads mails first and stores it locally in a sqlite DB separated by year of mail, then deletes
>
> How to use: `python3 delete-mails.py ./config-yamls/delete-mails-config.yaml`
>
> GMail API doc: [developers.google.com/gmail/api/v1/reference/users/messages/delete](https://developers.google.com/gmail/api/v1/reference/users/messages/delete)

---

#### ToDo

* offline backup of mails (all/filtered) into local SQLite3 db file; not of attachments

* delete filtered mails (by search term, by label); skips mails with attachment but can be forced to delete

* send mails from a custom template to a list of receivers

* check recent mails for a specific mail, act as desired if received

---
