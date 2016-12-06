"""adaptable.

A serialization middleware.
"""
from abc import abstractmethod


class _AdapterRegistry(type):
    """Adapter regsitry.

    Attributes:
        adapters (dict): Name, object pairs.
    """

    adapters = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.adapters[name] = new_cls
        return new_cls


class Adapter(metaclass=_AdapterRegistry):
    """Serialization abstraction layer.

    "deserialize" accepts an unvalidated, raw dictionary and returns a
    validated dictionary.  It will likely implement your "view"
    attribute's deserialization functionality.  This method can be as
    simple as calling your view or can require complex field marshaling
    and schema generation.  The method should accept any number of
    keyword arguments that are necessary to complete the operation.

    "serialize" accepts a model instance and returns serialized output.
    Complex marshaling and schema generation can be applied here. This
    method should only ever accept one required "model" argument.

    "fetch_all" should return a list of model instances that were
    retrieved by a "select" query operation.

    "fetch_one" should return a model instance that was retrieved by a
    "select" query operation.

    "make_query" should accept any number of keyword arguments and
    apply those keyword arguments as query filters. The returned object
    should be a callable capable of communicating with a database and
    returning the desired output.

    Attributes:
        model (object): Model object type.
        view (object): Schema object type.
    """

    model = None
    view = None

    @abstractmethod
    def deserialize(self, form: dict) -> dict:
        """Return a deserialized dictionary.

        Keyword arguments:
            form (dict): Dictionary.
        """
        return

    def deserialize_all(self, forms: list) -> list:
        """Return a set of deserialized dictionaries.

        Keyword arguments:
            forms (list): List of dictionaries.
        """
        return [self.deserialize(form) for form in forms]

    @abstractmethod
    def serialize(self, model) -> dict:
        """Return a serialized model object.

        Keyword arguments:
            model: Model class instance.
        """
        return

    def serialize_all(self, models: list) -> list:
        """Return a set of serialized models.

        Keyword arguments:
            models (list): List of model class instances.
        """
        return [self.serialize(model) for model in models]

    def fetch(self, id, **kwargs):
        """Return a model instance.

        A query is constructed from the "make_query" method prior to
        fetching the model instance.

        Keyword arguments:
            id: Unique model identifier.
        """
        query = self.make_query(**kwargs)
        return self.fetch_one(query, id)

    @abstractmethod
    def fetch_compounded(self, id, **kwargs):
        """Return a single-object query including joined relationships.

        Keyword arguments:
            id: Unique model identifier.
            filters (dict): Column, value filter options.
        """
        return

    @abstractmethod
    def fetch_all(self, query) -> list:
        """Return a list of model instances.

        Keyword arguments:
            query: ORM query object.
        """
        return

    @abstractmethod
    def fetch_one(self, query, id):
        """Return a model instance or None.

        Keyword arguments:
            query: ORM query object.
            id: Unique model identifier.
        """
        return

    @abstractmethod
    def make_query(self):
        """Return a query object."""
        return

    @abstractmethod
    def make_models_response(self, models: list):
        """Return a serialized set of model instances.

        Keyword arguments:
            models (list): List of model class instances.
        """
        return

    @abstractmethod
    def make_model_response(self, model):
        """Return a serialized model instance.

        Keyword arguments:
            model: Model class instance.
        """
        return

    @abstractmethod
    def make_collection_response(self, **filters):
        """Return a collection query response type.

        Keyword arguments:
            filters (dict): Column, value filter options.
        """
        return

    @abstractmethod
    def make_single_object_response(self, id, **filters):
        """Return a single-object query response type.

        Keyword arguments:
            id: Unique model identifier.
            filters (dict): Column, value filter options.
        """
        return


def get_adapter(name: str) -> Adapter:
    """Return the requested class or raise.

    Keyword arguments:
        name (str): Adapter class name.
    """
    return _AdapterRegistry.adapters[name]
