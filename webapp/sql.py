# -*- coding: utf-8 -*-

CREATE = {
    'users': """
CREATE TABLE IF NOT EXISTS users_t (
    login_id INTEGER PRIMARY KEY,
    login TEXT,
    passwd_hash BINARY
)
    """,

    'video': """
CREATE TABLE IF NOT EXISTS video_t (
    video_id INTEGER PRIMARY KEY,
    video_path TEXT,
    source_name TEXT,
    comment TEXT
)
    """
}

INSERT = {
    'users': 'INSERT INTO users_t (login, passwd_hash) VALUES(?, ?)',
    'video': '\
INSERT INTO video_t (video_path, source_name, comment) VALUES(?, ?, ?)',
}

SELECT = {
    'users': 'SELECT passwd_hash FROM users_t WHERE login = ?',
    'video': 'SELECT video_id, video_path, comment FROM video_t',
}
