# AWS Lambda add layers steps


## Steps to create pandas package in virtual env from EC2/Sagemaker instance  

* Create venv and install pandas  (used python3.7)
  mkdir python
  cd python
  python3 -m venv env
  source env/bin/activate
  python --version
  pip3 install pandas  
  
* Create sub folder python to copy only site packages - due to lambda 250 MB size limit uncompressed
  cd python
  cp -r ../env/lib/python3.7/site-packages/* .
  
* zip the directory and copy to s3  
  zip -r pandas_layer.zip python 
  aws s3 cp pandas_layer.zip s3://dgx-ds-use1-dev-landing-s3/lambda-layers/

* Add layers to Lambda function - Python3.7 runtime

* The function executed with python module

* To install zip 
  sudo yum install zip
