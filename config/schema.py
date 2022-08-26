import graphene

import outages.schema
from users.mutations import Mutation


class Query(outages.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
