# api/resources/users.py
from resourceful import decorators, views
from resourceful.extensions.flask import FlaskResourcefulView


class UsersViewMixin(FlaskResourcefulView):
    pass


class ReadView(views.ReadView):
    model = None

    def dispatch_request(self, **uri_args):
        query = None

        # Fetch a model while interleaving pre- and post-processors.
        query = self.interleave('pre_fetch', query, **uri_args)
        model = self.fetch_model(query)
        model = self.interleave('post_fetch', model)

        # Dump a model while interleaving pre- and post-processors.
        model = self.interleave('pre_dump', model)
        data = self.dump_model(model)
        data = self.interleave('post_dump', model)

        return self.send_response(data, self._code)

    def dump_model(self, model):
        return model

    def fetch_model(self, query):
        return query


class BrowseUsersView(UsersViewMixin, ReadView):

    @decorators.pre_fetch
    def filter_by_uri_args(self, query, **uri_args):
        return query.filter_by(**uri_args)


class DetailUserView(UsersViewMixin, ReadView):

    @decorators.pre_fetch
    def ignore_this_method(self, query, **uri_args):
        return {'user_id': 1}

    @decorators.post_fetch
    def raise_if_not_first_user(self, model):
        if model['user_id'] != 1:
            raise Exception('You\'re not the first user!')
        return model


class CreateUsersView(UsersViewMixin, views.CreateView):

    @decorators.pre_load
    def set_first_name(self, request_data):
        request_data['data']['attributes']['first-name'] = 'George'
        return request_data

    @decorators.post_load
    def set_last_name(self, request_data):
        request_data['last_name'] = 'Micheal'
        return request_data

    @decorators.post_load
    def set_run_task(self, request_data):
        self['run_task'] = request_data.pop('should_run_task')
        return request_data


class UpdateUsersView(UsersViewMixin, views.UpdateView):

    @decorators.pre_save
    def save_the_model_as_belonging_to_account(self, model):
        model.account_id = 1
        return model

    @decorators.post_save
    def run_task_from_previous_operation(self, model):
        if self['run_task']:
            from tasks import some_task
            some_task.delay(id=model.id)
        return model

    @decorators.pre_dump
    def encode_the_id_as_a_shortuuid(self, model):
        model.id = self.__encode_shortuuid(model.id)
        return model

    @decorators.post_dump
    def lie_to_the_user_about_the_archival_status(self, response_data):
        response_data['data']['attributes']['is_archived'] = False
        return response_data


class DeleteUserView(UsersViewMixin, views.DeleteView):
    pass



# factory.py
from flask import Flask
from resourceful.extensions.flask import FlaskResourceful

app = Flask(__name__)
api = FlaskResourceful()
api.init_app(app)



# routes.py
api.add_views('/users', [BrowseUsersView, CreateUsersView])
api.add_views('/users/<id>', [DetailUserView, UpdateUsersView, DeleteUserView])

api.add_view('/users/<id>', UpdateUsersView, methods=['POST'])



# None
with app.app_context():
    response = app.test_client().get('users/1')
    print(response.data.decode('utf-8'))
