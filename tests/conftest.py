import pytest

def pytest_collection_modifyitems(items, config):
    """
    Deselects tests that are parametrized with the 'trio' backend.
    """
    supported_backends = ["asyncio"]
    deselected = []
    for item in items:
        if hasattr(item, "callspec") and "anyio_backend" in item.callspec.params:
            backend = item.callspec.params["anyio_backend"]
            if backend not in supported_backends:
                deselected.append(item)

    items[:] = [item for item in items if item not in deselected]
    config.hook.pytest_deselected(items=deselected)
