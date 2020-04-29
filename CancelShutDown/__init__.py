import logging
import os
import json
import azure.functions as func
from datetime import date

# Cancel shutdown for specified Azure Machine Learning Compute Instance, write a row with current date to Azure Table Storage
def main(req: func.HttpRequest, cishutdown: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Get Azure Machine Learning Compute Instance name
    aml_compute_instance = req.params.get('aml_compute_instance')
    if not aml_compute_instance:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('aml_compute_instance')

    if aml_compute_instance:
        logging.info(f'aml_compute_instance: {aml_compute_instance}')
        # Create row to be saved on Azure Table Storage
        data = {
            "PartitionKey" : aml_compute_instance,
            "RowKey" : str(date.today())
        }
        # Save row on Azure Table Storage
        cishutdown.set(json.dumps(data))
        return func.HttpResponse(f"Row {str(date.today())} for {aml_compute_instance} added")
    else:
        return func.HttpResponse(
             "Please pass a compute instance name on the query string or in the request body",
             status_code=400
        )