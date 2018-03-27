from unittest import TestCase

from resourceful.decorators import *
from resourceful.views import *


class ViewsTestCase(TestCase):

    def test_read_view(self):
        """Test ReadView HTTP interactions."""
        self.assertTrue(ReadView._method == 'GET')
        self.assertTrue(ReadView._code == 200)

    def test_create_view(self):
        """Test CreateView HTTP interactions."""
        self.assertTrue(CreateView._method == 'POST')
        self.assertTrue(CreateView._code == 201)

    def test_update_view(self):
        """Test UpdateView HTTP interactions."""
        self.assertTrue(UpdateView._method == 'PUT')
        self.assertTrue(UpdateView._code == 202)

    def test_partial_update_view(self):
        """Test PartialUpdateView HTTP interactions."""
        self.assertTrue(PartialUpdateView._method == 'PATCH')
        self.assertTrue(PartialUpdateView._code == 202)

    def test_archive_view(self):
        """Test ArchiveView HTTP interactions."""
        self.assertTrue(ArchiveView._method == 'DELETE')
        self.assertTrue(ArchiveView._code == 204)

    def test_delete_view(self):
        """Test DeleteView HTTP interactions."""
        self.assertTrue(DeleteView._method == 'DELETE')
        self.assertTrue(DeleteView._code == 204)
