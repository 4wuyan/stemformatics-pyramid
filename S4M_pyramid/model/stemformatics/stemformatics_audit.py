#TODO-1
import re , string , json , psycopg2 , psycopg2.extras,datetime
from S4M_pyramid.lib.deprecated_pylons_globals import config


__all__ = ['Stemformatics_Audit']


class Stemformatics_Audit(object):
    def __init__ (self):
        pass


    """
    add_audit_log expecting a dictionary with:
        ref_type (unicode)
        ref_id (unicode)
        uid (int)
        url (from pylons)
        request (from pylons)
    """
    @staticmethod
    def add_audit_log(audit_dict):
        url = audit_dict['url']
        request = audit_dict['request']

        ref_type = audit_dict['ref_type']
        ref_id = audit_dict['ref_id']

        # ref_type could be a ds_id etc
        if isinstance(ref_id,int):
            ref_id = str(ref_id)

        if 'extra_ref_type' in audit_dict:
            extra_ref_type = audit_dict['extra_ref_type']
            extra_ref_id = audit_dict['extra_ref_id']

            # ref_type could be a ds_id etc
            if isinstance(extra_ref_id,int):
                ref_id = str(extra_ref_id)
        else:
            extra_ref_type = ''
            extra_ref_id = ''


        uid = audit_dict['uid']
        date_created = datetime.datetime.now()
        controller = url.environ['pylons.routes_dict']['controller']
        action = url.environ['pylons.routes_dict']['action']
        if 'controller' in audit_dict:
            controller = audit_dict['controller']
        if 'action' in audit_dict:
            action = audit_dict['action']

        ip_address = request.environ.get("HTTP_X_FORWARDED_FOR", request.environ["REMOTE_ADDR"])

        valid_ref_types = ['ds_id','gene_id','search_term','gene_set_id','share','feature_id','help_in_page','help_tutorial','help_tutorial_landing','help_faq']
        if ref_type in valid_ref_types:
            conn_string = config['psycopg2_conn_string']
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("insert into stemformatics.audit_log (ref_type,ref_id,uid,date_created,controller,action,ip_address,extra_ref_type,extra_ref_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s) ;",(ref_type,ref_id,uid,date_created,controller,action,ip_address,extra_ref_type,extra_ref_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            return False

    @staticmethod
    def check_date_format(date_string):
        r = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
        return r.match(date_string)


    @staticmethod
    def get_user_statistics(start_date,end_date,limit):

        if not isinstance(start_date, str):
            return []
        if not isinstance(end_date, str):
            return []
        if not isinstance(limit, int):
            return []

        if not Stemformatics_Audit.check_date_format(start_date) or not Stemformatics_Audit.check_date_format(end_date):
            return []

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select username,max(organisation) as organisation,max(full_name) as full_name,a.uid,count(*) as c from stemformatics.audit_log as a left join stemformatics.users as u on u.uid = a.uid  where date_created >= %s and date_created <= %s group by a.uid,username order by c desc limit %s;"
        data = (start_date,end_date,limit,)
        cursor.execute(sql,data)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return  result

    @staticmethod
    def get_dataset_statistics(start_date,end_date,limit):
        if not isinstance(start_date, str):
            return []
        if not isinstance(end_date, str):
            return []
        if not isinstance(limit, int):
            return []
        if not Stemformatics_Audit.check_date_format(start_date) or not Stemformatics_Audit.check_date_format(end_date):
            return []

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "select handle,ref_id,count(*) as c from stemformatics.audit_log as a left join datasets as d on d.id = cast(a.ref_id as int) where date_created >= %s and date_created <=%s and ref_type = 'ds_id' group by ref_id,handle order by c desc limit %s;"
        data = (start_date,end_date,limit,)
        cursor.execute(sql,data)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return  result


    @staticmethod
    def get_gene_statistics(start_date,end_date,limit):
        if not isinstance(start_date, str):
            return []
        if not isinstance(end_date, str):
            return []
        if not isinstance(limit, int):
            return []
        if not Stemformatics_Audit.check_date_format(start_date) or not Stemformatics_Audit.check_date_format(end_date):
            return []

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        sql="select associated_gene_name,ref_id,count(*) as c from stemformatics.audit_log as a left join genome_annotations as ga on ga.gene_id = a.ref_id where date_created >= %s and date_created <=%s and ref_type = 'gene_id' group by ref_id,associated_gene_name order by c desc limit %s;"
        data = (start_date,end_date,limit,)
        cursor.execute(sql,data)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return  result



    @staticmethod
    def get_controller_statistics(start_date,end_date,limit):
        if not isinstance(start_date, str):
            return []
        if not isinstance(end_date, str):
            return []
        if not isinstance(limit, int):
            return []
        if not Stemformatics_Audit.check_date_format(start_date) or not Stemformatics_Audit.check_date_format(end_date):
            return []

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        sql="select controller,action,count(*) as c from stemformatics.audit_log  where date_created >= %s and date_created <=%s group by controller,action order by c desc limit %s;"
        data = (start_date,end_date,limit,)
        cursor.execute(sql,data)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return  result




    @staticmethod
    def get_dataset_user_statistics(start_date,end_date,limit):
        if not isinstance(start_date, str):
            return []
        if not isinstance(end_date, str):
            return []
        if not isinstance(limit, int):
            return []
        if not Stemformatics_Audit.check_date_format(start_date) or not Stemformatics_Audit.check_date_format(end_date):
            return []

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        sql = "select max(ref_id) as ref_id,ref_type,d.handle as handle,username,count(*) as c from stemformatics.audit_log as a left join datasets as d on d.id = cast(a.ref_id as int) left join stemformatics.users as u on u.uid = a.uid where ref_type = 'ds_id' and date_created >= %s and date_created <=%s group by ref_type, handle ,username  order by c desc limit %s;"
        data = (start_date,end_date,limit,)
        cursor.execute(sql,data)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return  result


    @staticmethod
    def get_controller_user_statistics(start_date,end_date,limit):
        if not isinstance(start_date, str):
            return []
        if not isinstance(end_date, str):
            return []
        if not isinstance(limit, int):
            return []
        if not Stemformatics_Audit.check_date_format(start_date) or not Stemformatics_Audit.check_date_format(end_date):
            return []

        conn_string = config['psycopg2_conn_string']
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        sql = "select controller,action,username,c from (select controller,action,uid,count(*) as c, row_number() over (partition by controller,action order by count(*) desc ) rn from stemformatics.audit_log where date_created >=%s and date_created <=%s group by controller,action,uid order by controller,action,c desc) s left join stemformatics.users as u on u.uid = s.uid  where rn <=%s;"

        data = (start_date,end_date,limit,)
        cursor.execute(sql,data)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return  result
