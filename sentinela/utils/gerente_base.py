"""GerenteBase abstrai a necessidade de conhecer a estrutura das bases
ou utilizar comandos mais avançados. Transforma a estrutura em dicts
mais fáceis de lidar
Usa reflection para navegar nos modelos
"""
import csv
import importlib
import inspect
import os
from collections import defaultdict

from sentinela.conf import APP_PATH, CSV_FOLDER, CSV_FOLDER_TEST

PATH_MODULOS = os.path.join(APP_PATH, 'models')


class Filtro:
    def __init__(self, field, tipo, valor):
        self.field = field
        self.tipo = tipo
        self.valor = valor


class GerenteBase:
    """Métodos para padronizar a manipulação de bases de dados
     no modelo do sistema sentinela"""

    def set_path(self, path, test=False):
        """Lê a estrutura de 'tabelas' de uma pasta de csvs importados"""
        PATH_BASE = os.path.join(CSV_FOLDER, path)
        if test:
            PATH_BASE = os.path.join(CSV_FOLDER_TEST, path)
        files = sorted(os.listdir(PATH_BASE))
        self.dict_models = defaultdict(dict)
        for file in files:
            with open(os.path.join(PATH_BASE, file), 'r',
                      encoding='latin1', newline='') as arq:
                reader = csv.reader(arq)
                cabecalhos = next(reader)
                campos = [campo for campo in cabecalhos]
                self.dict_models[file[:-4]]['campos'] = campos

    def set_module(self, model, db=None):
        """Lê a estrutura de 'tabelas' de um módulo SQLAlchemy"""
        self.module_path = 'sentinela.models.' + model
        module = importlib.import_module(self.module_path)
        classes = inspect.getmembers(module, inspect.isclass)
        self.dict_models = defaultdict(dict)
        for i, classe in classes:
            if classe.__module__.find('sentinela.models') != -1:
                campos = [i for i in classe.__dict__.keys() if i[:1] != '_']
                self.dict_models[classe.__name__]['campos'] = sorted(campos)
        SessionClass = getattr(module, 'MySession')
        if db:
            self.dbsession = SessionClass(nomebase=db).session
        else:
            self.dbsession = SessionClass().session

    def set_session(self, adbsession):
        self.dbsession = adbsession

    def filtra(self, base, filters, return_query=False):
        module = importlib.import_module(self.module_path)
        aclass = getattr(module, base)
        q = self.dbsession.query(aclass)
        print('filters ', filters)
        for afilter in filters:
            afield = getattr(aclass, afilter.field)
            print('field', afield)
            print('valor', afilter.valor)
            q = q.filter(afield == afilter.valor)
        if return_query:
            return q
        onerow = q.first()
        result = []
        if onerow:
            result.append([key for key in onerow.to_dict.keys()])
            result_list = [row.to_list for row in q.all()]
            result.extend(result_list)
        return result

    @property
    def list_models(self):
        if self.dict_models is None:
            return None
        return self.dict_models.keys()

    @property
    def list_modulos(self):
        lista = [filename[:-3] for filename in os.listdir(PATH_MODULOS)
                 if filename.find('.py') != -1]
        return sorted(lista)

    def busca_paiarvore(self, ainstance):
        try:
            if ainstance.pai:
                return self.busca_paiarvore(ainstance.pai)
        except AttributeError:
            pass
        return ainstance

    def recursive_tree(self, ainstance, recursive=True):
        result = []
        result.append('<ul class="tree">')
        result.append('<li>' + type(ainstance).__name__ + '</li><ul>')
        lista = ['<li>' + str(key) + ': ' + str(value) + '</li>'
                 for key, value in ainstance.to_dict.items()]
        result.extend(lista)
        filhos = getattr(ainstance, 'filhos', None)
        if filhos:
            for arvore_filho in filhos:
                if recursive:
                    if isinstance(arvore_filho, list):
                        for filho in arvore_filho:
                            result.extend(
                                self.recursive_tree(filho)
                            )
                            result.append('</ul>')
                    else:
                        result.extend(
                            self.recursive_tree(arvore_filho)
                        )
                        result.append('</ul>')
                else:
                    result.append('<ul>')
                    if isinstance(arvore_filho, list):
                        for filho in arvore_filho:
                            result.append('<li><a href="#" id="' + filho.id +
                                          '">' + type(filho).__name__ +
                                          '</a></li>')
                    else:
                        result.append('<li><a href="#" id="' +
                                      arvore_filho.id +
                                      '">' + type(filho).__name__ +
                                      '</a></li>')
                    result.append('</ul>')

        result.append('</ul>')
        return result
