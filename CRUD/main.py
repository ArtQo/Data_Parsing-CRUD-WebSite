from bottle import route, run, template, request
import pymysql
import configparser

from bs4 import BeautifulSoup
import requests

config = configparser.ConfigParser()
config.read('pymysql.ini', encoding='utf-8-sig')


@route('/news_data/')
def news_main_page():
    return template('news_data_main')

@route('/news_data/search_menu/')
def news_main_page():
    return template('news_data_search_menu')

@route('/news_data/all/')
def show_all():
    conn = pymysql.connect(host=config.get('py_sql', 'host'),
                           user=config.get('py_sql', 'user'),
                           password=config.get('py_sql', 'password'),
                           db=config.get('py_sql', 'db'))
    c = conn.cursor()
    c.execute('SELECT id, Article, Pre_Body, Link FROM news_data_RT')
    rows = c.fetchall()
    conn.close()
    return template('news_data_all', rows=rows)


@route('/news_data/<id>/')
def news_find_id(id):
    conn = pymysql.connect(host=config.get('py_sql', 'host'),
                           user=config.get('py_sql', 'user'),
                           password=config.get('py_sql', 'password'),
                           db=config.get('py_sql', 'db'))
    c = conn.cursor()
    c.execute("SELECT id, Article, Pre_Body, Link FROM news_data_RT WHERE id = %s", (id,))
    result = c.fetchall()
    conn.close()
    if not result:
        return '<p>This item number does not exist! ID = %s.</p>' \
               '<button onclick="window.location.href = `/news_data/`">Back</button>' % id
    else:
        return template('news_data_id', result=result)
        # return str(result)


@route('/news_data/delete/<id>/')
def news_delete_id(id):
    conn = pymysql.connect(host=config.get('py_sql', 'host'),
                           user=config.get('py_sql', 'user'),
                           password=config.get('py_sql', 'password'),
                           db=config.get('py_sql', 'db'))
    c = conn.cursor()
    c.execute("SELECT id FROM news_data_RT WHERE id = %s", (id,))
    check = c.fetchone()
    if check is None:
        conn.close()
        return '<p>ID doenst exist.</p>' \
               '<button onclick="window.location.href = `/news_data/`">Back</button>'
    else:
        c.execute("DELETE FROM news_data_RT WHERE id = %s;", (id,))
        conn.commit()
        conn.close()
        return '<p>ID has been delete.</p>' \
               '<button onclick="window.location.href = `/news_data/`">Back</button>'


@route('/news_data/create/', method=['POST'])
def news_create():
    if request.POST.save:

        Article = request.POST.Article.strip()
        Pre_Body = request.POST.Pre_Body.strip()
        Link = request.POST.Link.strip()
        conn = pymysql.connect(host=config.get('py_sql', 'host'),
                               user=config.get('py_sql', 'user'),
                               password=config.get('py_sql', 'password'),
                               db=config.get('py_sql', 'db'))
        c = conn.cursor()
        c.execute("INSERT INTO news_data_RT (Article, Pre_Body, Link) VALUES (%s, %s, %s)", (Article, Pre_Body, Link))
        new_id = c.lastrowid
        conn.commit()
        conn.close()
        return '<p>The new task was inserted into the database, the ID is %s</p>' \
               '<button onclick="window.location.href = `/news_data/create/`">Again</button> '\
               '<button onclick="window.location.href = `/news_data/`">Back</button>' % new_id
    else:
        return template('news_data_create')


@route('/news_data/edit/<id>/', method=['GET', 'POST'])
def news_edit_id(id):
    if request.POST.save:
        Article = request.POST.Article.strip()
        Pre_Body = request.POST.Pre_Body.strip()
        Link = request.POST.Link.strip()

        conn = pymysql.connect(host=config.get('py_sql', 'host'),
                               user=config.get('py_sql', 'user'),
                               password=config.get('py_sql', 'password'),
                               db=config.get('py_sql', 'db'))
        c = conn.cursor()
        c.execute("UPDATE news_data_RT SET Article = %s, Pre_Body = %s, Link = %s WHERE id LIKE %s",
                  (Article, Pre_Body, Link, id))
        conn.commit()

        return '<p>The item number %s was successfully updated!</p>' \
               '<button onclick="window.location.href = `/news_data/`">Back</button>' % id
    else:
        conn = pymysql.connect(host=config.get('py_sql', 'host'),
                               user=config.get('py_sql', 'user'),
                               password=config.get('py_sql', 'password'),
                               db=config.get('py_sql', 'db'))
        c = conn.cursor()
        c.execute("SELECT Article, Pre_Body, Link FROM news_data_RT WHERE id LIKE %s", (id,))
        cur_data = c.fetchone()
        conn.close()
        if cur_data is None:
            return '<p>ID doenst exist.</p>' \
                   '<button onclick="window.location.href = `/news_data/`">Back</button>'
        else:
            return template('news_data_edit', old=cur_data, id=id)


@route('/news_data/find_word_like/<word>/')
def news_find_word(word):
    conn = pymysql.connect(host=config.get('py_sql', 'host'),
                           user=config.get('py_sql', 'user'),
                           password=config.get('py_sql', 'password'),
                           db=config.get('py_sql', 'db'))
    c = conn.cursor()
    # c.execute(f'SELECT * FROM news_data_RT WHERE Article LIKE \'%{word}%\'')
    c.execute("SELECT * FROM news_data_RT WHERE Article OR Pre_Body LIKE '%{0}%'".format(word))
    result = c.fetchall()
    conn.close()
    if not result:
        return '<p>This item word does not exist!</p>' \
               '<button onclick="window.location.href = `/news_data/search_menu/`">Again</button> ' \
               '<button onclick="window.location.href = `/news_data/`">Back</button>'
    else:
        return template('news_data_word', result=result)

@route('/news_data/find_word_not_like/<word1>&<word2>/')
def news_find_different_word(word1, word2):
    conn = pymysql.connect(host=config.get('py_sql', 'host'),
                           user=config.get('py_sql', 'user'),
                           password=config.get('py_sql', 'password'),
                           db=config.get('py_sql', 'db'))
    c = conn.cursor()
    c.execute("SELECT * FROM news_data_RT WHERE Article LIKE '%{0}%' AND Article NOT LIKE '%{1}%' OR Pre_Body LIKE '%{0}%' AND Pre_Body NOT LIKE '%{1}%'".format(word1, word2))
    result = c.fetchall()
    conn.close()
    if not result:
        return '<p>This item word does not exist!</p>' \
               '<button onclick="window.location.href = `/news_data/search_menu/`">Again</button> ' \
               '<button onclick="window.location.href = `/news_data/`">Back</button>'
    else:
        return template('news_data_word', result=result)

run()
