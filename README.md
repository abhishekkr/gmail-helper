
## gmail-helper

> to allow helpful GMail tasks over OAuth2 API using Google's API Client

* generate and store `credentials.json` by creating an **OAuth client ID** credentials for your Google account by browsing [https://console.developers.google.com/apis/dashboard](https://console.developers.google.com/apis/dashboard) and clicking on `+ Create Credentials` button

> details on how to get credentials json are [here](wiki/gmail-credentials.md)

* for creating mail filter queries [Google Support Reference](https://support.google.com/mail/answer/7190?ctx=gmail&hl=en&authuser=0) can be used

* if for some reason different scope need to be used in configuration, [Gmail Scope Reference](https://developers.google.com/gmail/api/auth/scopes#gmail_scopes) can be used


### Capabilities

* Permanently delete mails based on search criteria allowed by GMail such as partial match of `subject`, `to` or `from` e-mail address fields (also allowing just domain match). Ran for a range of years provided by config as `since_year` and `before_year`.

> by default it reads mails first and stores it locally (except attachments) in a sqlite DB separated by year of mail, then deletes
>
> How to use: `python3 delete-mails.py ./config-yamls/delete-mails-config.yaml`
>
> GMail API doc: [developers.google.com/gmail/api/v1/reference/users/messages/delete](https://developers.google.com/gmail/api/v1/reference/users/messages/delete)

* Fetch created GMail Labels and persist to a local DB

> How to use: `python3 get-labels.py ./config-yamls/get-labels-config.yaml`


* Get all GMail filters

> * persisted in db: `python3 get-labels.py ./config-yamls/get-filters-config.yaml`
>
> * exported to json in configured dir `filters_json_basepath` with adding switch `--to-json` to above command


* Create a new/overwrite GMail filter

> * read [command help](wiki/filter-create.md) for usage help
>
> * details can be found at [developers.google.com](https://developers.google.com/gmail/api/v1/reference/users/settings/filters)

---

#### ToDo

* offline backup of mails (all/filtered) into local SQLite3 db file; not of attachments

* send mails from a custom template to a list of receivers

* check recent mails for a specific mail, act as desired if received

---

### For Contributors

* Decent list and definitions for possible exposures for Google-API-Python-Client [http://googleapis.github.io/google-api-python-client/docs/dyn/gmail_v1.html](http://googleapis.github.io/google-api-python-client/docs/dyn/gmail_v1.html)

* [Hacker News discussion](https://news.ycombinator.com/item?id=22989904)

---
