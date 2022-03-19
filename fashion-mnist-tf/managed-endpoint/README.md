# Creating online managed endpoints in Azure ML

For a detailed explanation of the code, check out the accompanying blog post: [Creating managed online endpoints in Azure ML](https://bea.stollnitz.com/blog/managed-endpoint/).

The `pytorch-model`, `tf-model`, and `sample-request` folders can be re-created with code found under the `pytorch-src` and `tf-src` folders. I've included these generated folders in the project so you can go straight to working with the Azure endpoints without running any code. If you want to run any of the code in the `-src` folders, you'll need to create and activate the conda environment for this project:

```
conda env create -f environment.yml
conda env activate azureml-basics
```

You can find below the steps needed to create and invoke the endpoints in this project.


## Azure setup

* You need to have an Azure subscription. You can get a [free subscription](https://azure.microsoft.com/en-us/free?WT.mc_id=aiml-31508-bstollnitz) to try it out.
* Create a [resource group](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal?WT.mc_id=aiml-31508-bstollnitz).
* Create a new machine learning workspace by following the "Create the workspace" section of the [documentation](https://docs.microsoft.com/en-us/azure/machine-learning/quickstart-create-resources?WT.mc_id=aiml-31508-bstollnitz). Keep in mind that you'll be creating a "machine learning workspace" Azure resource, not a "workspace" Azure resource, which is entirely different!
* If you have access to GitHub Codespaces, click on the "Code" button in this GitHub repo, select the "Codespaces" tab, and then click on "New codespace". 
* Alternatively, if you plan to use your local machine:
  * Install the Azure CLI by following the instructions in the [documentation](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?WT.mc_id=aiml-31508-bstollnitz).
  * Install the ML extension to the Azure CLI by following the "Installation" section of the [documentation](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli?WT.mc_id=aiml-31508-bstollnitz).
* On a terminal window, log into Azure by executing `az login --use-device-code` (if you're not working on Codespaces, you can login by executing `az login`).
* Set your default subscription by executing `az account set -s "<YOUR_SUBSCRIPTION_NAME_OR_ID>"`. You can verify your default subscription by executing `az account show`, or by looking at `~/.azure/azureProfile.json`.
* Set your default resource group and workspace by executing `az configure --defaults group="<YOUR_RESOURCE_GROUP>" workspace="<YOUR_WORKSPACE>"`. You can verify your defaults by executing `az configure --list-defaults` or by looking at `~/.azure/config`.
* You can now open the [Azure Machine Learning studio](https://ml.azure.com/?WT.mc_id=aiml-31508-bstollnitz), where you'll be able to see and manage all the machine learning resources we'll be creating.
* Although not essential to run the code in this post, I highly recommend installing the [Azure Machine Learning extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.vscode-ai).


## Create the models

Execute the following commands:

```
az ml model create -f cloud/model-pytorch-fashion.yml
az ml model create -f cloud/model-tf-fashion.yml
```


## Create and invoke endpoints

Execute the following commands, replacing `endpoint-managed-fashion-X` with names you choose for your endpoints.


### Endpoint 1

```
az ml online-endpoint create -f cloud/endpoint-1/endpoint.yml --name endpoint-managed-fashion-1
az ml online-deployment create -f cloud/endpoint-1/deployment.yml --all-traffic --endpoint-name endpoint-managed-fashion-1
az ml online-endpoint invoke -n endpoint-managed-fashion-1 --request-file sample-request/sample_request.json
```


### Endpoint 2

```
az ml online-endpoint create -f cloud/endpoint-2/endpoint.yml --name endpoint-managed-fashion-2
az ml online-deployment create -f cloud/endpoint-2/deployment.yml --endpoint-name endpoint-managed-fashion-2 --all-traffic
az ml online-endpoint invoke -n endpoint-managed-fashion-2 --request-file sample-request/sample_request.json
```


### Endpoint 3

```
az ml online-endpoint create -f cloud/endpoint-3/endpoint.yml --name endpoint-managed-fashion-3
az ml online-deployment create -f cloud/endpoint-3/deployment.yml --endpoint-name endpoint-managed-fashion-3 --all-traffic
az ml online-endpoint invoke -n endpoint-managed-fashion-3 --request-file sample-request/sample_request.json
```


### Endpoint 4

```
az ml online-endpoint create -f cloud/endpoint-4/endpoint.yml --name endpoint-managed-fashion-4
az ml online-deployment create -f cloud/endpoint-4/deployment.yml --endpoint-name endpoint-managed-fashion-4 --all-traffic
az ml online-endpoint invoke -n endpoint-managed-fashion-4 --request-file sample-request/sample_request.json
```


### Endpoint 5

```
az ml online-endpoint create -f cloud/endpoint-5/endpoint.yml --name endpoint-managed-fashion-5
az ml online-deployment create -f cloud/endpoint-5/deployment.yml --endpoint-name endpoint-managed-fashion-5 --all-traffic
az ml online-endpoint invoke -n endpoint-managed-fashion-5 --request-file sample-request/sample_request.json
```


### Endpoint 6

```
az ml online-endpoint create -f cloud/endpoint-6/endpoint.yml --name endpoint-managed-fashion-6
az ml online-deployment create -f cloud/endpoint-6/deployment-blue.yml --all-traffic --endpoint-name endpoint-managed-fashion-6
az ml online-deployment create -f cloud/endpoint-6/deployment-green.yml --endpoint-name endpoint-managed-fashion-6
az ml online-endpoint update --name endpoint-managed-fashion-6 --traffic "blue=90 green=10"
az ml online-endpoint invoke -n endpoint-managed-fashion-6 --request-file sample-request/sample_request.json
```
