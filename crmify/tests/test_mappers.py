from django.test import TestCase
from unittest import mock
from django.contrib.auth.models import User
from crmify.mappers import DjangoUserFieldMapper
from crmify import factories
from crmify.models import Lead


class FieldMapperTestCase(TestCase):
    def setUp(self):
        self.mapper = DjangoUserFieldMapper()
        self.instance = User(username='test@test.com', first_name='Bob', last_name='Testy', email='test@test.com')


class TestFieldMapperLookupValue(FieldMapperTestCase):
    def test_lookup_value_simple(self):
        instance = User(username='test@test.com', first_name='Bob', last_name='Testy')
        self.assertEqual(instance.username, self.mapper.lookup_value('username', instance))

    def test_lookup_value_nested(self):
        class NestedInner(object):
            def __init__(self, value):
                self.value = value

        class NestedOuter(object):
            def __init__(self):
                self.inner = NestedInner('test')

        instance = NestedOuter()
        self.assertEqual(instance.inner.value, self.mapper.lookup_value('inner__value', instance))


class TestFieldMapperFieldMapping(FieldMapperTestCase):
    def test_apply_field_mapping_to_simple_fields(self):
        self.assertDictEqual(
            self.mapper.apply_field_mapping(self.instance),
            {'first_name': self.instance.first_name, 'last_name': self.instance.last_name, 'email': self.instance.email}
        )

    def test_falls_back_to_username_for_email_when_no_email_set(self):
        self.instance.email = None
        self.assertDictEqual(
            self.mapper.apply_field_mapping(self.instance),
            {'first_name': self.instance.first_name, 'last_name': self.instance.last_name, 'email': self.instance.username}
        )

    def test_apply_field_mapping_to_fields_not_existing(self):
        class OtherClass(object):
            def __init__(self, foo=None):
                self.foo = foo

        instance = OtherClass(foo='bar')
        self.assertRaises(AttributeError, self.mapper.apply_field_mapping, instance)


class TestFieldMapperCreateLead(FieldMapperTestCase):
    def test_uses_result_from_apply_field_mapping_to_create_lead(self):
        self.mapper.apply_field_mapping = mock.MagicMock(return_value={})

        self.mapper.create_lead(self.instance)

        self.assertIsNone(self.mapper.apply_field_mapping.assert_called_once_with(self.instance))

    def test_returns_new_lead(self):
        new_lead = self.mapper.create_lead(self.instance)

        self.assertTrue(type(new_lead) is Lead)
        self.assertEqual(new_lead.email, self.instance.email)
        self.assertEqual(new_lead.first_name, self.instance.first_name)
        self.assertEqual(new_lead.last_name, self.instance.last_name)


class TestFieldMapperUpdateLead(FieldMapperTestCase):
    def setUp(self):
        super(TestFieldMapperUpdateLead, self).setUp()
        self.lead = factories.LeadFactory()

    def test_returns_updated_lead(self):
        updated_lead = self.mapper.update_lead(self.lead, self.instance)

        self.assertTrue(type(updated_lead) is Lead)
        self.assertEqual(updated_lead.email, self.instance.email)
        self.assertEqual(updated_lead.first_name, self.instance.first_name)
        self.assertEqual(updated_lead.last_name, self.instance.last_name)
