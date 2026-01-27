from db import get_connection
from datetime import datetime
import uuid

def obtener_ultimo_id(tabla, id_columna):
    """Obtiene el último ID usado en una tabla específica."""
    conn = get_connection()
    cursor = conn.cursor()

    sql = f"SELECT MAX({id_columna}) FROM {tabla}"
    cursor.execute(sql)
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado and resultado[0] is not None:
        return resultado[0]
    return 0

def obtener_id_concepto(codigo_concepto):
    """Obtiene el ID del concepto basado en su código"""
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT CIDCONCEPTODOCUMENTO
        FROM admConceptos
        WHERE CCODIGOCONCEPTO = ?
    """

    cursor.execute(sql, (codigo_concepto,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        return resultado[0]
    return None

def obtener_id_moneda(nombre_moneda):
    """Obtiene el ID de la moneda basado en su nombre"""
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT CIDMONEDA
        FROM admMonedas
        WHERE CNOMBREMONEDA = ?
    """

    cursor.execute(sql, (nombre_moneda,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        return resultado[0]
    return None

def obtener_plantilla_documento():
    return {
        'CIDDOCUMENTODE': 9,
        'CIDCONCEPTODOCUMENTO': 0,
        'CSERIEDOCUMENTO': '',
        'CFOLIO': 0.00,
        'CFECHA': '18991230',
        'CIDCLIENTEPROVEEDOR': 0,
        'CRAZONSOCIAL': '',
        'CRFC': '',
        'CIDAGENTE': 0,
        'CFECHAVENCIMIENTO': '18991230',
        'CFECHAPRONTOPAGO': '18991230',
        'CFECHAENTREGARECEPCION': '18991230',
        'CFECHAULTIMOINTERES': '18991230',
        'CIDMONEDA': 1,
        'CTIPOCAMBIO': 1,
        'CREFERENCIA': '',
        'COBSERVACIONES': '',
        'CNATURALEZA': 1,
        'CIDDOCUMENTOORIGEN': 0,
        'CPLANTILLA': 0,
        'CUSACLIENTE': 1,
        'CUSAPROVEEDOR': 0,
        'CAFECTADO': 1,
        'CIMPRESO': 0,
        'CCANCELADO': 0,
        'CDEVUELTO': 0,
        'CIDPREPOLIZA': 0,
        'CIDPREPOLIZACANCELACION': 0,
        'CESTADOCONTABLE': 1,
        'CNETO': 0.00,
        'CIMPUESTO1': 0.00,
        'CIMPUESTO2': 0.00,
        'CIMPUESTO3': 0.00,
        'CRETENCION1': 0.00,
        'CRETENCION2': 0.00,
        'CDESCUENTOMOV': 0.00,
        'CDESCUENTODOC1': 0.00,
        'CDESCUENTODOC2': 0.00,
        'CGASTO1': 0.00,
        'CGASTO2': 0.00,
        'CGASTO3': 0.00,
        'CTOTAL': 0.00,
        'CPENDIENTE': 0.00,
        'CTOTALUNIDADES': 0.00,
        'CDESCUENTOPRONTOPAGO': 0.00,
        'CPORCENTAJEIMPUESTO1': 0.00,
        'CPORCENTAJEIMPUESTO2': 0.00,
        'CPORCENTAJEIMPUESTO3': 0.00,
        'CPORCENTAJERETENCION1': 0.00,
        'CPORCENTAJERETENCION2': 0.00,
        'CPORCENTAJEINTERES': 0.00,
        'CTEXTOEXTRA1': '',
        'CTEXTOEXTRA2': '',
        'CTEXTOEXTRA3': '',
        'CFECHAEXTRA': '18991230',
        'CIMPORTEEXTRA1': 0.00,
        'CIMPORTEEXTRA2': 0.00,
        'CIMPORTEEXTRA3': 0.00,
        'CIMPORTEEXTRA4': 0.00,
        'CDESTINATARIO': '',
        'CNUMEROGUIA': '',
        'CMENSAJERIA': '',
        'CCUENTAMENSAJERIA': '',
        'CNUMEROCAJAS': 0.00,
        'CPESO': 0.00,
        'CBANOBSERVACIONES': 0,
        'CBANDATOSENVIO': 0,
        'CBANCONDICIONESCREDITO': 0,
        'CBANGASTOS': 0,
        'CUNIDADESPENDIENTES': 0.00,
        'CTIMESTAMP': datetime.now().strftime('%m/%d/%Y %H:%M:%S:%f')[:-3],
        'CIMPCHEQPAQ': 0,
        'CSISTORIG': 205,
        'CIDMONEDCA': 0,
        'CTIPOCAMCA': 0.00,
        'CESCFD': 0,
        'CTIENECFD': 0,
        'CLUGAREXPE': '',
        'CMETODOPAG': '',
        'CNUMPARCIA': 0,
        'CCANTPARCI': 0,
        'CCONDIPAGO': '',
        'CNUMCTAPAG': '',
        'CGUIDDOCUMENTO': str(uuid.uuid4()),
        'CUSUARIO': 'SUPERVISOR',
        'CIDPROYECTO': 0,
        'CIDCUENTA': 2,
        'CTRANSACTIONID': '',
        'CIDCOPIADE': 0,
        'CVERESQUE': '',
        'CDATOSADICIONALES': '',
        'CIDAPERTURA': 0
    }


def crear_documento(datos):
    """
    Crea un nuevo registro en admDocumentos.
    
    Args:
        datos (dict): Diccionario con los campos a insertar. 
        Los campos no especificados usarán sus valores DEFAULT de la BD.
        
    Returns:
        int: El CIDDOCUMENTO del registro creado
        
    Ejemplo:
        datos = obtener_plantilla_documento()
        datos['CIDCONCEPTODOCUMENTO'] = 5
        datos['CSERIEDOCUMENTO'] = 'P'
        datos['CFOLIO'] = 100
        nuevo_id = crear_documento(datos)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Obtener el siguiente ID disponible
    nuevo_id = obtener_ultimo_id('admDocumentos', 'CIDDOCUMENTO') + 1
    datos['CIDDOCUMENTO'] = nuevo_id
    datos['CFECHAVENCIMIENTO'] = datos['CFECHA']
    datos['CFECHAPRONTOPAGO'] = datos['CFECHA']
    datos['CFECHAENTREGARECEPCION'] = datos['CFECHA']
    datos['CFECHAULTIMOINTERES'] = datos['CFECHA']
    
    # Construir la consulta dinámicamente
    columnas = ', '.join(datos.keys())
    placeholders = ', '.join(['?' for _ in datos])
    valores = tuple(datos.values())
    
    sql = f"INSERT INTO admDocumentos ({columnas}) VALUES ({placeholders})"
    
    cursor.execute(sql, valores)
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return nuevo_id


def obtener_plantilla_movimiento():
    return {
        'CIDDOCUMENTO': 0,
        'CNUMEROMOVIMIENTO': 1,
        'CIDDOCUMENTODE': 9,
        'CIDPRODUCTO': 0,
        'CIDALMACEN': 0,
        'CUNIDADES': 0.00,
        'CUNIDADESNC': 0.00,
        'CUNIDADESCAPTURADAS': 0.00,
        'CIDUNIDAD': 0,
        'CIDUNIDADNC': 0,
        'CPRECIO': 0.00,
        'CPRECIOCAPTURADO': 0.00,
        'CCOSTOCAPTURADO': 0.00,
        'CCOSTOESPECIFICO': 0.00,
        'CNETO': 0.00,
        'CIMPUESTO1': 0.00,
        'CPORCENTAJEIMPUESTO1': 0.00,
        'CIMPUESTO2': 0.00,
        'CPORCENTAJEIMPUESTO2': 0.00,
        'CIMPUESTO3': 0.00,
        'CPORCENTAJEIMPUESTO3': 0.00,
        'CRETENCION1': 0.00,
        'CPORCENTAJERETENCION1': 0.00,
        'CRETENCION2': 0.00,
        'CPORCENTAJERETENCION2': 0.00,
        'CDESCUENTO1': 0.00,
        'CPORCENTAJEDESCUENTO1': 0.00,
        'CDESCUENTO2': 0.00,
        'CPORCENTAJEDESCUENTO2': 0.00,
        'CDESCUENTO3': 0.00,
        'CPORCENTAJEDESCUENTO3': 0.00,
        'CDESCUENTO4': 0.00,
        'CPORCENTAJEDESCUENTO4': 0.00,
        'CDESCUENTO5': 0.00,
        'CPORCENTAJEDESCUENTO5': 0.00,
        'CTOTAL': 0.00,
        'CPORCENTAJECOMISION': 0.00,
        'CREFERENCIA': '',
        'COBSERVAMOV': '',
        'CAFECTAEXISTENCIA': 3,
        'CAFECTADOSALDOS': 1,
        'CAFECTADOINVENTARIO': 0,
        'CFECHA': '18991230',
        'CMOVTOOCULTO': 0,
        'CIDMOVTOOWNER': 0,
        'CIDMOVTOORIGEN': 0,
        'CUNIDADESPENDIENTES': 0.00,
        'CUNIDADESNCPENDIENTES': 0.00,
        'CUNIDADESORIGEN': 0.00,
        'CUNIDADESNCORIGEN': 0.00,
        'CTIPOTRASPASO': 0,
        'CIDVALORCLASIFICACION': 0,
        'CTEXTOEXTRA1': '',
        'CTEXTOEXTRA2': '',
        'CTEXTOEXTRA3': '',
        'CFECHAEXTRA': '18991230',
        'CIMPORTEEXTRA1': 0.00,
        'CIMPORTEEXTRA2': 0.00,
        'CIMPORTEEXTRA3': 0.00,
        'CIMPORTEEXTRA4': 0.00,
        'CTIMESTAMP': datetime.now().strftime('%m/%d/%Y %H:%M:%S:%f')[:-3],
        'CGTOMOVTO': 0.00,
        'CSCMOVTO': '',
        'CCOMVENTA': 0.00,
        'CIDMOVTODESTINO': 0,
        'CNUMEROCONSOLIDACIONES': 0,
        'COBJIMPU01': ''
    }


def crear_movimiento(datos):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Obtener el siguiente ID disponible
    nuevo_id = obtener_ultimo_id('admMovimientos', 'CIDMOVIMIENTO') + 1
    datos['CIDMOVIMIENTO'] = nuevo_id
    
    # Construir la consulta dinámicamente
    columnas = ', '.join(datos.keys())
    placeholders = ', '.join(['?' for _ in datos])
    valores = tuple(datos.values())
    
    sql = f"INSERT INTO admMovimientos ({columnas}) VALUES ({placeholders})"
    
    cursor.execute(sql, valores)
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return nuevo_id


def obtener_plantilla_asociacion():
    return {
        'CIDDOCUMENTOABONO': 0,
        'CIDDOCUMENTOCARGO': 0,
        'CIMPORTEABONO': 0.00,
        'CIMPORTECARGO': 0.00,
        'CFECHAABONOCARGO': '18991230',
        'CIDDESCUENTOPRONTOPAGO': 0,
        'CIDUTILIDADPERDIDACAMB': 0,
        'CIDAJUSIVA': 0,
    }


def crear_asociacion(datos):
    conn = get_connection()
    cursor = conn.cursor()

    columnas = ', '.join(datos.keys())
    placeholders = ', '.join(['?' for _ in datos])
    valores = tuple(datos.values())

    sql = f"INSERT INTO admAsocCargosAbonos ({columnas}) VALUES ({placeholders})"

    cursor.execute(sql, valores)
    conn.commit()

    ciddoc_abono = datos.get('CIDDOCUMENTOABONO')
    ciddoc_cargo = datos.get('CIDDOCUMENTOCARGO')

    cursor.close()
    conn.close()

    return (ciddoc_abono, ciddoc_cargo)

def actualizar_saldo_documento(ciddocumento, importe_abono):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE admDocumentos
        SET CPENDIENTE = (CPENDIENTE - ?)
        WHERE CIDDOCUMENTO = ?
    """

    cursor.execute(sql, (importe_abono, ciddocumento))
    conn.commit()

    cursor.close()
    conn.close()