# Carga masiva de pagos a CONTPAQi Comercial Premium

Esta herramienta carga pagos masivos desde un archivo Excel y los aplica a facturas en CONTPAQi Comercial Premium mediante conexión ODBC a SQL Server. Valida clientes, facturas, monedas y existencia previa del pago; crea el documento de pago, su movimiento, asocia el pago a la factura y actualiza el saldo pendiente. El resultado de cada fila se escribe de vuelta en el Excel. El proceso registra todo en un archivo `log.txt`.

## Configuración

El archivo `config.ini` debe estar en la misma carpeta donde se ejecuta el script o el `.exe` (se detecta automáticamente con `utils.obtener_ruta_base`). Puedes usar `config.example.ini` como base.

### Sección `[database]`
- **server:** nombre o IP del servidor SQL Server.
- **database:** base de datos de la empresa CONTPAQi (por ejemplo, `adTU_EMPRESA`).
- **user / password:** credenciales con permisos para leer y escribir en tablas de CONTPAQi.
- **driver:** nombre del controlador ODBC de SQL Server en Windows (por ejemplo, `ODBC Driver 17 for SQL Server`).

Tablas afectadas/consultadas:
- Lectura: `admConceptos`, `admMonedas`, `admClientes`, `admDocumentos`.
- Escritura: `admDocumentos`, `admMovimientos`, `admAsocCargosAbonos`, y actualización de `CPENDIENTE` en `admDocumentos`.

### Sección `[excel]`
- **file:** ruta del archivo Excel (puede ser relativa a la carpeta de ejecución).
- **sheet_name:** nombre de la hoja con los datos, por ejemplo `Datos`.

Estructura esperada de la hoja de datos:
- Las filas 1 y 2 son cabeceras; el procesamiento inicia en la fila 3.
- Columnas leídas por fila:
	- A: código de cliente (`CCODIGOCLIENTE`).
	- D: serie de la factura.
	- E: folio de la factura.
	- G: moneda de la factura (nombre en `admMonedas.CNOMBREMONEDA`).
	- H: fecha de pago (se convierte a formato `YYYYMMDD`).
	- I: serie del pago.
	- J: folio del pago.
	- K: importe del pago (`CTOTAL`).
	- L: impuesto 1 (`CIMPUESTO1`).
	- M: porcentaje de impuesto 1 (`CPORCENTAJEIMPUESTO1`).
	- N: moneda del pago (nombre).
	- O: tipo de cambio (`CTIPOCAMBIO`).
	- P: referencia del pago (`CREFERENCIA`).
- La columna Q se utiliza para escribir el resultado del procesamiento por cada fila.

### Sección `[conceptos]`
- **codigo_factura:** código visible del concepto de factura (`admConceptos.CCODIGOCONCEPTO`).
- **codigo_pago:** código visible del concepto de pago (`admConceptos.CCODIGOCONCEPTO`).

Durante la ejecución, estos códigos se traducen a `CIDCONCEPTODOCUMENTO` y se usan para validar facturas y crear pagos.

## Registro y alertas
- Se crea o actualiza `log.txt` en la misma carpeta donde corre el script o el `.exe`.
- Se registran el inicio, el resultado por fila y el resumen final.

Notas adicionales:
- Las monedas se validan por nombre; deben existir en `admMonedas`.
- El pago se considera duplicado si ya existe combinación de `CSERIEDOCUMENTO`, `CFOLIO` y `CIDCONCEPTODOCUMENTO` en `admDocumentos`.
- Se actualiza el saldo pendiente de la factura (`CPENDIENTE = CPENDIENTE - importe`).

## Licencia
Proyecto bajo Licencia MIT. Ver [LICENSE.md](LICENSE.md).
