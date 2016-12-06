from adaptable import get_adapter
from marshmallow_jsonapi import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    parent = fields.Relationship(
        include_resource_linkage=True, type_='users', schema='UserSchema')

    class Meta:
        type_ = 'users'

    def get_adapter(self, simplified=False):
        """Return an adapter object.

        This method of retrieval is contrived. In a real world use case,
        you might want to return an adapter based on the URL requested.
        Different APIs or different API versions could return
        different fields from one another.  By coupling to something like
        a flask request context, this method can be converted to a
        property and intelligently return based on the conditions of the
        request.
        """
        if simplified:
            return get_adapter('SimplifiedResponseAdapter')
        return get_adapter('UserAdapter')
