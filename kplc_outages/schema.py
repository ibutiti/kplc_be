import graphene

import outages.schema


class Query(outages.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
