import os
from ApiBase.ApiBase import ApiBase
from commond.commond import Auth
from .middleware import test

version = os.path.basename(os.path.dirname(__file__))

# GET
ApiBase.get(f'/{version}/test', test, ['admin'], Auth.Bearer)
