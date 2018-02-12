

__all__ = ['Stemformatics_Shared_Resource']




class Stemformatics_Shared_Resource(object):
    """\
    Stemformatics_Shared_Resource Model Object
    ========================================

    A simple model of static functions to make the controllers thinner for login controller

    Please note for most of these functions you will have to pass in the db object



    """

    def __init__(self):
        pass

    @staticmethod
    def add_shared_resource(db, share_type, share_id, from_uid, to_uid):  # CRITICAL-2
        try:
            expires_in = 30

            delta_days = timedelta(days=expires_in)

            created = datetime.now()
            expiry_date = created + delta_days

            db.schema = 'stemformatics'
            result = db.shared_resources.insert(share_type=share_type, share_id=share_id, from_uid=from_uid,
                                                to_uid=to_uid, expiry_date=expiry_date, created=created)
            db.commit()
            db.flush()

            return result
        except:
            return None

    @staticmethod
    def check_shared_resource(db, share_type, share_id, to_uid):  # CRITICAL-2

        db.schema = 'stemformatics'
        sr = db.shared_resources
        result = sr.filter(and_(sr.share_type == share_type, sr.share_id == share_id, sr.to_uid == to_uid)).all()

        return result

    @staticmethod
    def delete_shared_resource(db, share_type, share_id, to_uid):  # CRITICAL-2
        db.schema = 'stemformatics'
        sr = db.shared_resources
        share = sr.filter(and_(sr.share_type == share_type, sr.share_id == share_id, sr.to_uid == to_uid))
        print
        "\n\n\n\n\n==================\n\n"
        print
        share
        share.delete()
        db.commit()
        print
        sr.filter(and_(sr.share_type == share_type, sr.share_id == share_id, sr.to_uid == to_uid))
        print
        "\n\n==================\n\n\n\n\n"




