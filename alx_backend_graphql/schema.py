import graphene
from graphene_django import DjangoObjectType
import crm.schema


class Query(crm.schema.Query, graphene.ObjectType):
    pass


class Mutation(crm.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)