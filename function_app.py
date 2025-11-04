import azure.functions as func
import datetime
import json
import logging
import os

app = func.FunctionApp()


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# @app.function_name(name="RootFunction")
@app.route(route="home", methods=["GET"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    function_directory = os.path.dirname(__file__)
    html_file_path = os.path.join(function_directory, "static", "index.html")
    logging.info(f"processing main")

    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        return func.HttpResponse(body=html_content, 
                                headers={"Content-Type": "text/html"},
                                status_code=200)