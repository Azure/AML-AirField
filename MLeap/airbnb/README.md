# Predicting Airbnb Price as an Azure ML Service using a Spark Model with MLeap

This example uses Azure ML to deploy a trained Spark model as a web service. 
We utilize MLeap, an open source Spark package that serializes Spark-trained pipelines
into a portable format and execution engine. 
Because MLeap uses a special lightweight data structure called LeapFrame, it makes it possible to
scored against Spark ML Pipeline in real-time without using a SparkContext or SparkSession.
(For more information on MLeap, see [this link](https://github.com/combust/mleap)).

## Service deployment steps

Requirements:

   * Java 8
   * Scala 2.10 or 2.11
   * Spark

1. Complete the [Setup steps](../README.md).

This example follows the example laid out in the [MLeap demo](https://github.com/combust/mleap-demo/blob/master/notebooks/airbnb-price-regression.ipynb) where it trains a simple linear regression model and a random forest model to predict airbnb prices. The data used for thie model can be downloaded from [here](https://s3-us-west-2.amazonaws.com/mleap-demo/datasources/airbnb.avro)

2. Install SBT

   For Linux systems, follow steps in [this link](https://www.scala-sbt.org/1.0/docs/Installing-sbt-on-Linux.html) \
   For Windows, follow steps in [this link](https://www.scala-sbt.org/1.0/docs/Installing-sbt-on-Windows.html)

3. Package scoring model written in Scala into an uber-jar using sbt-assembly.

Unfortunately, MLeap package does not support LeapFrames in PySpark runtime. Thus, we have to create a scoring method in Scala and package it into an uber-jar so that we can call it from score.py. The scoring method is defined under the directory AML-AirField/MLeap/packagemodels/scoringmodel/src/main/scala 
as AirbnbScoring.scala. \ 
We utilize the sbt-assembly plugin to create an uber-jar.\
For more details in how to use sbt-assembly look [here](https://github.com/sbt/sbt-assembly)

The packaging is done automatically in the deploy step below.

4. Deploy the service (also downloads serialized models):

If you have made changes to the scoring jar file name, you might need to modify the score.py file accordingly.

   * Linux

         cd AML-AirField/MLeap/airbnb
         ./deploy.sh

   * Windows

         cd AML-AirField\MLeap\airbnb
         deploy

5. Call the service:

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
