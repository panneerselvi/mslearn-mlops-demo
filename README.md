
## Steps

1. The below command used to create or register new dataset in Azure ML Workspace

    ```sh
    az ml data create --name diabetes-dev-folder --path experimentation/data --resource-group sriram.m-rg --workspace-name mlopsdemo
    ```

2. To create and run the new AML Job, use the following command in Azure CLI (V2)

    ```sh
    az ml job create --file src/job.yml --resource-group  sriram.m-rg --workspace-name mlopsdemo
    ```
                       
3. To run the AML Job in Github Actions, we need to create a ServicePrinciple using the below command

    ```sh
    az ad sp create-for-rbac --name "mlops-github-actions-demo" --role contributor \
                                --scopes /subscriptions/358e870f-f037-490e-8ee3-6c17b7430d54/resourceGroups/sriram.m-rg \
                                --sdk-auth
    ```
    
4. To register ML Models in AML Workspace, use the below command

    ```sh
    az ml model create --name diabetes-model --path runs:/<run-id>/model/ --type mlflow_model
    ```