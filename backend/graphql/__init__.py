import graphene

from . import auth
from . import subgroup
from . import thread

class Query(
    auth.Query,
    subgroup.Query,
    thread.Query,
    graphene.ObjectType,
):
    pass

class Mutation(
    auth.Mutation,
    subgroup.Mutation,
    thread.Mutation,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
