# -*- coding: utf-8 -*-

import random
import re
from string import digits, letters
from flask import Flask, redirect, flash, url_for, render_template, request, \
    session, abort
from werkzeug.routing import BaseConverter
from flask_sqlalchemy import SQLAlchemy


BASE = digits + letters


def gen_url():
    return ''.join(random.sample(BASE, 3))


def url_to_id(url):
    if re.match(r'[\w]{3}$', url):
        return BASE.find(url[0]) * 62 * 62 + BASE.find(url[1]) * 62 \
            + BASE.find(url[2])


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app = Flask('Shortner')
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shortener.db'
app.secret_key = 'DEV'
app.url_map.converters['regex'] = RegexConverter
db = SQLAlchemy(app)


class Url(db.Model):
    __tablename__ = 'Urls'
    long_url = db.Column(db.String, nullable=False)
    short_url_id = db.Column(db.Integer, nullable=False,
                             primary_key=True, autoincrement=False)

    def __init__(self, long_url, short_url_id):
        self.long_url = long_url
        self.short_url_id = short_url_id


@app.route("/")
def shorten():
    url = None
    if session.get('url'):
        url = session['url']
        session.pop('url', None)
    return render_template("shortener.html", url=url)


@app.route('/<regex("[\w]{3}$"):url>')
def redirect_url(url):
    long_url = Url.query.get(url_to_id(url))
    if long_url:
        return redirect(long_url.long_url)
    else:
        return abort(404)

@app.route("/shorten", methods=['POST'])
def shorten_url():
    if request.form['text']:
        long_url = request.form['text']
        short_url = gen_url()
        session['url'] = short_url
        short_url_id = url_to_id(short_url)
        url = Url(long_url, short_url_id)
        db.session.add(url)
        db.session.commit()
        flash("Url is sucessfully shortened to")
    return redirect(url_for('shorten'))

if __name__ == '__main__':
    db.create_all(app=app)
    app.run()
