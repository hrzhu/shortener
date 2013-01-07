# -*- coding: utf-8 -*-

import random
import re
from string import digits, letters
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


BASE = digits + letters


def gen_url():
    return ''.join(random.sample(BASE, 3))


def url_to_id(url):
    if re.match(r'[\w]{3}$', url):
        return BASE.find(url[0]) * 62 * 62 + BASE.find(url[1]) * 62 \
            + BASE.find(url[2])

app = Flask('Shortner')
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/shortener.db'
db = SQLAlchemy(app)


class Url(db.Model):
    __tablename__ = 'Urls'
    org = db.Column(db.String, nullable=False)
    short = db.Column(db.Integer, primary_key=True)

    def __init__(self, org, short):
        self.org = org
        self.short = short


if __name__ == '__main__':
    db.create_all(app=app)
    app.run()
