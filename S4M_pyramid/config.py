import psycopg2
import psycopg2.extras

config = {
    'psycopg2_conn_string': "host='localhost' dbname='portal_beta' user='portaladmin'",
    'orm_conn_string': 'postgresql://portaladmin@localhost/portal_beta',

    # The configuration below should be imported from the stemformatics.configs table in the database.
    # But for now, we just do some hack here, since we don't have access to that database table.
    'validation_regex': '(?=^.{12,}$)(?=.*\s+).*$',
    'from_email': 'noreply@stemformatics.org',
    'secret_hash_parameter_for_unsubscribe': 'I LOVE WY',
}

conn_string = config['psycopg2_conn_string']
conn = psycopg2.connect(conn_string)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
sql = "select ref_type,ref_id from stemformatics.configs;"
cursor.execute(sql)
result = cursor.fetchall()
cursor.close()
conn.close()

result_dir={}
for row in result:
    ref_type = row['ref_type']
    ref_id = row['ref_id']
    try:
       ref_id = int(ref_id)
    except:
       pass

    result_dir[ref_type] = ref_id

for key in result_dir:
    config[key] = result_dir[key]
