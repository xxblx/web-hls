#!VENV/bin/python
# -*- coding: utf-8 -*-

import getpass
import sqlite3
import os.path
import argparse

import bcrypt

from webapp.sql import CREATE, INSERT


def create_tables(db_path):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(CREATE['users'])
        cur.execute(CREATE['video'])


def insert_users(db_path, login, passwd_hash):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(INSERT['users'], (login, passwd_hash))


def insert_video(db_path, path, source_name, comment):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(INSERT['video'], (path, source_name, comment))


def main():
    parser = argparse.ArgumentParser(prog='web-hls')
    parser.add_argument('--db', type=str, required=True,
                        help='absolute path to db')

    subparsers = parser.add_subparsers()

    users_parser = subparsers.add_parser('users')
    users_parser.set_defaults(used='users')
    users_parser.add_argument('-l', '--login', type=str, required=True)

    video_parser = subparsers.add_parser('video')
    video_parser.set_defaults(used='video')
    video_parser.add_argument('-p', '--path', type=str, required=True,
                              help='absolute path to m3u8')
    video_parser.add_argument('-n', '--source_name', type=str, required=True,
                              help='video\'s source name')
    video_parser.add_argument('-c', '--comment', type=str, default=None)

    args = parser.parse_args()
    if 'used' not in args:
        return

    if not os.path.exists(args.db):
        create_tables(args.db)

    if args.used == 'users':
        passwd = getpass.getpass()
        passwd_hash = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())
        insert_users(args.db, args.login, passwd_hash)
    elif args.used == 'video':
        insert_video(args.db, args.path, args.source_name, args.comment)


if __name__ == '__main__':
    main()
