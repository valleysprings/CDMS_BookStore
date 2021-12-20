import requests
import threading
from urllib.parse import urljoin
from fe import conf
from be.service import db_init
from be import create_app
import click

thread: threading.Thread = None

def run_backend():
    # rewrite this if rewrite backend
    app = create_app()
    app.run()
    runner = app.test_cli_runner()
    result = runner.invoke(args=['init-db'])
    assert 'Initialized the database.' in result.output

def pytest_configure(config):
    global thread
    print("frontend begin test")
    thread = threading.Thread(target=run_backend)
    thread.start()

def pytest_unconfigure(config):
    url = urljoin(conf.URL, "shutdown")
    requests.get(url)
    thread.join()
    print("frontend end test")
