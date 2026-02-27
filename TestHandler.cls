USING Progress.Lang.*.
USING OpenEdge.Web.WebResponseWriter.
USING OpenEdge.Web.WebHandler.
USING Progress.Json.ObjectModel.*.

CLASS TestHandler INHERITS WebHandler:

    METHOD OVERRIDE PROTECTED INTEGER HandleGet(INPUT poRequest AS OpenEdge.Web.IWebRequest):
        
        DEFINE VARIABLE oResponse AS WebResponseWriter NO-UNDO.
        DEFINE VARIABLE oBody     AS JsonObject         NO-UNDO.
        DEFINE VARIABLE oItem     AS JsonObject         NO-UNDO.
        
        /* 1. Crear el cuerpo del JSON */
        oBody = NEW JsonObject().
        
        /* 2. Lógica similar a SQL: SELECT * FROM Customer */
        FOR EACH Customer WHERE Customer.Balance > 1000 NO-LOCK:
            oItem = NEW JsonObject().
            oItem:Add("id",     Customer.CustNum).
            oItem:Add("nombre", Customer.Name).
            oItem:Add("saldo",  Customer.Balance).
            
            /* Agregamos el registro al objeto principal */
            oBody:Add("cliente_" + STRING(Customer.CustNum), oItem).
        END.

        /* 3. Enviar la respuesta HTTP */
        oResponse = NEW WebResponseWriter(poRequest).
        oResponse:Entity = oBody.
        oResponse:ContentType = "application/json".
        oResponse:StatusCode = 200.
        oResponse:WriteResponse().
        
        RETURN 0.
        
    END METHOD.
END CLASS.