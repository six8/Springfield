import pytest
from springfield import Entity, FlexEntity, fields
from springfield.timeutil import date_parse

def test_entity():
    class TestEntity(Entity):
        id = fields.IntField()
        name = fields.StringField()
        bool = fields.BooleanField()

    e = TestEntity(id='1', bool='1')
    e.name = 'foo'

    assert e.id == 1
    assert e.name == 'foo'
    assert e.bool is True


    with pytest.raises(AttributeError):
        e.invalid_field

def test_bool_field():
    class TestEntity(Entity):
        bool = fields.BooleanField()

    e = TestEntity()

    for i in [True, 'yes', 'YES', 'on', 'true', '1', 1]:
        e.bool = i
        assert e.bool is True

    for i in [False, 'no', 'OFF', 'off', 'FALSE', '0', 0]:
        e.bool = i
        assert e.bool is False

    e.bool = None
    assert e.bool is None


    for i in [22, object(), 2.4, 'frag']:
        with pytest.raises(TypeError):
            e.bool = i

def test_flex_entity():
    class TestEntity(FlexEntity):
        id = fields.IntField()
        name = fields.StringField()

    e = TestEntity(name='test', nofield='foo')
    assert e.name == 'test'
    assert e.nofield == 'foo'

def test_entity_field():
    class SubEntity(Entity):
        id = fields.IntField()

    class TestEntity(Entity):
        sub = fields.EntityField(SubEntity)

    e = TestEntity(sub=dict(id='2'))
    assert e.sub.id == 2

def test_jsonify():
    class TestEntity(Entity):
        id = fields.IntField()
        name = fields.StringField(default='foo')
        location = fields.StringField()
        department = fields.StringField(default=None)
        created_at = fields.DateTimeField()
    e = TestEntity(id=1, location='CA')
    assert e.jsonify() == {'id': 1, 'name': 'foo', 'location': 'CA', 'department': None}
    e = TestEntity(location='CA', name='bar')
    assert e.jsonify() == {'name': 'bar', 'location': 'CA', 'department': None}
    e = TestEntity(location=None)
    assert e.jsonify() == {'name': 'foo', 'location': None, 'department': None}
    e = TestEntity()
    assert e.jsonify() == {'name': 'foo', 'department': None}
    e = TestEntity(created_at='2016-04-15')
    assert e.jsonify() == {'name': 'foo', 'department': None,
                           'created_at': '2016-04-15T00:00:00Z'}

def test_flatten():
    class TestEntity(Entity):
        id = fields.IntField()
        name = fields.StringField(default='foo')
        location = fields.StringField()
        department = fields.StringField(default=None)
        created_at = fields.DateTimeField()

    e = TestEntity(id=1, location='CA')
    assert e.flatten() == {'id': 1, 'name': 'foo', 'location': 'CA', 'department': None}
    e = TestEntity(location='CA', name='bar')
    assert e.flatten() == {'name': 'bar', 'location': 'CA', 'department': None}
    e = TestEntity(location=None)
    assert e.flatten() == {'name': 'foo', 'location': None, 'department': None}
    e = TestEntity()
    assert e.flatten() == {'name': 'foo', 'department': None}
    e = TestEntity(created_at='2016-04-15')
    assert e.flatten() == {'name': 'foo', 'department': None,
                           'created_at': date_parse('2016-04-15')}
