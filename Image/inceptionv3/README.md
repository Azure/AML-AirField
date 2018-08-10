# Running Inceptionv3 as an Azure ML Service

This example uses Azure ML to deploy the trained Inceptionv3 model as a web service. The deployed web service
then takes an image as input and can return the matching category of an image with confidence scores.
(For more information on the Inception model, see [this link](https://www.tensorflow.org/tutorials/image_recogniton)).

## Service deployment steps

1. Complete the [Setup steps](../README.md).

2. Deploy the service (also downloads Inception model weights):

   * Linux

         cd AML-AirField/Image/inceptionv3
         ./deploy.sh

   * Windows

         cd AML-AirField\Image\inceptionv3
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

To setup a local debugging environment, please refer to [these steps](../../README.md#setting-up-local-debugging-environment-linux-only).
