from adaptable import _AdapterRegistry, Adapter, get_adapter, get_adapter_subset
from tests.unit import UnitTestCase


class BaseAdapter(Adapter):
    pass


class AdapterUnitTestCase(UnitTestCase):

    def test_adapter_registry(self):
        """Assert the test adapter has been registered."""
        self.assertTrue(
            get_adapter('tests.unit.adapter_tests.BaseAdapter') == BaseAdapter)

    def test_adapter_registry_subset(self):
        self.assertTrue('adaptable.Adapter' in _AdapterRegistry.adapters)

        subset = get_adapter_subset('tests.unit')
        self.assertTrue('adaptable.Adapter' not in subset)

        try:
            get_adapter('Adapter', subset)
            self.assertTrue(False)
        except KeyError:
            self.assertTrue(True)

        adapter = get_adapter('BaseAdapter', subset)
        self.assertTrue(adapter is not None)

    def test_adapter_registry_invalid_key(self):
        """Assert missing adapters raise a KeyError."""
        try:
            get_adapter('XYZ')
        except KeyError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
