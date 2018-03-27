from unittest import TestCase

from resourceful.decorators import *


class DecoratorsTestCase(TestCase):

    def test_pre_fetch(self):
        @pre_fetch(-1)
        def test():
            pass

        self.assertTrue(hasattr(test, '__invokation_type__'))
        self.assertTrue(test.__invokation_type__ == 'pre_fetch')
        self.assertTrue(test.__invokation_priority__ == -1)

    def test_post_fetch(self):
        @post_fetch(100)
        def test():
            pass

        self.assertTrue(hasattr(test, '__invokation_type__'))
        self.assertTrue(test.__invokation_type__ == 'post_fetch')
        self.assertTrue(test.__invokation_priority__ == 100)

    def test_pre_load(self):
        @pre_load(23)
        def test():
            pass

        self.assertTrue(hasattr(test, '__invokation_type__'))
        self.assertTrue(test.__invokation_type__ == 'pre_load')
        self.assertTrue(test.__invokation_priority__ == 23)

    def test_post_load(self):
        @post_load(41)
        def test():
            pass

        self.assertTrue(hasattr(test, '__invokation_type__'))
        self.assertTrue(test.__invokation_type__ == 'post_load')
        self.assertTrue(test.__invokation_priority__ == 41)

    def test_pre_save(self):
        @pre_save(67)
        def test():
            pass

        self.assertTrue(hasattr(test, '__invokation_type__'))
        self.assertTrue(test.__invokation_type__ == 'pre_save')
        self.assertTrue(test.__invokation_priority__ == 67)

    def test_post_save(self):
        @post_save(2)
        def test():
            pass

        self.assertTrue(hasattr(test, '__invokation_type__'))
        self.assertTrue(test.__invokation_type__ == 'post_save')
        self.assertTrue(test.__invokation_priority__ == 2)

    def test_pre_dump(self):
        @pre_dump(2)
        def test():
            pass

        self.assertTrue(hasattr(test, '__invokation_type__'))
        self.assertTrue(test.__invokation_type__ == 'pre_dump')
        self.assertTrue(test.__invokation_priority__ == 2)

    def test_post_dump(self):
        @post_dump
        def test():
            pass

        self.assertTrue(hasattr(test, '__invokation_type__'))
        self.assertTrue(test.__invokation_type__ == 'post_dump')
        self.assertTrue(test.__invokation_priority__ == 0)

    def test_tag_processor(self):
        def test():
            pass

        tag_processor(test, 'name')
        self.assertTrue(hasattr(test, '__invokation_type__'))
        self.assertTrue(test.__invokation_type__ == 'name')
        self.assertTrue(test.__invokation_priority__ == 0)

        tag_processor(10, 'name')(test)
        self.assertTrue(hasattr(test, '__invokation_type__'))
        self.assertTrue(test.__invokation_type__ == 'name')
        self.assertTrue(test.__invokation_priority__ == 10)
