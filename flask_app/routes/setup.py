def init_api(api):
    from .users import users_ns
    from .records import records_ns

    api.add_namespace(users_ns, path='/users')
    api.add_namespace(records_ns, path='/records')