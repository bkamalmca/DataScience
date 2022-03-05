import logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)
import argparse
import codecs
import json
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam

max_features = 20000
embedding_dims = 300
filters = 256
kernel_size = 3
hidden_dims = 256

def parse_args():

    parser = argparse.ArgumentParser()

    # hyperparameters sent by the client are passed as command-line arguments to the script
    parser.add_argument('--epochs', type=int, default=1)
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--learning_rate', type=float, default=0.01)

    # data directories
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))
    parser.add_argument('--test', type=str, default=os.environ.get('SM_CHANNEL_TEST'))

    # model directory: we will use the default set by SageMaker, /opt/ml/model
    parser.add_argument('--model_dir', type=str, default=os.environ.get('SM_MODEL_DIR'))

    return parser.parse_known_args()


def save_history(path, history):

    history_for_json = {}
    # transform float values that aren't json-serializable
    for key in list(history.history.keys()):
        if type(history.history[key]) == np.ndarray:
            history_for_json[key] == history.history[key].tolist()
        elif type(history.history[key]) == list:
           if  type(history.history[key][0]) == np.float32 or type(history.history[key][0]) == np.float64:
               history_for_json[key] = list(map(float, history.history[key]))

    with codecs.open(path, 'w', encoding='utf-8') as f:
        json.dump(history_for_json, f, separators=(',', ':'), sort_keys=True, indent=4) 


def get_train_data(train_dir):

    x_train = np.load(os.path.join(train_dir, 'x_train.npy'))
    y_train = np.load(os.path.join(train_dir, 'y_train.npy'))
    print('x train', x_train.shape,'y train', y_train.shape)

    return x_train, y_train


def get_test_data(test_dir):

    x_test = np.load(os.path.join(test_dir, 'x_test.npy'))
    y_test = np.load(os.path.join(test_dir, 'y_test.npy'))
    print('x test', x_test.shape,'y test', y_test.shape)

    return x_test, y_test



def get_model(learning_rate, maxlen):

    # Build the neural network
    model = Sequential()
    model.add(Dense(64, input_dim=maxlen, activation='relu')) # Hidden 1
    model.add(Dense(32, activation='relu')) # Hidden 2
    #model.add(Dense(10, activation='sigmoid')) # Hidden 2
    model.add(Dense(1)) # Output

    learning_rate=0.1
    optimizer = Adam(learning_rate)

    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])
    #model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model


if __name__ == "__main__":

    args, _ = parse_args()

    x_train, y_train = get_train_data(args.train)
    x_test, y_test = get_test_data(args.test)
    
    maxlen = x_train.shape[1]
    model = get_model(args.learning_rate, maxlen)

    monitor = EarlyStopping(monitor='val_loss', min_delta=1e-3, 
                        patience=5, verbose=1, mode='auto', 
                        restore_best_weights=True)

    history = model.fit(x_train,y_train,validation_data=(x_test,y_test),
              callbacks=[monitor],verbose=2,epochs=100)

    save_history(args.model_dir + "/history.p", history)
    
    # create a TensorFlow SavedModel for deployment to a SageMaker endpoint with TensorFlow Serving
    model.save(args.model_dir + '/1')

