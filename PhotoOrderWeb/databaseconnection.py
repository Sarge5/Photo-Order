__author__ = 'Sarge'

import pymysql
import sys


class DatabaseConnection:

    def __init__(self, host, database, user, password):
        try:
            self.connection = pymysql.connect(
                host=host,
                database=database,
                user=user,
                password=password)
        except:
            self.connection = False

    def getPhotosFromDB(self, siteurl):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT picture.idpicture, picture.name, picture.link, picture.ordered
                FROM picture
                LEFT JOIN folder
                USING (idfolder)
                WHERE folder.url = %s;
                """,
                (siteurl)
            )
            result = cursor.fetchall()
            cursor.close()
            return result
        except:
            return -1

    def setPhotoOrderStatus(self, idphoto, ordered):
        try:
            cursor = self.connection.cursor()
            if ordered:
                orderedint = 1
            else:
                orderedint = 0
            cursor.execute(
                """
                UPDATE picture
                SET ordered = %s
                WHERE (idpicture = %s)
                """,
                (orderedint, idphoto)
            )
            self.connection.commit()
            cursor.close()
            return 0
        except:
            print(sys.exc_info())
            return -1