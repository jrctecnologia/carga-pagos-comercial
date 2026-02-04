import sys

from contpaqi_utils import (
    actualizar_saldo_documento,
    crear_documento,
    obtener_id_moneda,
    obtener_plantilla_documento,
    crear_movimiento,
    obtener_plantilla_movimiento,
    obtener_plantilla_asociacion,
    crear_asociacion,
)
from excel_utils import imprime_resultado, formatea_fecha_pago, leer_filas_desde_excel
from utils import _handle_exception, show_msgbox, log_line
from validaciones import cliente_existe, factura_existe, pago_existe, buscar_id_concepto_por_codigo

from config import EXCEL_FILE, SHEET_NAME, CODIGO_CONCEPTO_FACTURA, CODIGO_CONCEPTO_PAGO

sys.excepthook = _handle_exception

if __name__ == "__main__":
    # Cargar codigo de conceptos desde config.ini
    concepto_factura = buscar_id_concepto_por_codigo(CODIGO_CONCEPTO_FACTURA)
    concepto_pago = buscar_id_concepto_por_codigo(CODIGO_CONCEPTO_PAGO)
    
    id_concepto_factura = concepto_factura['cidconceptodocumento'] if concepto_factura else None
    id_concepto_pago = concepto_pago['cidconceptodocumento'] if concepto_pago else None
    
    if not id_concepto_factura or not id_concepto_pago:
        log_line("Error: No se pudieron cargar los conceptos desde la configuracion.")
        show_msgbox("error al realizar la operacion")
        sys.exit(1)
    
    facturas = leer_filas_desde_excel()
    total_registros = len(facturas)
    errores = 0
    log_line(f"Procesando {total_registros} registro(s)...")
    
    for fila, codigo_cliente, serie_factura, folio_factura, moneda_factura, fecha_pago, serie_pago, folio_pago, importe_pago, impuesto1, porc_impuesto1, moneda_pago, tipo_cambio, referencia in facturas:
        resultado = None
        datos_cliente = None
        
        # Validar que existe la moneda de la factura
        id_moneda_factura = obtener_id_moneda(moneda_factura)
        if not id_moneda_factura:
            resultado = f"Moneda de factura no existe: {moneda_factura}"
        
        # Validar que existe la moneda del pago
        if resultado is None:
            id_moneda_pago = obtener_id_moneda(moneda_pago)
            if not id_moneda_pago:
                resultado = f"Moneda de pago no existe: {moneda_pago}"
        
        # Validar cliente existe (primera validación)
        if resultado is None:
            datos_cliente = cliente_existe(codigo_cliente)
        if not datos_cliente:
            resultado = "Cliente no existe"
        # Solo continuar si el cliente existe
        else:
            id_factura = factura_existe(serie_factura, folio_factura, id_concepto_factura)
            if not id_factura:
                resultado = "Factura no existe o no tiene saldo pendiente"
        # Solo continuar si cliente y factura existen
        if resultado is None and pago_existe(serie_pago, folio_pago, id_concepto_pago):
            resultado = f"Pago ya existe (ID Factura: {id_factura})"
        elif resultado is None:
            datos_nuevo_pago = obtener_plantilla_documento()
            datos_nuevo_pago['CIDCONCEPTODOCUMENTO'] = id_concepto_pago
            datos_nuevo_pago['CSERIEDOCUMENTO'] = serie_pago
            datos_nuevo_pago['CFOLIO'] = folio_pago
            datos_nuevo_pago['CFECHA'] = formatea_fecha_pago(fecha_pago)
            datos_nuevo_pago['CIDCLIENTEPROVEEDOR'] = datos_cliente['cidclienteproveedor']
            datos_nuevo_pago['CRAZONSOCIAL'] = datos_cliente['crazonsocial']
            datos_nuevo_pago['CRFC'] = datos_cliente['crfc']
            datos_nuevo_pago['CTOTAL'] = importe_pago
            datos_nuevo_pago['CIMPUESTO1'] = impuesto1 if impuesto1 else 0.00
            datos_nuevo_pago['CPORCENTAJEIMPUESTO1'] = porc_impuesto1 if porc_impuesto1 else 0.00
            datos_nuevo_pago['CNETO'] = (importe_pago if importe_pago else 0.00) - (impuesto1 if impuesto1 else 0.00)
            datos_nuevo_pago['CIDMONEDA'] = id_moneda_pago if id_moneda_pago else 1
            datos_nuevo_pago['CTIPOCAMBIO'] = tipo_cambio if tipo_cambio else 1
            datos_nuevo_pago['CREFERENCIA'] = referencia if referencia else ''
            datos_nuevo_pago['CIDCUENTA'] = concepto_pago['cidcuenta']
            
            try:
                documento_creado = crear_documento(datos_nuevo_pago)
            except Exception as exc:
                resultado = f"Error creando documento: {exc}"
            else:
                if not documento_creado:
                    resultado = "Error creando documento: sin ID devuelto"
                else:
                    try:
                        # Crear el movimiento del documento solo si el documento fue exitoso
                        datos_nuevo_movimiento = obtener_plantilla_movimiento()
                        datos_nuevo_movimiento['CIDDOCUMENTO'] = documento_creado
                        datos_nuevo_movimiento['CNUMEROMOVIMIENTO'] = 1
                        datos_nuevo_movimiento['CFECHA'] = formatea_fecha_pago(fecha_pago)
                        datos_nuevo_movimiento['CTOTAL'] = importe_pago
                        datos_nuevo_movimiento['CIMPUESTO1'] = impuesto1 if impuesto1 else 0.00
                        datos_nuevo_movimiento['CPORCENTAJEIMPUESTO1'] = porc_impuesto1 if porc_impuesto1 else 0.00
                        datos_nuevo_movimiento['CNETO'] = (importe_pago if importe_pago else 0.00) - (impuesto1 if impuesto1 else 0.00)

                        movimiento_creado = crear_movimiento(datos_nuevo_movimiento)
                        # Crear asociación pago-factura
                        try:
                            datos_asoc = obtener_plantilla_asociacion()
                            datos_asoc['CIDDOCUMENTOABONO'] = documento_creado  # pago
                            datos_asoc['CIDDOCUMENTOCARGO'] = id_factura        # factura
                            datos_asoc['CIMPORTEABONO'] = importe_pago if importe_pago else 0.00
                            datos_asoc['CIMPORTECARGO'] = importe_pago if importe_pago else 0.00
                            datos_asoc['CFECHAABONOCARGO'] = formatea_fecha_pago(fecha_pago)

                            crear_asociacion(datos_asoc)
                            
                            # Actualizar saldo de la factura, descontando el pago
                            actualizar_saldo_documento(id_factura, importe_pago)
                            
                            resultado = f"OK - ID Pago: {documento_creado}, ID Movimiento: {movimiento_creado}, Asociacion creada"
                        except Exception as exc:
                            resultado = f"OK - ID Pago: {documento_creado}, ID Movimiento: {movimiento_creado}, Asociacion ERROR: {exc}"
                    except Exception as exc:
                        resultado = f"Error creando movimiento: {exc}"
            
        # Escribir resultado en el Excel
        imprime_resultado(EXCEL_FILE, SHEET_NAME, fila, resultado)

        log_line(f"Fila {fila}: {resultado}")

        if not (resultado and resultado.startswith("OK -") and "ERROR" not in resultado):
            errores += 1

    if total_registros == 0:
        log_line("No se encontraron registros para procesar.")
        show_msgbox("error al realizar la operacion")
    elif errores == 0:
        log_line(f"Completado: {total_registros} registro(s) procesados. Sin errores.")
        show_msgbox("procesado correctamente")
    else:
        log_line(f"Completado: {total_registros} registro(s) procesados. Con errores: {errores}.")
        show_msgbox("procesado con errores")

