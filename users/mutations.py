import graphene
from dj_rest_auth.registration.serializers import RegisterSerializer
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation

from users.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class SignupMutation(SerializerMutation):
    class Meta:
        serializer_class = RegisterSerializer


# class QuestionMutation(graphene.Mutation):
#     class Arguments:
#         # The input arguments for this mutation
#         text = graphene.String(required=True)
#         id = graphene.ID()
#
#     # The class attributes define the response of the mutation
#     question = graphene.Field(QuestionType)
#
#     @classmethod
#     def mutate(cls, root, info, text, id):
#         question = Question.objects.get(pk=id)
#         question.text = text
#         question.save()
#         # Notice we return an instance of this mutation
#         return QuestionMutation(question=question)


class Mutation(graphene.ObjectType):
    signup_user = SignupMutation.Field()
