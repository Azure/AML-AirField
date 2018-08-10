# Running YOLOv3 as an Azure ML Service

This example uses Azure ML to deploy the trained YOLOv3 model as a web service. The deployed web service
then takes an image as input and can return either the list of detected objects with probabilities
and coordinates or an image with detected objects tagged
(For more information on the YOLO project, see [this link](https://pjreddie.com/darknet/yolo/)).

From Azure ML perspective, here is what's interesting about this service:
* It hosts it's own HTML UI page (for testing)
* It takes a binary image input "as-is"
* It returns JSON or image as an output
* It has access to inbound Content-Type header and URL parameters
* It specifies proper outbound Content-Type header
* The python code is calling into native C++ library which is using multiple threads.
* Yet it's all done using standard az CLI tools 

## Service deployment steps

Because we are building Darknet, **deployment can only be done from Linux.**

1. Complete the [Setup steps](../../README.md).

2. Deploy the service (also clones and builds the Darknet repo and downloads YOLO model weights):

       cd AML-AirField/Image/yolov3
       ./deploy.sh

3. Call the service:

   Find out your service details required to call it.

   * Get the service details and full service id:

         az ml service list realtime

   * Get the service auth keys (use either one):

         az ml service keys realtime -i [full_service_id]

   * Get the service URL:

         az ml service usage realtime -i [full_service_id]

   * Call service

         ./call.sh [service_url] [auth_key]

## Test your deployed service using a UI web page

To demonstrate a simple example of how you can customize your deployed web service, 
we provide a HTML UI web page that is hosted by your deployed service.

To test the UI web page of your deployed service, please refer to [these steps](../../README.md#test-your-deployed-service-using-a-ui-web-page).

## Setting up Local Debugging Environment

If you'd like to speed up your edit->debug cycle, you can run the service directly
on your Linux machine (without building Docker image).

To setup a local debugging environment, please refer to [these steps](../../README.md#setting-up-local-debugging-environment-linux-only).
