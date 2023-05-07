import pytest  # pylint: disable=import-error

from cachezilla import CacheZilla


@pytest.fixture()
def cachezilla_object() -> CacheZilla:
    return CacheZilla()
