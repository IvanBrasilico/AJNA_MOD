"""Exemplo de utilização no sistema CARGA.
Teste funcional simulando utilização com uma base "real".
A base é uma base do Sistema Siscomex Carga modificada por questões de sigilo.
"""
import unittest
import tempfile
import os

from sentinela.models.models import (Base, Filtro, MySession, ParametroRisco,
                                     ValorParametro)
from sentinela.utils.csv_handlers import muda_titulos_csv
from sentinela.utils.gerente_risco import GerenteRisco

PLANILHA_TEST = '/home/ivan/Downloads/planilhaBTP.csv'


class TestModel(unittest.TestCase):
    def setUp(self):
        mysession = MySession(Base, test=True)
        self.session = mysession.session
        self.engine = mysession.engine
        Base.metadata.create_all(self.engine)
        self.tmpdir = tempfile.mkdtemp()
        # Ensure the file is read/write by the creator only
        self.saved_umask = os.umask(0o077)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
        os.umask(self.saved_umask)
        os.rmdir(self.tmpdir)

    def test_planilhas(self):
        pass