"""jsonapiquery extension module."""
from abc import abstractmethod, abstractproperty
from jsonapiquery.database.sqlalchemy import include

import resourceful


class CompoundDocumentMixin(object):
    """jsonapiquery library mixin class.

    Adds handling for JSONAPI related querying and response
    construction. Response construction relies on the serializer being
    used to be JSONAPI compliant. It is recommended that your
    serializer implements "marshmallow-jsonapi" or another JSONAPI
    compliant serialization library.
    """

    query_options = {}

    @abstractproperty
    def jsonapi(self):
        """Return a "JSONAPIQuery" instance."""
        return None

    @abstractproperty
    def session(self):
        """Return a database session."""
        return None

    @abstractmethod
    def raise_jsonapi_errors(self, errors):
        """Raise JSONAPI related errors."""
        return None

    @resourceful.post_dump
    def compound_response(self, response):
        """Return a compound document."""
        may_include = self.query_options.get('may_include', True)
        if not may_include:
            return response

        if not isinstance(response, dict):
            return response

        wrapper = response.get('data')
        if isinstance(wrapper, dict):
            model_ids = [wrapper.get('id')]
        elif isinstance(wrapper, list):
            model_ids = [obj.get('id') for obj in wrapper]
        else:
            return response

        fields, errors = self.jsonapi.make_include_fields()
        if errors:
            return self.raise_jsonapi_errors(errors)

        mappers, selects, schemas = self.jsonapi.make_query_includes(fields)
        models = include(self.session, self.model, selects, mappers, model_ids)
        models = self._remove_null_values(models)
        return self.jsonapi.make_included_response(response, models, schemas)


class QueryMixin(CompoundDocumentMixin):
    """JSONAPI collection handling mixin class."""

    @abstractproperty
    def pagination_url(self):
        """Return a URL to paginate with."""
        return None

    def filter_query(self, query, errors):
        """Return a filtered query set."""
        may_filter = self.query_options.get('may_filter', True)
        if may_filter:
            return self.jsonapi.filter(query, errors)
        return query, []

    def sort_query(self, query, errors):
        """Return a sorted query set."""
        may_sort = self.query_options.get('may_sort', True)
        if may_sort:
            return self.jsonapi.sort(query, errors)
        return query, []

    def paginate_query(self, query, errors):
        """Return a paginated query set."""
        may_paginate = self.query_options.get('may_paginate', True)
        if may_paginate:
            return self.jsonapi.paginate(query, errors)
        return query, []

    @resourceful.pre_fetch(-1)
    def apply_jsonapi_args(self, query, **kwargs):
        """Return a filtered, sorted, and paginated query."""
        errors = []
        query, errs = self.filter_query(query, errors)
        errors.extend(errs)
        query, errs = self.sort_query(query, errors)
        errors.extend(errs)
        query, total, errs = self.paginate_query(query, errors)
        errors.extend(errs)

        self.pagination_total = total

        if errors:
            return self.raise_jsonapi_errors(errors)
        return query

    @resourceful.post_dump
    def paginate_response(self, response):
        """Return a paginated document."""
        response = self.jsonapi.make_paginated_response(
            response, self.pagination_url, self.pagination_total)
        return response
