from graphene_django import DjangoObjectType
import graphene
from accounts.models import Accounts
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations


class AccountsObjectType(DjangoObjectType):
    class Meta:
        model = Accounts
        fields = (
            "first_name",
            "last_name",
            "profile_image"
        )


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
