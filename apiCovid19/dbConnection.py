# hacer una funcion que se conecte a una base de datos mysql y maneje excepciones
import pymysql


def connectdb():
    """
    Connect to database
    Returns:
        con: connection
        raise Exception: if connection fails
        False: if connection fails
    """

    try:
        connection = pymysql.connect(host='localhost',
                                   user='root',
                                   password='',
                                   db='webdinarZappa')

        return connection

    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Error al conectar con la base de datos, detalle del error: ", e)
        exit()

