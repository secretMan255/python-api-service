import os
from ApiBase.ApiBase import ApiBase
from commond.commond import Auth
from .middleware import test, onLogin, onLogout

version = os.path.basename(os.path.dirname(__file__))

# GET
ApiBase.get(f'/{version}/test', test, ['admin'], Auth.Bearer)

# POST
ApiBase.post(f'/{version}/login', onLogin, ['admin'], Auth.Bearer)
ApiBase.post(f'/{version}/logout', onLogout, ['admin'], Auth.Cookie)