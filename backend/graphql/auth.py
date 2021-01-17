import graphene
from graphene_django.filter.fields import DjangoFilterConnectionField

from graphql_auth.schema import UserNode, MeQuery
from graphql_auth import relay
from graphql_auth.settings import graphql_auth_settings as app_settings
from django.contrib.auth import get_user_model
import datetime
from graphql import GraphQLError

User = get_user_model()


class BorzUserNode(UserNode):
    class Meta:
        model = User
        filter_fields = app_settings.USER_NODE_FILTER_FIELDS
        exclude = app_settings.USER_NODE_EXCLUDE_FIELDS
        interfaces = (graphene.relay.Node,)
        skip_registry = False

    date_joined = graphene.String()

    def resolve_date_joined(root, info):
        return int(root.date_joined.timestamp())

class AuthRelayMutation(graphene.ObjectType):
    register = relay.Register.Field()
    verify_account = relay.VerifyAccount.Field()
    resend_activation_email = relay.ResendActivationEmail.Field()
    send_password_reset_email = relay.SendPasswordResetEmail.Field()
    password_reset = relay.PasswordReset.Field()
    password_set = relay.PasswordSet.Field()
    password_change = relay.PasswordChange.Field()
    update_account = relay.UpdateAccount.Field()
    archive_account = relay.ArchiveAccount.Field()
    delete_account = relay.DeleteAccount.Field()
    send_secondary_email_activation =  relay.SendSecondaryEmailActivation.Field()
    verify_secondary_email = relay.VerifySecondaryEmail.Field()
    swap_emails = relay.SwapEmails.Field()
    remove_secondary_email = relay.RemoveSecondaryEmail.Field()

    token_auth = relay.ObtainJSONWebToken.Field()
    verify_token = relay.VerifyToken.Field()
    refresh_token = relay.RefreshToken.Field()
    revoke_token = relay.RevokeToken.Field()


class Query(MeQuery, graphene.ObjectType):
    user = graphene.relay.Node.Field(BorzUserNode)
    users = DjangoFilterConnectionField(BorzUserNode)


class Mutation(AuthRelayMutation, graphene.ObjectType):
    pass
