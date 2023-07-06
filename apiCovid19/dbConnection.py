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

    global conexion
    try:
        conexion = pymysql.connect(host='localhost',
                                   user='root',
                                   password='',
                                   db='webdinarZappa')

        return conexion

    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar, detalle del error: ", e)
        exit()

