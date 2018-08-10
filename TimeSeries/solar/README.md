# Solar Power Forcasting as an Azure ML Service using IoT Data with CNTK

This example uses Azure ML to deploy a pre-trained CNTK (Microsoft Cognitive Toolkit) model as a web service. The model is a simple LSTM network that is trained on a real-world IoT (Internet of Things) data generated from a solar panel.

Trained on time series data genereated every 30 minutes, this model aims to predict the solar panel array's total power production using initial readings of the day. The training of the model<sup name="link1">[[1]](#f1)</sup> was done from following the steps laid out in the CNTK tutorial available [here](https://github.com/Microsoft/CNTK/blob/master/Tutorials/CNTK_106B_LSTM_Timeseries_with_IOT_Data.ipynb)

The deployed web service takes in a csv data that consists of a sequence of total power production for the day so far in Watt/hour. For example, a three sample input data (in this case, from the same day) can be like

0, 13.97

0, 13.97, 66.35

0, 13.97, 66.35, 207.5

Using these initial readings, the web service will output a prediction of the total power production of the given day. For example, a desired output for the sample input data above will be something like

4778

4778

4778

since the three sample inputs are of the same day squence. (For more information on data, model, and training see [this link](https://github.com/Microsoft/CNTK/blob/master/Tutorials/CNTK_106B_LSTM_Timeseries_with_IOT_Data.ipynb)).

## Service deployment steps

1. Complete the [Setup steps](../README.md).

2. Deploy the service:

   * Linux

         cd AML-AirField/TimeSeries/solar
         ./deploy.sh

   * Windows

         cd AML-AirField\TimeSeries\solar
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

<sub name="f1">1: Instead of the 100 epochs used in the tutorial, our model was trained for 2000 epochs for better accuracy as suggested from the tutorial.</sub>[↩](#link1)
