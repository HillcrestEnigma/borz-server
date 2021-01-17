import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_relay.node.node import from_global_id

from .. import models
from borz import settings


class SubgroupNode(DjangoObjectType):
    class Meta:
        model = models.Subgroup
        filter_fields = ['name', 'slug', 'description', 'created', 'parent', 'members']
        interfaces = (relay.Node, )

class JoinSubgroup(relay.ClientIDMutation):
    class Input:
        subgroup = graphene.ID(required=True)

    subgroup = graphene.Field(SubgroupNode)

    @classmethod
    def mutate_and_get_payload(self, root, info, subgroup):
        parent_pk = from_global_id(parent)[1]
        if not info.context.user.is_authenticated:
            raise GraphQLError('Please sign in.')
        try:
            subgroup = models.Subgroup.objects.get(parent__pk=parent_pk, slug=slug)
            subgroup.members.add(info.context.user)
        except models.Subgroup.DoesNotExist:
            raise GraphQLError('The Subgroup does not exist.')
        return JoinSubgroup(subgroup=subgroup)

class LeaveSubgroup(relay.ClientIDMutation):
    class Input:
        subgroup = graphene.ID(required=True)

    subgroup = graphene.Field(SubgroupNode)

    @classmethod
    def mutate_and_get_payload(self, root, info, subgroup):
        parent_pk = from_global_id(parent)[1]
        if not info.context.user.is_authenticated:
            raise GraphQLError('Please sign in.')
        try:
            subgroup = models.Subgroup.objects.get(parent__pk=parent_pk, slug=slug)
            subgroup.members.remove(info.context.user)
        except models.Subgroup.DoesNotExist:
            raise GraphQLError('The Subgroup does not exist.')
        return LeaveSubgroup(subgroup=subgroup)

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

class UpdateSubgroup(relay.ClientIDMutation):
    class Input:
        description = graphene.String(required=True)
        subgroup = graphene.ID(required=True)

    subgroup = graphene.Field(SubgroupNode)

    @classmethod
    def mutate_and_get_payload(self, root, info, description, subgroup):
        subgroup_pk = from_global_id(subgroup)[1]
        try:
            subgroup_obj = models.Subgroup.objects.get(pk=subgroup_pk)
        except models.Subgroup.DoesNotExist:
            raise GraphQLError('The subgroup does not exist.')
        subgroup_obj.description = description
        subgroup_obj.save()
        return CreateSubgroup(subgroup=subgroup_obj)

class Query(ObjectType):
    subgroup = relay.Node.Field(SubgroupNode)
    subgroups = DjangoFilterConnectionField(SubgroupNode)

class Mutation(ObjectType):
    create_subgroup = CreateSubgroup.Field()
    join_subgroup = JoinSubgroup.Field()
    leave_subgroup = LeaveSubgroup.Field()
    update_subgroup = UpdateSubgroup.Field()
