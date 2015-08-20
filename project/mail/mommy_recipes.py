from model_mommy.recipe import Recipe, foreign_key, seq

from project.account.mommy_recipes import domain
from .models import EmailDomain, EmailUser, EmailForward, EmailAlias, CatchAll

email_domain = Recipe(EmailDomain,
                      domain=foreign_key(domain),
                      )

email_user = Recipe(EmailUser,
                    domain=foreign_key(email_domain),
                    )

email_forward = Recipe(EmailForward,
                       user=foreign_key(email_user),
                       )

email_alias = Recipe(EmailAlias,
                     user=foreign_key(email_user),
                     )

catch_all = Recipe(CatchAll,
                   domain=foreign_key(email_domain),
                   user=foreign_key(email_user),
                   )