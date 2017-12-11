"""Tests and documents use of the Web UI
Any client must make this type of request to Web UI
Made from Flask testing docs
http://flask.pocoo.org/docs/0.12/testing/
"""
import os
import unittest

import sentinela.app as app


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Ativar esta variável de ambiente na inicialização
        # do Servidor WEB para transformar em teste de integração
        self.http_server = os.environ.get('HTTP_SERVER')
        if self.http_server is not None:
            from webtest import TestApp
            self.app = TestApp(self.http_server)
        else:
            app.app.testing = True
            self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_not_found(self):
        if self.http_server is None:
            rv = self.app.get('/non_ecsiste')
            assert b'404 Not Found' in rv.data

    def data(self, rv):
        if self.http_server is not None:
            return rv.html
        return rv.data

    def test_home(self):
        rv = self.app.get('/')
        data = self.data(rv)
        assert b'AJNA' in data

    def test_upload_file(self):
        rv = self.app.get('/upload_file')
        data = self.data(rv)
        assert b'input type="file"' in data
        rp = self.app.post('/upload_file', data={'file': ''})
        self.assertTrue(rp.status_code == 302)
        data = self.data(rp)
        assert b'Redirecting...' in data

    def test_listfiles(self):
        rv = self.app.get('/list_files')
        data = self.data(rv)
        assert b'input type="file"' in data

    def test_importa(self):
        rv = self.app.get('/importa')
        data = self.data(rv)
        assert b'Redirecting...' in data

    def test_risco(self):
        rv = self.app.get('/risco?base=1')
        data = self.data(rv)
        print(data)
        assert b'Lista de Riscos' in data

    def _post(self, url, data):
        rv = self.app.post(url, data=data, follow_redirects=True)
        print(rv)


"""
    # Gerar arquivos para poder fazer este teste automático
    def test_aplica_risco(self):
        rv = self.app.get('/aplica_risco?filename=../tests&base=1')
        print(rv)
        # assert b'tests.zip' in rv.data
        assert b'<select name="base"' in rv.data
"""
