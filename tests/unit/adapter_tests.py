from adaptable import Adapter, get_adapter
from tests.unit import UnitTestCase


class BaseAdapter(Adapter):
    pass


class AdapterUnitTestCase(UnitTestCase):

    def test_adapter_registry(self):
        """Assert the test adapter has been registered."""
        self.assertTrue(get_adapter('BaseAdapter') == BaseAdapter)

    def test_adapter_registry_invalid_key(self):
        """Assert missing adapters raise a KeyError."""
        try:
            get_adapter('XYZ')
        except KeyError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
