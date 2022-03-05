
import argparse
import os
import warnings

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelBinarizer, KBinsDiscretizer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.compose import make_column_transformer
    
from sklearn.exceptions import DataConversionWarning

warnings.filterwarnings(action="ignore", category=DataConversionWarning)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-test-split-ratio", type=float, default=0.2)
    args, _ = parser.parse_known_args()

    print("Received arguments {}".format(args))

    input_data_path = os.path.join("/opt/ml/processing/input", "order_data_tf.csv")

    print("Reading input data from {}".format(input_data_path))
    model_data = pd.read_csv(input_data_path)
    
    x_columns = model_data.columns
    print(x_columns)
    # Convert to numpy - Classification
    x = model_data[x_columns[1:]].values
    y = model_data[x_columns[:1]].values
    print(x.shape, y.shape)

    split_ratio = args.train_test_split_ratio

    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=split_ratio) 
    
    
    train_x_output_path = os.path.join("/opt/ml/processing/train", "x_train.npy")
    train_y_output_path = os.path.join("/opt/ml/processing/train", "y_train.npy")
    print("Saving split file to {}".format(train_x_output_path))
    test_x_output_path = os.path.join("/opt/ml/processing/test", "x_test.npy")
    test_y_output_path = os.path.join("/opt/ml/processing/test", "y_test.npy")
    print("Saving split file to {}".format(test_x_output_path))
    
    np.save(train_x_output_path, x_train)
    np.save(train_y_output_path, y_train)
    np.save(test_x_output_path, x_test)
    np.save(test_y_output_path, y_test) 


    
