import pymysql


def connectdb():
    """
    Connect to database
    Returns:  connection object or error message if connection fails
    """

    try:
        connection = pymysql.connect(host='localhost',
                                   user='root',
                                   password='',
                                   db='webdinarZappa')

        return connection

    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Error al conectar con la base de datos, detalle del error: ", e)
        return e


