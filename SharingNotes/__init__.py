import pymysql
pymysql.install_as_MySQLdb()



# import redis
# from Main.models import Note
# from .local_settings import POOL
#
#
#
# notes = Note.get_hottest_note()
# conn = redis.Redis(connection_pool=POOL)
# for note in notes:
#     id = note['id']
#     conn.set(name=id, value=Note.objects.get(id=id).to_string())
#     print(conn.get(note['id']).decode('utf-8'))
