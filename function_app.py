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

@app.route(route="query/normal", methods=["GET"])
def queryNormal(req: func.HttpRequest):
    logging.info(f"processing /query/normal")
    rv = {
        "message": "Hello from Azure Function!",
        "status": "success"
    }
    json_string = json.dumps(rv)

    return func.HttpResponse(body=json_string,
                                headers={'Content-Type': 'json'})

@app.route(route="query/wait", methods=["GET"])
def queryWait(req: func.HttpRequest):
    logging.info(f"processing /query/wait")
    rv = {
        "message": "Hello from Azure Function!",
        "status": "success"
    }
    json_string = json.dumps(rv)

    return func.HttpResponse(body=json_string,
                                headers={'Content-Type': 'json'})                                

@app.route(route="query/missing_index", methods=["GET"])
def queryMissing_index(req: func.HttpRequest):
    logging.info(f"processing /query/missing_index")
    rv = {
        "message": "Hello from Azure Function!",
        "status": "success"
    }
    json_string = json.dumps(rv)

    return func.HttpResponse(body=json_string,
                                headers={'Content-Type': 'json'})        