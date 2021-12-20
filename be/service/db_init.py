from be.dao.user import User
from be.dao.book import Book
from be.dao.store import Store
from be.dao.orderform import Orderform
import pymysql
import click
from flask.cli import with_appcontext

@click.command('init-db')
@with_appcontext
def init_db_command():
    Orderform().drop_table()
    Store().drop_table()
    Book().drop_table()
    User().drop_table()
    
    User().create_table()
    Book().create_table()
    Store().create_table()
    Orderform().create_table()

    try:
        Book().create_index()
        Store().create_index()
        Orderform().create_index()
    except pymysql.Error as e: # 1061 means that you cannot create duplicate index
        print(e.args[0])

    click.echo('Initialized the database.')

def init_app(app):
    app.cli.add_command(init_db_command)