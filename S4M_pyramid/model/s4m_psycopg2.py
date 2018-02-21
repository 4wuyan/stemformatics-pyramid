#-------Last synchronised with Pylons repo (master) on---------------#
#------------------------19 Feb 2018---------------------------------#
#-------------------------by WU Yan----------------------------------#

from S4M_pyramid.lib.deprecated_pylons_globals import config
import psycopg2
import psycopg2.extras


"""
    generic call for psycopg2
    example #1

    from guide.model import s4m_psycopg2
    sql = "select id,handle,chip_type from datasets where db_id = %(db_id)s and id = ANY (%(temp_list_of_ds_ids)s) ;"
    data = {"db_id":db_id,'temp_list_of_ds_ids':temp_list_of_ds_ids}
    result = s4m_psycopg2._get_psycopg2_sql(sql,data)


    example #2

    from guide.model import s4m_psycopg2
    sql = "select * from biosamples_metadata where ds_id = %s order by md_name,md_value;"
    data =(ds_id,)
    result = s4m_psycopg2._get_psycopg2_sql(sql,data)


"""
def _get_psycopg2_sql(sql,data):
    conn_string = config['psycopg2_conn_string']
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(sql,data)

    # retrieve the records from the database
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


