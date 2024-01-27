def init_api(api):
    from .users import api as users_ns

    api.add_namespace(users_ns, path='/users')