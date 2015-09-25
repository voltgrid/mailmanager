from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    sql = """
        CREATE OR REPLACE VIEW v_email_aliases AS SELECT concat(mail_emailalias.alias,'@',account_domain.name) AS source,concat(mail_emailuser.name,'@',account_domain.name) AS destination from (((mail_emailalias join mail_emailuser on((mail_emailuser.id = mail_emailalias.user_id))) join mail_emaildomain on((mail_emaildomain.id = mail_emailuser.domain_id))) join account_domain on((account_domain.id = mail_emaildomain.domain_id))) union select concat(mail_emailuser.name,'@',account_domain.name) AS source,mail_emailforward.destination AS destination from (((mail_emailforward join mail_emailuser on((mail_emailuser.id = mail_emailforward.user_id))) join mail_emaildomain on((mail_emaildomain.id = mail_emailuser.domain_id))) join account_domain on((account_domain.id = mail_emaildomain.domain_id)));
        CREATE OR REPLACE VIEW v_email_catchall AS SELECT ad2.name AS source,concat(mail_emailuser.name,'@',ad1.name) AS destination from (((((mail_catchall join mail_emailuser on((mail_emailuser.id = mail_catchall.user_id))) join mail_emaildomain ed1 on((ed1.id = mail_emailuser.domain_id))) join mail_emaildomain ed2 on((ed2.id = mail_catchall.domain_id))) join account_domain ad1 on((ad1.id = ed1.domain_id))) join account_domain ad2 on((ad2.id = ed2.domain_id)));
        CREATE OR REPLACE VIEW v_email_domains AS SELECT account_domain.name AS name from (account_domain join mail_emaildomain on((account_domain.id = mail_emaildomain.domain_id)));
        CREATE OR REPLACE VIEW v_email_users AS SELECT mail_emailuser.id AS id, concat(mail_emailuser.name,'@',account_domain.name) AS email, mail_emailuser.password AS password, concat('*:bytes=', mail_emailuser.quota, 'M') AS quota_rule from ((mail_emailuser join mail_emaildomain on((mail_emaildomain.id = mail_emailuser.domain_id))) join account_domain on((account_domain.id = mail_emaildomain.domain_id)));
        """

    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute(self.sql)