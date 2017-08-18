# NextNest LLC

Database
======
We are going to use Postgres for our backend. If you don't have it installed.... then figure it out :)

## User Setup
We are going to need 3 different users to keep permissions segmented in the database. Development and Test are to only be used on local machines, any production machine needs to have passwords for database stored in a different place, not in this directory.

While developing we will only need 2 users, the test and development. Don't bother creating the production one until we need it.

[Postgres Create User](https://www.postgresql.org/docs/current/static/app-createuser.html)

**nextnest_development**

`createuser -U postgres -h localhost -E -p 5432 -d -w nexnest_development`

`sudo -u postgres psql -U postgres -c "alter user nexnest_development with password 'domislove';"`

**nextnest_test**

`createuser -U postgres -h localhost -E -p 5432 -d -w nexnest_test`

`sudo -u postgres psql -U postgres -c "alter user nexnest_test with password 'domislove';"`

## Database Setup

**nextnest_development**

`createdb -U nexnest_development -O nexnest_development -h localhost -p 5432 nexnest_development`

**nextnest_test**

`createdb -U nexnest_test -O nexnest_test -h localhost -p 5432 nexnest_test`

Vagrant
=======
Vagrant allows us to develop in the same environment as well as giving Kyle the ability to influence our environment with whatever he has set up for produciton.

1. First install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)!
2. Then install [Vagrant](https://www.vagrantup.com/downloads.html) :)

Make sure you have CPU virtualization turned on in your BIOS. Usually it is turned off by default.

***THIS IS IMPORTANT!!!*** You must use a bash cli with SSH capabilities. The easiest way to do this is just use [GitBash](https://git-scm.com/downloads)

## Vagrant Initialization
1. `cd` into the project directory on your computer
2. type `vagrant up`, this will boot a virtual machine
3. Once that is done running ssh into the machine by typing `vagrant ssh`
4. cd to our mounted project directory at `/vagrant` so ... `cd /vagrant`
5. Type `make install` to install all the python packages and initialize our database!


Production Setup
======
`git remote add stage ssh://nexnest@dev.nexnest.com/home/nexnest/nexnest`



Environment Variables
======
These are going to be the environment variables that we are going to need to implement in the Unit file on the production server

MAIL_USERNAME
