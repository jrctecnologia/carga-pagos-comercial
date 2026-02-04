from db import get_connection


def buscar_id_concepto_por_codigo(codigo_concepto):
    # Devuelve el CIDCONCEPTODOCUMENTO dado un CCODIGOCONCEPTO.
    if codigo_concepto is None:
        return None

    codigo = str(codigo_concepto).strip()
    if codigo == "":
        return None

    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """
            SELECT CIDCONCEPTODOCUMENTO, CIDCUENTA
            FROM admConceptos
            WHERE CCODIGOCONCEPTO = ?
        """
        cursor.execute(sql, (codigo,))
        row = cursor.fetchone()
        if row:
            return {
                'cidconceptodocumento': row[0],
                'cidcuenta': row[1]
            }
    finally:
        cursor.close()
        conn.close()


def cliente_existe(codigo_cliente):
    # Retorna los datos del cliente si existe, None si no existe
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT CIDCLIENTEPROVEEDOR, CRAZONSOCIAL, CRFC
        FROM admClientes
        WHERE CCODIGOCLIENTE = ?
        AND CTIPOCLIENTE = 1
    """

    cursor.execute(sql, (codigo_cliente,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        return {
            'cidclienteproveedor': resultado[0],
            'crazonsocial': resultado[1],
            'crfc': resultado[2]
        }
    return None


def factura_existe(serie, folio, id_concepto_factura):
    # Verifica si la factura existe, tiene saldo pendiente y no está cancelada
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT CIDDOCUMENTO
        FROM admDocumentos
        WHERE CSERIEDOCUMENTO = ?
          AND CFOLIO = ?
          AND CIDCONCEPTODOCUMENTO = ?
          AND CPENDIENTE > 0
          AND CCANCELADO = 0
    """

    cursor.execute(sql, (serie, folio, id_concepto_factura))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return row[0]
    return None


def pago_existe(serie, folio, id_concepto_pago):
    # Verifica si el pago existe (usamos la misma tabla admDocumentos)
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT 1
        FROM admDocumentos
        WHERE CSERIEDOCUMENTO = ?
          AND CFOLIO = ?
          AND CIDCONCEPTODOCUMENTO = ?
    """

    cursor.execute(sql, (serie, folio, id_concepto_pago))
    existe = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return existe
