
## How To Get Authentication Completed

> TROUBLESHOOT: when see `invalid_grant` errors, means your Grant from Google OAuth has expired.. remove your file from path configured for `gmail_auth_picklepath` & re-run; it will re-auth and get fresh grant

* generate and store `credentials.json` by creating an **OAuth client ID** credentials for your Google account by browsing [https://console.developers.google.com/apis/dashboard](https://console.developers.google.com/apis/dashboard) and clicking on `+ Create Credentials` button

* Goto following url for your GMail account: https://console.developers.google.com/apis/credentials

> * There you'll find your newly created OAuth Client entry under sub-section `OAuth 2.0 Client IDs`.
>
> * Click on its Download Icon to get your credentials json. Copy it somewhere safe, configure its path in **config yaml** to be used.

* Do remember to update other values of your config yaml as desired.

* (**Only on first run**) Now when you run your required GMail utility for the first time, it will open GMail link in your default browser. You'll need to allow permission in browser, can then close it. The utility will save theis auth token in a pickle file locally and use it for new future until revoked.

> Once revoked last step will get repeated again, on next run.

---
