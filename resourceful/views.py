"""View module."""
from abc import abstractmethod, abstractproperty

import collections
import contextlib
import resourceful


def resolve_processors(obj):
    processors = collections.defaultdict(list)
    for name in dir(obj):
        with contextlib.suppress(AttributeError):
            attr = getattr(obj, name)
            name = attr.__invokation_type__
            processors[name].append(attr)
    for processor, methods in processors.items():
        processors[processor] = sorted(
            methods, key=lambda x: x.__invokation_priority__, reverse=True)
    return processors


class View:
    """View class."""

    _code = None
    _method = None

    def interleave(self, name, arg, **kwargs):
        for processor in self.processors[name]:
            arg = processor(self, arg, **kwargs)
        return arg


class ReadView(View):
    """Resource read view."""

    _code = 200
    _method = 'GET'


class CreateView(View):
    """Resource create view."""

    _code = 201
    _method = 'POST'


class UpdateView(View):
    """Resource update view."""

    _code = 202
    _method = 'PUT'


class PartialUpdateView(UpdateView):
    """Resource partial update view."""

    _method = 'PATCH'


class DeleteMixin:
    """Common HTTP DELETE request behavior.

    Views inheriting this type will by default accept only the "DELETE"
    method. All "DELETE" requests must return the status code "204".
    """

    _code = 204
    _method = 'DELETE'


class ArchiveView(DeleteMixin, View):
    """Resource archive view."""

    _archive_column = 'is_archived'
    _archive_value = True

    @resourceful.pre_save
    def archive_model(self, model):
        """Return an archived model instance."""
        setattr(model, self._archive_column, self._archive_value)
        return model


class DeleteView(DeleteMixin, View):
    """Resource delete view."""

    def save(self, model):
        """Delete and return "None".

        Delete the model after executing pre-save processors. Post-save
        processors are not invoked for DELETE views.
        """
        model = self.interleave('pre_save', model)
        self.delete_action(model)
