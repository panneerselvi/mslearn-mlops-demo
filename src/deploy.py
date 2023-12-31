# import required libraries
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model, ManagedOnlineEndpoint, ManagedOnlineDeployment, CodeConfiguration
from azure.identity import DefaultAzureCredential
from azure.ai.ml.constants import AssetTypes
import argparse
from datetime import datetime
# Enter details of your AML workspace
subscription_id = "358e870f-f037-490e-8ee3-6c17b7430d54"
resource_group = "sriram.m-rg"
workspace = "mlopsdemo"


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--run-id", dest='run_id',
                        type=str)

    # parse args
    args = parser.parse_args()

    # return args
    return args


if __name__ == "__main__":
    args = parse_args()
    # get a handle to the workspace
    ml_client = MLClient(
        DefaultAzureCredential(), subscription_id, resource_group, workspace
    )

    mlflow_model = Model(
        path=f"runs:/{args.run_id}/model",
        type=AssetTypes.MLFLOW_MODEL,
        name="diabetes-mlops-model",
        description="MLflow model created from run path")
    mlflow_model = ml_client.models.create_or_update(mlflow_model)
    # Define an endpoint name
    endpoint_name = "mlops-endpoint"

    # create an online endpoint
    endpoint = ManagedOnlineEndpoint(
        name=endpoint_name,
        description="this is a diabetes online endpoint",
        auth_mode="key",
        tags={"env": "prod"}
    )
    # ml_client.online_endpoints.create_or_update(endpoint)

    blue_deployment = ManagedOnlineDeployment(
        name='blue',
        endpoint_name=endpoint_name,
        model=mlflow_model,
        instance_type="Standard_D2as_v4",
        instance_count=1,
    )

    ml_client.online_deployments.begin_create_or_update(
        deployment=blue_deployment
    ).result()
