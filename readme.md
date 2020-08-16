## Requirements

```sh
$ sudo apt install python3-venv python3-pip
$ python3 -m venv env
$ . env/bin/activate
$ pip3 install -r requirements.txt
```

## Set up database

```sh
$ sudo apt install postgresql
$ sudo -u postgres psql postgres
postgres=# create database myblog;
postgres=# create user myblog with password 'myblog';
postgres=# alter role myblog set client_encoding to 'utf8';
postgres=# alter role myblog set default_transaction_isolation to 'read committed';
postgres=# alter role myblog set timezone to 'UTC';
postgres=# grant all privileges on database myblog to myblog;
postgres=# \q
```

## Docs

- [РПЗ](https://github.com/wcdbmv/DBC/blob/master/doc/build/note.pdf)
- [Presentation](https://docs.google.com/presentation/d/10508dnoIA5MAv8JEQQX-3zi0mu6ep02MGNGiBs9mBzQ/edit?usp=sharing)
