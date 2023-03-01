import os
from importlib import import_module


def _import_routes():
    """ USER MANAGEMENT """

    modules = [
        'controllers.auth_routes',
        # 'controllers.member_routes',
        # 'controllers.payment_routes',
        # 'controllers.provider_routes',
        # 'controllers.callback_routes',
        # 'controllers.system_routes',
        # 'controllers.follow_routes',
        # 'controllers.game_routes',
        # 'controllers.task_routes',
        # 'controllers.transaction_routes',
        # 'controllers.article_routes',
    ]

    if os.environ.get('ENVIRONMENT') in {'develop', 'release'}:
        modules.append('controllers.dev_routes')

    for module in modules:
        import_module(module)


def _import_api_render_template():
    import_module('common.api_render_template')


def register_views():
    _import_routes()
    _import_api_render_template()
