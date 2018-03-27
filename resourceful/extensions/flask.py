"""Flask extension module."""
from flask import jsonify, make_response, request, views

import resourceful


class FlaskResourceful(object):
    """REST API framework."""

    def init_app(self, app):
        """Initialize the flask application instance."""
        self.app = app

    def add_views(self, route, views):
        """Register a set of views to a given route."""
        for view in views:
            self.add_view(route, view, [view._method])

    def add_view(self, route, view, methods):
        """Register a view to a route."""
        view_func = view.as_view('{}{}'.format(route, methods))
        self.app.add_url_rule(route, view_func=view_func, methods=methods)


class FlaskResourcefulView(resourceful.View, views.View):
    """Flask integrated resourceful view."""

    @property
    def context(self):
        """Return a request-local context object."""
        if not hasattr(request, 'resourceful_context'):
            request.resourceful_context = {}
        return request.resourceful_context

    def send_response(self, response, code):
        """Return a HTTP response."""
        return make_response(jsonify(response), code)

    @property
    def __dict__(self):
        """Return a dictionary of the thread-local context."""
        return self.context

    def __getitem__(self, key):
        """Return a thread-local-key's value."""
        return self.context[key]

    def __setitem__(self, key, value):
        """Set a thread-local-key's value."""
        self.context[key] = value

    def __contains__(self, key):
        """Return True if the thread-local-key exists."""
        return key in self.context

    def __len__(self):
        """Return the number of keys in the thread-local context."""
        return len(self.context)

    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        cls.processors = resourceful.resolve_processors(cls)
        return super().as_view(name, *class_args, **class_kwargs)
