import datetime
import logging
import os
import json
from datetime import date

import azure.functions as func
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core import Workspace
from azureml.core.compute import ComputeInstance

# Shutdown compute instance when no entry is present on Azure Table Storage
def main(mytimer: func.TimerRequest, cishutdown) -> None: 
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    # Load rows from Azure Table Storage
    message = json.loads(cishutdown)
    logging.info(message)
    # If no entry is present in the Table Storage, stop the compute instance
    if(not any(list(map(lambda x: x['PartitionKey'] == os.environ["aml_compute_instance"] and x['RowKey'] == str(date.today()), message)))):
        
        # Read configuration 
        tenant_id                   = os.environ["tenant_id"]
        subscription_id             = os.environ["subscription_id"]
        service_principal_id        = os.environ["service_principal_id"]
        service_principal_password  = os.environ["service_principal_password"]
        resource_group              = os.environ["resource_group"]
        aml_workspace               = os.environ["aml_workspace"]
        aml_compute_instance        = os.environ["aml_compute_instance"]

        # Set up authentication
        auth = ServicePrincipalAuthentication(
            tenant_id = tenant_id,
            service_principal_id = service_principal_id,
            service_principal_password = service_principal_password)

        # Connect to Azure Machine Learning Workspace
        ws = Workspace(subscription_id = subscription_id,
                    resource_group = resource_group,
                    workspace_name = aml_workspace,
                    auth = auth)
        
        # Stop Compute Instance
        compute_instance = ComputeInstance(ws, aml_compute_instance)
        compute_instance.stop()