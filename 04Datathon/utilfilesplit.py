
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
    parser.add_argument("--train-test-split-ratio", type=float, default=0.3)
    args, _ = parser.parse_known_args()

    print("Received arguments {}".format(args))

    input_data_path = os.path.join("/opt/ml/processing/input", "datathon_full.zip")

    print("Reading input data from {}".format(input_data_path))
    df = pd.read_csv(input_data_path, sep='\t')
    
    
    
    split_ratio = args.train_test_split_ratio
    
    split_output_path = os.path.join("/opt/ml/processing/split", "orderdata_split.csv")
    print("Saving split file to {}".format(split_output_path))

    df.sample(n=3000000, random_state=42).to_csv(split_output_path)


    
