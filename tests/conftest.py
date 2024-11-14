import pytest

@pytest.fixture(scope="session")
def resources_path(request):
    from os import path

    return path.join(
        request.config.rootpath,
        "tests",
        "resources"
    )