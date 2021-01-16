import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id
from django.contrib.auth import get_user_model
from graphql import GraphQLError

from .. import models


User = get_user_model()


class ThreadNode(DjangoObjectType):
    class Meta:
        model = models.Thread
        filter_fields = ['title', 'content', 'created', 'modified', 'author', 'subgroup']
        interfaces = (relay.Node, )

class ReplyNode(DjangoObjectType):
    class Meta:
        model = models.Reply
        filter_fields = ['content', 'created', 'modified', 'author', 'thread']
        interfaces = (relay.Node, )

class CreateThread(relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        subgroup = graphene.ID(required=True)

    thread = graphene.Field(ThreadNode)

    @classmethod
    def mutate_and_get_payload(self, root, info, title, content, subgroup):
        subgroup_pk = from_global_id(subgroup)[1]
        try:
            subgroup = models.Subgroup.objects.get(pk=subgroup_pk)
        except models.Subgroup.DoesNotExist:
            raise GraphQLError('The Subgroup does not exist.')
        if info.context.user.is_authenticated:
            author = info.context.user
        else:
            raise GraphQLError('Please login.')
        thread = models.Thread.objects.create(title=title, content=content, author=author, subgroup_id=subgroup_pk)
        return CreateThread(thread=thread)

class Query(ObjectType):
    thread = relay.Node.Field(ThreadNode)
    threads = DjangoFilterConnectionField(ThreadNode)

    reply = relay.Node.Field(ReplyNode)
    replies = DjangoFilterConnectionField(ReplyNode)

class Mutation(ObjectType):
    create_thread = CreateThread.Field()
