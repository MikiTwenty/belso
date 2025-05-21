# belso.gui.api

from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi import APIRouter, Request, UploadFile, File, Form

from belso.core.processor import SchemaProcessor

router = APIRouter()

@router.post("/validate")
async def validate_schema(request: Request):
    """
    Validate a data sample against a schema.
    Body: { "data": ..., "schema": ..., "schema_format": "json|yaml|xml|belso|pydantic|..." }
    """
    try:
        payload = await request.json()
        data = payload["data"]
        schema = payload["schema"]
        schema_format = payload.get("schema_format", None)
        # Standardizza lo schema in formato Belso
        belso_schema = SchemaProcessor.standardize(schema, from_format=schema_format)
        # Valida i dati
        result = SchemaProcessor.validate(data, belso_schema)
        return JSONResponse({"valid": True, "result": result})
    except Exception as e:
        return JSONResponse({"valid": False, "error": str(e)}, status_code=400)

@router.post("/convert")
async def convert_schema(request: Request):
    """
    Convert a schema between any supported format.
    Body: { "schema": ..., "to": "json|yaml|xml|belso|pydantic|openai|..." }
    Optional: "from_format" se il formato non è auto-detectabile
    """
    try:
        payload = await request.json()
        schema = payload["schema"]
        to = payload["to"]
        from_format = payload.get("from_format", None)
        result = SchemaProcessor.convert(schema, to=to, from_format=from_format)
        # Per i formati serializzati, restituisci testo; per altri, JSON
        if isinstance(result, str):
            return PlainTextResponse(result)
        return JSONResponse({"converted": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

@router.post("/import")
async def import_schema(file: UploadFile = File(...), format: str = Form(None)):
    """
    Import a schema file in any supported format (json, yaml, xml...).
    Returns the standard internal (Belso) format.
    """
    try:
        content = await file.read()
        text = content.decode("utf-8")
        schema = SchemaProcessor.standardize(text, from_format=format)
        # Attenzione: restituisci un oggetto serializzabile in JSON (non una classe)
        # Potresti voler aggiungere un metodo di export "as dict" su Schema
        if hasattr(schema, "model_dump"):
            schema = schema.model_dump()
        return JSONResponse({"schema": schema})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

@router.post("/export")
async def export_schema(request: Request):
    """
    Export a schema to the desired format.
    Body: { "schema": ..., "to": "json|yaml|xml|openai|pydantic|..." }
    Optional: "from_format"
    """
    try:
        payload = await request.json()
        schema = payload["schema"]
        to = payload["to"]
        from_format = payload.get("from_format", None)
        result = SchemaProcessor.convert(schema, to=to, from_format=from_format)
        if isinstance(result, str):
            return PlainTextResponse(result)
        return JSONResponse({"exported": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
