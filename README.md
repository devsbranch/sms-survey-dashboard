# SMS SURVEY DASHBOARD

A service to monitoring sms survey as well as reporting.

The Latest source code is available at
[https://github.com/Digital-Prophets/sms-survey-dashboard](https://github.com/Digital-Prophets/sms-survey-dashboard)


* **Developers:** See our [developer guide](README-dev.md)
* **For production:** See our [deployment guide](README-docker.md)

## Quick Installation Guide

For deployment we use [docker](http://docker.com) so you need to have docker
running on the host. ppcr-tralard is a django app so it will help if you have
some knowledge of running a django site.

```
git clone git@github.com:Digital-Prophets/sms-survey-dashboard.git
cd sms-survery-dashboard/deployment
```

```
make build
make permissions
make web
# Wait a few seconds for the DB to start before to running the next command
make migrate
make collectstatic

```

```
make superuser
```