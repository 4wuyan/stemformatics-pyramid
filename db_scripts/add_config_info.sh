#!/bin/bash

psql -U portaladmin portal_beta -c "insert into stemformatics.configs (ref_type,ref_id) values('validation_regex', '(?=^.{12,}$)(?=.*\s+).*$');"
psql -U portaladmin portal_beta -c "insert into stemformatics.configs (ref_type,ref_id) values('from_email', 'noreply@stemformatics.org');"
psql -U portaladmin portal_beta -c "insert into stemformatics.configs (ref_type,ref_id) values('secret_hash_parameter_for_unsubscribe', 'I LOVE WY');"
