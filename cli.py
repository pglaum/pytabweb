#!/usr/bin/env python3

from argparse import ArgumentParser
from getpass import getpass
from web import db
from models.user import User

parser = ArgumentParser()
parser.add_argument('--create-admin', help='Create an admin account.',
                    action='store_true')

args = parser.parse_args()

if not args.create_admin:
    print('error: no action')
    exit(0)

if args.create_admin:

    username = input('Username: ')
    password = getpass('Password: ')
    password2 = getpass('Repeat password: ')

    if password != password2:
        print('error: passwords do not match')
        exit(1)

    user = User()
    user.username = username
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    print('admin account was created.')
    exit(0)
