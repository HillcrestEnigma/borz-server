import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_relay.node.node import from_global_id

from .. import models


class SubgroupNode(DjangoObjectType):
    class Meta:
        model = models.Subgroup
        filter_fields = ['name', 'slug', 'description', 'created', 'parent']
        interfaces = (relay.Node, )

class CreateSubgroup(relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        slug = graphene.String(required=True)
        description = graphene.String(required=True)
        parent = graphene.ID()

    subgroup = graphene.Field(SubgroupNode)

    @classmethod
    def mutate_and_get_payload(self, root, info, name, slug, description, parent):
        parent_pk = from_global_id(parent)[1]
        try:
            subgroup = models.Subgroup.objects.get(parent__pk=parent_pk, slug=slug)
            raise GraphQLError('The Subgroup already exists.')
        except models.Subgroup.DoesNotExist:
            subgroup = models.Subgroup.objects.create(parent_id=parent_pk, name=name, slug=slug, description=description)
        return CreateSubgroup(subgroup=subgroup)

class Query(ObjectType):
    subgroup = relay.Node.Field(SubgroupNode)
    subgroups = DjangoFilterConnectionField(SubgroupNode)

class Mutation(ObjectType):
    create_subgroup = CreateSubgroup.Field()
