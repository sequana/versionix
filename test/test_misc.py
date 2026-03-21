from versionix import version


def test_version():
    assert isinstance(version, str) and len(version) > 0
