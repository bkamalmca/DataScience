# AWS Lambda Services

* ### Lambda Read / write files from s3  
  To read a file using pandas and using other pandas functionality, the pandas and other related libraries must be included.   
  There is Add layer capability to package all the required libraries and add as a layer.  
  Refer to AWSLambdaLayers.md for creating package.  
  The code file lambda_s3_read_write.py - pandas read_csv and write_csv cannot be used directly due to remote access which needed s3f3 libraries.   
  Instead use the io.StringIO to read the file and return into dataframe for further processing.
   
* ### Lambda SES
  To send email or email attachments, the SES service can be used as shown in sample code - lambda_ses.py

* ### Lambda S3 trigger event
  To trigger lambda function based on s3 file event, add the trigger to lambda function.   
  The sample code is used to read the content of s3 from boby of response message from event.   
  Then parse the message using json method for further processing need. 


    