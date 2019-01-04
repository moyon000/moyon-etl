# contructor del obj db
import db

def query1():
    result = []

    # creo obj db OMS de la forma 2
    oms = db.database('oms')
    query = """
            SELECT
                ORDERS.TC_ORDER_ID AS FOLIO, 
                OMSEOMCLPR.PURCHASE_ORDERS_STATUS.DESCRIPTION AS ESTADO 
            FROM PURCHASE_ORDERS_LINE_ITEM 
                INNER JOIN ORDER_LINE_ITEM ON ORDER_LINE_ITEM.MO_LINE_ITEM_ID = PURCHASE_ORDERS_LINE_ITEM.PURCHASE_ORDERS_LINE_ITEM_ID 
                INNER JOIN ORDERS ON ORDER_LINE_ITEM.ORDER_ID = ORDERS.ORDER_ID 
                INNER JOIN PURCHASE_ORDERS ON ORDERS.PURCHASE_ORDER_ID = PURCHASE_ORDERS.PURCHASE_ORDERS_ID 
                INNER JOIN OMSEOMCLPR.PURCHASE_ORDERS_STATUS ON PURCHASE_ORDERS_LINE_ITEM.PURCHASE_ORDERS_LINE_STATUS = OMSEOMCLPR.PURCHASE_ORDERS_STATUS.PURCHASE_ORDERS_STATUS 
            WHERE ORDERS.TC_ORDER_ID LIKE '12758999%';
            """
    oms.cursor.execute(query)
    oms_result = oms.cursor.fetchall()
    oms.cursor.close()

    # creo obj db SAB de la forma 1
    sab = db.database('sab')
    for folio,estado in oms_result:
        query2 = """
                SELECT 
                    b.CNPEDIDO AS ID, 
                    b.CFUNCION AS FUNCION, 
                    b.FCREAREG AS REGISTRO
                FROM f132hist b,
                    (SELECT Max(h.FCREAREG) fecha, h.CNPEDIDO 
                    FROM f132hist h 
                    WHERE h.CNPEDIDO in('%s') 
                    GROUP BY h.CNPEDIDO) query1
                WHERE 
                    b.FCREAREG = query1.fecha 
                    AND b.CNPEDIDO = query1.CNPEDIDO 
                    AND (b.CNPEDIDO in('%s'))
                """ %(folio,folio)
        sab.cursor.execute(query2)
        row = sab.cursor.fetchone()
        
        if not row:
            pass
        else:
            row = {
                'FOLIO'   :folio,
                'ESTADO'  :estado,
                'ID'      :row.ID,
                'FUNCION' :row.FUNCION,
                'REGISTRO':row.REGISTRO }
        result.append(row)
    sab.cursor.close()
    return (result)