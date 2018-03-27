from nose.tools import assert_raises
from unittest import TestCase

from resourceful.serializer import *


class SerializerTestCase(TestCase):

    def test_get_serializer(self):
        """Test fetching a serializer from the registry."""
        class TestSerializer(Serializer):
            pass
        self.assertTrue(get_serializer('TestSerializer') == TestSerializer)

    def test_get_unknown_serializer(self):
        """Test fetching an undefined serializer."""
        assert_raises(KeyError, get_serializer, 'ABC')

    def test_serializer_deserialize_all(self):
        """Test calling deserialize_all method."""
        class TestSerializer(Serializer):
            def deserialize(self, form, many, **kwargs):
                return form, many, kwargs

        form, many, kwargs = TestSerializer().deserialize_all('test', a=1, b=2)
        self.assertTrue(form == 'test')
        self.assertTrue(many is True)
        self.assertTrue(kwargs == {'a': 1, 'b': 2})

    def test_serializer_serialize_all(self):
        """Test calling serialize_all method."""
        class TestSerializer(Serializer):
            def serialize(self, model, many, **kwargs):
                return model, many, kwargs

        model, many, kwargs = TestSerializer().serialize_all('test', a=1, b=2)
        self.assertTrue(model == 'test')
        self.assertTrue(many is True)
        self.assertTrue(kwargs == {'a': 1, 'b': 2})
