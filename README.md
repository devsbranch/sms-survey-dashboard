# PPCR-TRALARD

A service for monitoring ward beneficiary projects as well as reporting.
View a running instance at [http://81.28.6.181:8009](http://81.28.6.181:8009/)

Note that ppcr-tralard is under development and not yet feature complete.

The latest source code is available at
[https://github.com/Digital-Prophets/ppcr-tralard](https://github.com/Digital-Prophets/ppcr-tralard).

* **Developers:** See our [developer guide](README-dev.md)
* **For production:** See our [deployment guide](README-docker.md)


## Key features

* Granular user and access control management 
* Project level definition and meta data capture
* SubComponent management - project first level child entity
* SubcCmponent Indicator management
* Citizen Feedback management
* SubProject management - Subcomponent child entity
* Beneficiary Organization management - SubProject child entity
* Fund, Disbursement, Expediture management - SubProject child entity
* Training management - SubProject child entity - a high level training schedule manager
* Indicator report generation
* Custom report generation management for various data points
* Web Map - dynamic and feature rich GIS web map for subprojects
* REST API for data sharing - both browsable and interactive documentations 
* GraphQL API - a feature rich appolo graphQL API as an alternative to REST clients

## Quick Installation Guide

For deployment we use [docker](http://docker.com) so you need to have docker
running on the host. ppcr-tralard is a django app so it will help if you have
some knowledge of running a django site.

```
git clone git://github.com/Digital-Prophets/ppcr-tralard.git
cd ppcr-tralard/deployment
cp btsync-db.env.EXAMPLE btsync-db.env
cp btsync-media.env.EXAMPLE btsync-media.env

make build
make permissions
make web
# Wait a few seconds for the DB to start before to running the next command
make migrate
make collectstatic

```

At this point the project should be up and running at http://127.0.0.1:8009

If you need backups, put btsync keys in these files. If you don't need backups,
you can let the default content.

So as to create your admin account:
```
make superuser
```

**intercom.io**

If you wish to make use of [intercom.io](https://www.intercom.io), include a
`private.py` file in `core.settings` with your `INTERCOM_APP_ID` as a string.
The necessary code snippet is already included in `project_base.html`.

**google authentication**

In social auth to use the google authentication you need to go to:

https://console.developers.google.com/apis/credentials

Create and oath2 credential with these options:

Authorized redirect URIs

http://ppcr.org<your domain>/en/complete/google-oauth2/

Use the ppcr-tralard admin panel to set up the google account with your id and
secret

**github authentication**

Create a developer key here:

https://github.com/settings/applications/new

Set the callback and site homepage url to the top of your site e.g.

http://localhost:61202

At http://localhost:61202/en/site-admin/socialaccount/socialapp/add/

Set the key and secret from the github key page.

**Backups**

If you wish to sync backups, you need to establish a read / write btsync
key on your production server and run one or more btsync clients
with a read only key.

```
cd deployment
cp btsync-media.env.EXAMPLE btsync-media.env
cp btsync-db.env.EXAMPLE btsync-db.env
```

Now edit the ``btsync-media.env`` and ``btsync-db.env`` files, including
relevant SECRET and DEVICE settings.


## Credits

ppcr-tralard was funded by [Think2044](https://think2044.com) and developed by [DigitalProphets.com](http://digiprophets.com), [Think2044 - World Bank](https://think2044.com).

## Thank you

Thank you to the individual contributors who have helped to build PPCR-TRALARD:

* Alison Mukoma (Lead developer): alison@digiprophets.com
* Jachin Manda: jachin@digiprophets.com
* Chriford Siame: chriford@digiprophets.com
* Cephas Zulu: cephas@digiprophets.com
* Gift Muyembe: gift@digiprophets.com
* Olipa Tembo: olipa@digiprophets.com
* Prince Musole: prince@digiprophets.com
* Bupe Mulenga: bupe@digiprophets.com
