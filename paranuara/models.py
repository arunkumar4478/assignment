"""
Models for Paranuara data
Contains people and company collection
"""

from mongoengine import *

## For now hardcoding db as paranuaradb which should be read either from config file or environment variable
connect(db='paranuaradb', host='localhost', connect=False)


class FriendReference(EmbeddedDocument):
    """Friends reference"""
    index = IntField(required=True)

    def __str__(self):
        """Returns string format of object"""
        return str(dict(index=self.index))


class Person(Document):
    """Model for people collection."""
    meta = {'collection': 'people'}

    index = IntField(required=True)
    guid = StringField()
    has_died = BooleanField(required=True)
    balance = DecimalField()
    picture = StringField()
    age = IntField(required=True)
    eyeColor = StringField(required=True)
    name = StringField(required=True)
    gender = StringField()
    company_id = IntField(required=True)
    email = EmailField()
    phone = StringField(required=True)
    address = StringField(required=True)
    about = StringField()
    registered = StringField()
    tags = ListField(StringField())
    friends = EmbeddedDocumentListField(FriendReference)
    greeting = StringField()
    favouriteFood = ListField(StringField())

    def friend_indexes(self):
        """Returns indexes for friend from associated FriendReferences"""
        return [friend.index for friend in self.friends]

    def details_with_common_friends(self, second_person):
        common_friends_indexes = set(self.friend_indexes()).intersection(set(second_person.friend_indexes()))
        common_friends = Person.objects(index__in=common_friends_indexes)(has_died=False)(eyeColor='brown')
        common_friends = list(map(lambda p: p.as_dict(), common_friends))
        return dict(first_person=self.as_dict(),
                    second_person=second_person.as_dict(),
                    common_friends=common_friends)

    def __str__(self):
        """Returns string format of object"""
        return str(dict(index=self.index, name=self.name))

    def as_dict(self):
        """Returns person as dict with required attributes"""
        return dict(name=self.name, age=self.age, phone=self.phone, address=self.address)


class Company(Document):
    """companies collection."""
    meta = {'collection': 'companies'}

    index = IntField(required=True)
    company = StringField(required=True)

    def employees(self):
        """Returns registered employees associated to the company."""
        person_list = Person.objects(company_id=self.index)
        person_list = list(map(lambda p: p.as_dict(), person_list))
        return person_list

    def __str__(self):
        """Returns string format of object"""
        return str(dict(index=self.index, company=self.company))
