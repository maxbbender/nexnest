# NextNest LLC

Database
======
We are going to use Postgres for our backend. If you don't have it installed.... then figure it out :)

## User Setup
We are going to need 3 different users to keep permissions segmented in the database. Development and Test are to only be used on local machines, any production machine needs to have passwords for database stored in a different place, not in this directory.

While developing we will only need 2 users, the test and development. Don't bother creating the production one until we need it.

[Postgres Create User](https://www.postgresql.org/docs/current/static/app-createuser.html)

1. nextnest_development

`createuser -U postgres -h localhost -E -p 5432 -d -w nextnest_development`

`sudo -u postgres psql -U postgres -c "alter user nextnest_development with password 'domislove';"`

2. nextnest_test

`createuser -U postgres -h localhost -E -p 5432 -d -w nextnest_test`

`sudo -u postgres psql -U postgres -c "alter user nextnest_test with password 'domislove';"`

## Database Setup

1. nextnest_development

`createdb -U nextnest_development -O nextnest_development -h localhost -p 5432 nextnest_development`

2. nextnest_test

`createdb -U nextnest_test -O nextnest_test -h localhost -p 5432 nextnest_test`



