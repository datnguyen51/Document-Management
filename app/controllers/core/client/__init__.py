from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def format_data_return(response_data=None, response_message=None, response_code="ERROR", response_http_code=200):
    if response_http_code == 200 or response_http_code == 204:
        response_data = jsonable_encoder(response_data)
        return JSONResponse(content=response_data,
                            status_code=response_http_code)
    else:
        return JSONResponse(
            content={
                "error": {
                    "code": response_code,
                    "message": response_message
                }},
            status_code=response_http_code)
