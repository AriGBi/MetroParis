from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def hasConnessione(u:Fermata,v:Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from connessione c where c.id_stazP = %s and c.id_stazA =%s"""
        cursor.execute(query,(u.id_fermata,v.id_fermata)) #perchè nel database ci sono gli di non gli oggetti

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result)>0 #cioè fa il return solo se la len>0 (quindi alla fine ritorna True o False)

    @staticmethod
    def getVicini(u: Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from connessione c where c.id_stazP = %s"""
        cursor.execute(query, (u.id_fermata,))  # perchè nel database ci sono gli di non gli oggetti

        for row in cursor:
            result.append(Connessione(**row)) #result è una lista di connessione che partono dal nodo u
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from connessione c""" #mi da tutti gli archi
        cursor.execute(query, ())

        for row in cursor:
            result.append(Connessione(**row))  # result è una lista di connessione che partono dal nodo u
        cursor.close()
        conn.close()
        return result
