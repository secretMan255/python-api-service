import os
from ApiBase.ApiBase import ApiBase
from commond.commond import Auth
from .middleware import test, onLogin, onLogout, onGetProducts, onUpdateProductDescribe, onUpdateProductPerantId, onUpdateProductDetail, onUpdateProductStatus, onDeleteProduct, onAddProduct

version = os.path.basename(os.path.dirname(__file__))

# GET
ApiBase.get(f'/{version}/test', test, ['admin'], Auth.Bearer)
ApiBase.get(f'/{version}/products', onGetProducts, ['admin'], Auth.Bearer)

# POST
ApiBase.post(f'/{version}/login', onLogin, ['admin'], Auth.Bearer)
ApiBase.post(f'/{version}/logout', onLogout, ['admin'], Auth.Cookie)
ApiBase.post(f'/{version}/update/product/describe', onUpdateProductDescribe, ['admin'], Auth.Cookie)
ApiBase.post(f'/{version}/update/product/detail', onUpdateProductDetail, ['admin'], Auth.Cookie)
ApiBase.post(f'/{version}/update/product/status', onUpdateProductStatus, ['admin'], Auth.Cookie)
ApiBase.post(f'/{version}/delete/product', onDeleteProduct, ['admin'], Auth.Cookie)
ApiBase.post(f'/{version}/update/product/parentId', onUpdateProductPerantId, ['admin'], Auth.Cookie)
ApiBase.post(f'/{version}/add/product', onAddProduct, ['admin'], Auth.Cookie)
