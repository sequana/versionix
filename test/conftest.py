import pytest
import versionix.registry as _registry


@pytest.fixture(autouse=True)
def _inject_test_registry_entries():
    """Inject test-only entries into the registry for the duration of each test."""
    test_entries = {
        "for_testing_empty_parsers": {"options": "", "parsers": []},
        "for_testing_no_parsers": {"options": ""},
    }
    _registry.metadata.update(test_entries)
    yield
    for key in test_entries:
        _registry.metadata.pop(key, None)
