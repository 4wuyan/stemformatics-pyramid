#!/bin/bash

psql -U portaladmin portal_beta -c "insert into stemformatics.configs (ref_type,ref_id) values('validation_regex', '(?=^.{12,}$)(?=.*\s+).*$');"
psql -U portaladmin portal_beta -c "insert into stemformatics.configs (ref_type,ref_id) values('from_email', 'noreply@stemformatics.org');"
psql -U portaladmin portal_beta -c "insert into stemformatics.configs (ref_type,ref_id) values('secret_hash_parameter_for_unsubscribe', 'I LOVE WY');"
psql -U portaladmin portal_beta -c "insert into stemformatics.configs (ref_type,ref_id) values('publish_gene_set_email_address', 'fake_email');"

psql -U portaladmin portal_beta -c "INSERT INTO stemformatics.configs (ref_type,ref_id) values('twitter_app_key','xRPPHXqi49Wwde2B8dTlXw');"
psql -U portaladmin portal_beta -c "INSERT INTO stemformatics.configs (ref_type,ref_id) values('twitter_app_secret','l0d48qRQ0gSOLXQI4v2xP3a7vT1TgiOg8H3YVvDEo');"
psql -U portaladmin portal_beta -c "INSERT INTO stemformatics.configs (ref_type,ref_id) values('twitter_oauth_token','456310432-JTqWAijgvpuJuFIxcIGJ5mStek78bCRjXlvSzSMV');"
psql -U portaladmin portal_beta -c "INSERT INTO stemformatics.configs (ref_type,ref_id) values('twitter_oauth_token_secret','0Rftaoi6uPb9A5x9vNVcfdwLTUMa196LELBPpoZz1w');"

psql -U portaladmin portal_beta -c "INSERT INTO stemformatics.configs (ref_type,ref_id) values('GPQueue','/var/www/pylons-data/prod/jobs/GPQueue/');"
psql -U portaladmin portal_beta -c "INSERT INTO stemformatics.configs (ref_type,ref_id) values('StemformaticsQueue','/var/www/pylons-data/prod/jobs/StemformaticsQueue');"
psql -U portaladmin portal_beta -c "INSERT INTO stemformatics.configs (ref_type,ref_id) values('DatasetGCTFiles','/var/www/prod/pylons-data/GCTFiles');"
psql -U portaladmin portal_beta -c "INSERT INTO stemformatics.configs (ref_type,ref_id) values('email_to','test@mailinator.com');"
psql -U portaladmin portal_beta -c "update stemformatics.configs set ref_id = 'stemformatics.sa.metacdn.com/release_69' where ref_type = 'cdn_base_url';"
# psql -U portaladmin portal_beta -c "UPDATE stemformatics.configs set ref_id = 'false' where ref_type = 'production';"
# galaxy server url and key are not included(they are confidential); the information can be found on agile.org or by consulting Isha
