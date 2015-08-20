
CREATE VIEW `v_email_aliases` AS select concat(`mail_emailalias`.`alias`,'@',`account_domain`.`name`) AS `source`,concat(`mail_emailuser`.`name`,'@',`account_domain`.`name`) AS `destination` from (((`mail_emailalias` join `mail_emailuser` on((`mail_emailuser`.`id` = `mail_emailalias`.`user_id`))) join `mail_emaildomain` on((`mail_emaildomain`.`id` = `mail_emailuser`.`domain_id`))) join `account_domain` on((`account_domain`.`id` = `mail_emaildomain`.`domain_id`))) union select concat(`mail_emailuser`.`name`,'@',`account_domain`.`name`) AS `source`,`mail_emailforward`.`destination` AS `destination` from (((`mail_emailforward` join `mail_emailuser` on((`mail_emailuser`.`id` = `mail_emailforward`.`user_id`))) join `mail_emaildomain` on((`mail_emaildomain`.`id` = `mail_emailuser`.`domain_id`))) join `account_domain` on((`account_domain`.`id` = `mail_emaildomain`.`domain_id`)));

CREATE VIEW `v_email_catchall` AS select `ad2`.`name` AS `source`,concat(`mail_emailuser`.`name`,'@',`ad1`.`name`) AS `destination` from (((((`mail_catchall` join `mail_emailuser` on((`mail_emailuser`.`id` = `mail_catchall`.`user_id`))) join `mail_emaildomain` `ed1` on((`ed1`.`id` = `mail_emailuser`.`domain_id`))) join `mail_emaildomain` `ed2` on((`ed2`.`id` = `mail_catchall`.`domain_id`))) join `account_domain` `ad1` on((`ad1`.`id` = `ed1`.`domain_id`))) join `account_domain` `ad2` on((`ad2`.`id` = `ed2`.`domain_id`)));

CREATE VIEW `v_email_domains` AS select `account_domain`.`name` AS `name` from (`account_domain` join `mail_emaildomain` on((`account_domain`.`id` = `mail_emaildomain`.`domain_id`)));

CREATE VIEW `v_email_users` AS select `mail_emailuser`.`id` AS `id`,concat(`mail_emailuser`.`name`,'@',`account_domain`.`name`) AS `email`,`mail_emailuser`.`password` AS `password` from ((`mail_emailuser` join `mail_emaildomain` on((`mail_emaildomain`.`id` = `mail_emailuser`.`domain_id`))) join `account_domain` on((`account_domain`.`id` = `mail_emaildomain`.`domain_id`)));