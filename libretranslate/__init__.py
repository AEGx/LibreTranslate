def main(*args, **kwargs):
    from .main import main as _main
    return _main(*args, **kwargs)


def manage(*args, **kwargs):
    from .manage import manage as _manage
    return _manage(*args, **kwargs)


__all__ = ["main", "manage"]
