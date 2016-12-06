from jsonapiquery import JSONAPIQuery
from jsonapiquery.drivers.model import SQLAlchemyDriver
from jsonapiquery.drivers.view import MarshmallowDriver


class JSONAPI(JSONAPIQuery):
    model_driver = SQLAlchemyDriver
    view_driver = MarshmallowDriver

    def make_errors(self, errors):
        """Return an "Exception" instance."""
        return Exception(errors)

    def serialize_included(self, schema, models):
        """Return serialized output.

        For included responses, we only want to include "id" and "type"
        fields. This method of inclusion is obviously contrived. More
        flexibility can be found by offloading this hard coded behavior
        to the schema. By using a request context, in the case of flask,
        the method can key off the request URL and return an adapter
        based on the API being accessed.
        """
        adapter = schema.get_adapter(simplified=True)()
        return adapter.serialize_all(models)
