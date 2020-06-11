import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, QuerySet
from rest_framework import serializers


class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=64, null=False)
    users = models.ManyToManyField(User, db_index=True)

    @staticmethod
    def create_collection(name: str, owner: User) -> 'Collection':
        """ Create a collection owned by this user. """
        collection = Collection.objects.create(name=name)
        collection.users.add(owner)
        collection.save()
        return collection

    @staticmethod
    def get_collections(owner: User) -> QuerySet:
        return Collection.objects.filter(users=owner)

    @staticmethod
    def get_collection(owner: User, collection_id: str) -> 'Collection':
        return Collection.objects.get(
            Q(users=owner) & Q(id=collection_id)
        )

    @staticmethod
    def get_one_collection(owner: User) -> 'Collection':
        """
        TODO: Software will work for more than one collection, but for now one is enough.
        """
        collections = Collection.get_collections(owner)
        if len(collections) != 1:
            raise ValueError('Got %d collections' % len(collections))
        return collections[0]

    def __str__(self):
        return f'Collection({self.id}, "{self.name}"")'


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name']
        read_only_fields = ['id']
