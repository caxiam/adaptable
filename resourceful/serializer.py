"""Serialization middleware."""
from abc import abstractmethod


class _SerializerRegistry(type):
    serializers = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.serializers[name] = new_cls
        return new_cls


class Serializer(metaclass=_SerializerRegistry):
    """Serialization abstraction layer.

    "deserialize" accepts an unvalidated, raw dictionary and returns a
    validated dictionary.  It will likely implement your "schema"
    attribute's deserialization functionality.  This method can be as
    simple as calling your view or can require complex field marshaling
    and schema generation.  The method should accept any number of
    keyword arguments that are necessary to complete the operation.

    "serialize" accepts a model instance and returns serialized output.
    Complex marshaling and schema generation can be applied here. This
    method should only ever accept one required "model" argument.

    Attributes:
        fields (iterable): A list or tuple of fields to marshal.
        schema (object): Schema object type.
    """

    fields = None
    schema = None

    @abstractmethod
    def deserialize(self, form, many=False, **schema_args: dict):
        """Return a deserialized dictionary."""
        return

    def deserialize_all(self, form, **schema_args: dict):
        """Return a set of deserialized dictionaries."""
        return self.deserialize(form, many=True, **schema_args)

    @abstractmethod
    def serialize(self, model, many=False, **schema_args: dict):
        """Return a serialized model object."""
        return

    def serialize_all(self, models: list, **schema_args: dict):
        """Return a set of serialized models."""
        return self.serialize(models, many=True, **schema_args)


def get_serializer(name: str) -> Serializer:
    """Return the requested class or raise.

    Keyword arguments:
        name (str): Serializer class name.
    """
    return _SerializerRegistry.serializers[name]
