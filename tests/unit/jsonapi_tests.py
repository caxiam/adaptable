from sqlalchemy.orm import Query, sessionmaker
from jsonapiquery.database.sqlalchemy import QueryMixin

from adaptable.extensions import JSONAPIAdapter
from tests.unit import UnitTestCase
from tests.jsonapi import JSONAPI
from tests.marshmallow import UserSchema
from tests.sqlalchemy import SQLAlchemyTestMixin, UserModel


def make_session(engine):
    class BaseQuery(QueryMixin, Query):
        pass
    return sessionmaker(bind=engine, query_cls=BaseQuery)()


class UserAdapter(JSONAPIAdapter):
    fields = ('id', 'name', 'parent')
    model = UserModel
    view = UserSchema

    def deserialize(self, form):
        result, errors = self.view(only=self.fields).load(form)
        if errors:
            raise Exception(errors)
        return result

    def serialize(self, model):
        return self.view(only=self.fields).dump(model).data['data']

    def fetch_all(self, query):
        return query.all()

    def fetch_one(self, query, id):
        return query.filter(self.model.id == id).first()

    def make_jsonapi(self, model, view):
        return JSONAPI(self.parameters, model, view)

    def make_query(self):
        return session.query(self.model)


class SimplifiedResponseAdapter(UserAdapter):
    fields = ('id',)


class JSONAPIUnitTestCase(SQLAlchemyTestMixin, UnitTestCase):

    def make_session(self):
        global session

        session = make_session(self.engine)
        return session

    def test_serialize_collection(self):
        """Assert a fully marshaled collection is returned."""
        model = UserModel()
        self.session.add(model)

        adapter = UserAdapter()
        response = adapter.make_collection_response()
        print(response)
        self.assertTrue('data' in response)
        self.assertTrue(isinstance(response['data'], list))
        self.assertTrue('id' in response['data'][0])
        self.assertTrue('type' in response['data'][0])
        self.assertTrue('name' in response['data'][0]['attributes'])
        self.assertTrue('parent' in response['data'][0]['relationships'])
        self.assertTrue(len(response['data'][0]) == 4)

    def test_serialize_response(self):
        """Assert a fully marshaled response is returned."""
        model = UserModel()
        self.session.add(model)

        adapter = UserAdapter()
        response = adapter.make_single_object_response(1)
        self.assertTrue('data' in response)
        self.assertTrue('id' in response['data'])
        self.assertTrue('type' in response['data'])
        self.assertTrue('name' in response['data']['attributes'])
        self.assertTrue('parent' in response['data']['relationships'])
        self.assertTrue(len(response['data']) == 4)

    def test_serialize_include(self):
        """Assert a partially marshaling response is included."""
        model = UserModel()
        self.session.add(model)
        model = UserModel(parent=model)
        self.session.add(model)

        adapter = UserAdapter(parameters={'include': 'parent'})
        response = adapter.make_single_object_response(1)

        self.assertTrue('data' in response)
        self.assertTrue('id' in response['data'])
        self.assertTrue('type' in response['data'])
        self.assertTrue('name' in response['data']['attributes'])
        self.assertTrue('parent' in response['data']['relationships'])
        self.assertTrue(len(response['data']) == 4)

        self.assertTrue('included' in response)
        self.assertTrue('id' in response['included'][0])
        self.assertTrue('type' in response['included'][0])
        self.assertTrue(len(response['included'][0]) == 2)
