"""Adapter extensions.

Extensions allow for out-of-the-box compatibility with your API
specification of choice.

Currently supported formats:
    - JSONAPI (http://jsonapi.org)
"""
from abc import abstractmethod

from jsonapiquery import JSONAPIQuery
from jsonapiquery.database.sqlalchemy import group_and_remove

from adaptable import Adapter


class JSONAPIAdapter(Adapter):
    """JSONAPI adapter extension.

    Attributes:
        query_options (dict): Option, boolean pairs.
    """

    query_options = {}
    """JSONAPI query options.

    Setting the "can_filter", "can_sort", "can_paginate", and "can_compound"
    keys with a value of `False` will prevent the adapter from allowing those
    behaviors to occur.

    "can_*" values default to True but they can specified explicitly if
    required.
    """

    def __init__(self, base_url='', parameters={}):
        """Initialize the adapter class.

        Keyword arguments:
            base_url (str): Request URL stripped of its query parameters.
            parameters (dict): Parameter, value pairs.
        """
        self.base_url = base_url
        self.parameters = parameters

    def make_jsonapi(self, model, view) -> JSONAPIQuery:
        """Return a JSONAPI instance.

        Keyword arguments:
            model (object): Model object type.
            view (object): Schema object type.
        """
        return JSONAPIQuery(self.parameters, model, view)

    @abstractmethod
    def make_jsonapi_errors(self, errors: list):
        """Return a JSONAPI error class instance.

        Keyword arguments:
            errors (list): A list of JSONAPI errors.
        """
        return

    def make_models_response(self, models: list) -> dict:
        """Return a set of JSONAPI serialized models.

        Keyword arguments:
            models (list): List of model class instances.
        """
        return {'data': self.serialize_all(models)}

    def make_model_response(self, model) -> dict:
        """Return a JSONAPI serialized model.

        Keyword arguments:
            model: Model class instance.
        """
        return {'data': self.serialize(model)}

    def make_collection_response(self, **kwargs) -> dict:
        """Return a JSONAPI formatted collection response.

        If configured through the "query_options" attribute, this
        method may filter, sort, compound and paginate the document.

        Keyword arguments:
            kwargs (dict): Dictionary of query restrictions.
        """
        jsonapi = self.make_jsonapi(self.model, self.view)
        query, total, selects, schemas = jsonapi.make_query(
            self.make_query(**kwargs), self.query_options)

        models = self.fetch_all(query)
        models = group_and_remove(models, selects + [self.model])

        response = self.make_models_response(models.pop())
        response = jsonapi.make_included_response(response, models, schemas)
        response = jsonapi.make_paginated_response(
            response, self.base_url, total)
        return response

    def make_single_object_response(self, id, **kwargs) -> dict:
        """Return a JSONAPI formatted response object.

        If configured through the "query_options" attribute, the
        document may be compounded.

        Keyword arguments:
            id: Unique model identifier.
            kwargs (dict): Dictionary of query restrictions.
        """
        model, includes, schemas = self.fetch_compounded(id, **kwargs)
        jsonapi = self.make_jsonapi(self.model, self.view)

        response = self.make_model_response(model)
        response = jsonapi.make_included_response(response, includes, schemas)
        return response

    def fetch_compounded(self, id, **kwargs):
        """Return a model and the requested joins.

        If configured through the "query_options" attribute, the
        query may join and return related models.

        Keyword arguments:
            id: Unique model identifier.
            kwargs (dict): Dictionary of query restrictions.
        """
        query = self.make_query(**kwargs)
        jsonapi = self.make_jsonapi(self.model, self.view)

        selects = []
        schemas = []
        if self.query_options.get('can_compound', True):
            query, selects, schemas, errors = jsonapi.include(query)
            if errors:
                raise self.make_jsonapi_errors(errors)

        result = self.fetch_one(query, id)
        includes = group_and_remove([result], selects + [self.model])
        return includes.pop()[0], includes, schemas
