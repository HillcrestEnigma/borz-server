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

    # @classmethod
    # def get_queryset(cls, queryset, info):
    #     if info.context.user.is_anonymous:
    #         return queryset.empty()
    #     else:
    #         return queryset.filter(subgroup=info.context.user.subgroups)

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
            models.Subgroup.objects.get(pk=subgroup_pk)
        except models.Subgroup.DoesNotExist:
            raise GraphQLError('The Subgroup does not exist.')
        if info.context.user.is_authenticated:
            author = info.context.user
        else:
            raise GraphQLError('Please login.')
        thread = models.Thread.objects.create(title=title, content=content, author=author, subgroup_id=subgroup_pk)
        return CreateThread(thread=thread)

class UpdateThread(relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        thread = graphene.ID(required=True)

    thread = graphene.Field(ThreadNode)

    @classmethod
    def mutate_and_get_payload(self, root, info, title, content, thread):
        thread_pk = from_global_id(thread)[1]
        try:
            thread_obj = models.Thread.objects.get(pk=thread_pk)
        except models.Thread.DoesNotExist:
            raise GraphQLError('The Thread does not exist.')
        if not info.context.user.is_authenticated:
            raise GraphQLError('Please login.')
        elif info.context.user != thread_obj.author:
            raise GraphQLError('You are not the author of this thread.')
        thread_obj.title = title
        thread_obj.content = content
        thread_obj.save()
        return UpdateThread(thread=thread_obj)

class CreateReply(relay.ClientIDMutation):
    class Input:
        content = graphene.String(required=True)
        thread = graphene.ID(required=True)

    reply = graphene.Field(ReplyNode)

    @classmethod
    def mutate_and_get_payload(self, root, info, content, thread):
        thread_pk = from_global_id(thread)[1]
        try:
            subgroup = models.Thread.objects.get(pk=thread_pk)
        except models.Thread.DoesNotExist:
            raise GraphQLError('The thread does not exist.')
        if info.context.user.is_authenticated:
            author = info.context.user
        else:
            raise GraphQLError('Please login.')
        reply = models.Reply.objects.create(content=content, author=author, thread_id=thread_pk)
        return CreateReply(reply=reply)

class UpdateReply(relay.ClientIDMutation):
    class Input:
        content = graphene.String(required=True)
        reply = graphene.ID(required=True)

    reply = graphene.Field(ReplyNode)

    @classmethod
    def mutate_and_get_payload(self, root, info, title, content, reply):
        reply_pk = from_global_id(reply)[1]
        try:
            reply_obj = models.Reply.objects.get(pk=reply_pk)
        except models.Reply.DoesNotExist:
            raise GraphQLError('The reply does not exist.')
        if not info.context.user.is_authenticated:
            raise GraphQLError('Please login.')
        elif info.context.user != reply_obj.author:
            raise GraphQLError('You are not the author of this thread.')
        reply_obj.content = content
        reply_obj.save()
        return UpdateReply(thread=reply_obj)

class Query(ObjectType):
    thread = relay.Node.Field(ThreadNode)
    threads = DjangoFilterConnectionField(ThreadNode)

    reply = relay.Node.Field(ReplyNode)
    replies = DjangoFilterConnectionField(ReplyNode)

class Mutation(ObjectType):
    create_thread = CreateThread.Field()
    update_thread = UpdateThread.Field()
    create_reply = CreateReply.Field()
    update_reply = UpdateReply.Field()
