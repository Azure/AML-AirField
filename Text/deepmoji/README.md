# Analyzing Sentiment using DeepMoji as an Azure ML Service

This example uses Azure ML to deploy the trained DeepMoji model as a web service. The deployed web service
then takes a text as input and returns a list of emojis with scores that represent the sentiment of the text.
This example uses the Pytorch implementation of DeepMoji from [here](https://github.com/huggingface/torchMoji) 
which is also mentioned in the original DeepMoji repo.
(For more information on the DeepMoji, see [this link](https://github.com/bfelbo/DeepMoji) and the [paper](https://arxiv.org/abs/1708.00524)).


## Service deployment steps

1. Complete the [Setup steps](../README.md).

2. Deploy the service (also downloads DeepMoji model weights):

   * Linux

         cd AML-AirField/Text/deepmoji
         ./deploy.sh

   * Windows

         cd AML-AirField\Text\deepmoji
         deploy

3. Call the service:

   Find out your service details required to call it.

   * Get the service details and full service id:

         az ml service list realtime

   * Get the service auth keys (use either one):

         az ml service keys realtime -i [full_service_id]

   * Get the service URL:

         az ml service usage realtime -i [full_service_id]

   * Call service

        * Linux

         ./call.sh [service_url] [auth_key]

        * Windows

         call.cmd [service_url] [auth_key]

## Test your deployed service using a UI web page

To demonstrate a simple example of how you can customize your deployed web service, 
we provide a HTML UI web page that is hosted by your deployed service.

To test the UI web page of your deployed service, please refer to [these steps](../../README.md#test-your-deployed-service-using-a-ui-web-page).

## Setting up Local Debugging Environment (Linux only)

If you'd like to speed up your edit->debug cycle, you can run the service directly
on your Linux machine (without building Docker image).

**Requirements:**

Because the DeepMoji repo uses conda to set up requirements, it is best to set up a conda enviornment to locally debug your service. 
You can install Miniconda or Anaconda for Python3.x [here](https://conda.io/docs/user-guide/install/linux.html)

Assuming that you have successfully installed conda, please refer to [these steps](../../README.md#setting-up-local-debugging-environment-linux-only).
The setup_local_debugging.sh script will create a conda enviornment with necessary dependencies to run the DeepMoji service.
