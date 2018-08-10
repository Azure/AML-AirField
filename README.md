# Ready to use scoring engines for Image, Text and Time Series processing

Demo of how to use Azure ML to deploy various models for Image, Text and Time Series processing as a web service.

We currently provide steps to deploy Azure ML services for the following models:
   * Images
        * [YOLOv3 (Darknet)](./Image/yolov3/)
        * [Inceptionv3 (Tensorflow)](./Image/inceptionv3/)
   * Text
        * [DeepMoji (PyTorch)](./Text/deepmoji/)
   * Time Series
        * [Forcasting Solar Power Production using IoT Data (CNTK)](./TimeSeries/solar)
   * MLeap
        * [Airbnb Price Prediction (PySpark)](./MLeap/airbnb)

## Setup steps

You will need an Azure subscription to deploy the web service. You can get a free one
[here](https://azure.microsoft.com/en-us/free/).

1. Install Azure CLI (see the instructions
[here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)).

2. Install Azure Machine Learning (ML) CLI
(see the instructions [here](https://docs.microsoft.com/en-us/azure/machine-learning/desktop-workbench/deployment-setup-configuration)).

3. Create an Azure ML model management account.

   Example:

       az ml account modelmanagement create -n [account_name] -l westcentralus -g [resource_group_name]

4. Setup an execution environment (both local and cluster would work):

   Example (using bigger agent VMs for faster computation):

       az ml env setup --cluster -n [environment_name] -l westcentralus -g [resource_group_name] --agent-count 3 --agent-vm-size Standard_D4_v2

   If that command fails because you are not allowed creating bigger VMs, or don't heave enough cores in your subscription,
   then retry without `--agent-vm-size` parameter (note that scoring will be slower):

       az ml env setup --cluster -n [environment_name] -l westcentralus -g [resource_group_name] --agent-count 3

5. Clone the GitHub repo and get the files.

       git clone https://github.com/Azure/AML-AirField

6. Navigate to one of directories listed below and read readme.md and then run `./deploy.sh`

   We currently provide steps to deploy Azure ML services for the following models:
   * Images
        * [YOLOv3 (Darknet)](./Image/yolov3/)
        * [Inceptionv3 (Tensorflow)](./Image/inceptionv3/)
   * Text
        * [DeepMoji (PyTorch)](./Text/deepmoji/)
   * Time Series
        * [Forcasting Solar Power Production using IoT Data (CNTK)](./TimeSeries/solar)
   * MLeap
        * [Airbnb Price Prediction (PySpark)](./MLeap/airbnb)

## Test your deployed service using a UI web page

To demonstrate a simple example of how you can customize your deployed web service, 
we provide a HTML UI web page that is hosted by your deployed service.
Because the service requires authentication keys to call to it directly, you must disable authentication of
your service in order to use the HTML page we have provided in our exmaples.

:warning: **!!! Note that your service will be publicly exposed if you disable authentication !!!** :warning:

To disable authentication of your service:

   * Get your deployed service's name:

         kubectl get services

   * Edit your service's configuration:

         kubectl label --overwrite services [service_name] auth.enabled=false

   * View your UI web page by going to `your_service_url/ui` (replace `/score` with `/ui`)

        *If you do not know your service URL, you can get it by running:*

         az ml service list realtime                            # Get your full service id
         az ml service usage realtime -i [full_service_id]      # Get your service URL

## Setting up Local Debugging Environment (Linux only)

If you'd like to speed up your edit->debug cycle, you can run the service directly
on your Linux machine (without building Docker image) by following the steps below.

1. Setup environment for local debugging:

   Move to the top level directory of the service you are trying to setup a local debugging enviornment. 
   (ex. cd AML-AirField/Image/yolov3)
   Run

        ./setup_local_debug.sh

   **NOTE**: The main scoring file must be called `score.py`. If not, `main.py` should be changed accordingly after
   this step.

2. Run service locally:

        ./local_run.sh

   The service will be listening on port 9090 by default.

3. Call the service (from a separate terminal window):

        ./call.sh 127.0.0.1:9090/score

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
