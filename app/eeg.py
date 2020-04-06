from flask import Flask
from flask_cors import CORS
import pandas as pd
from sklearn.externals import joblib
from sklearn import pipeline
from sklearn.ensemble import RandomForestClassifier
import argparse
import numpy as np
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


def make_app():

    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route('/')
    def return_prediction():

        #ms = post_id
        # Lines 27-65 copied from https://brainflow.readthedocs.io/en/stable/Examples.html
        # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port

        params = BrainFlowInputParams()
        params.board_id = 1
        params.serial_port = "COM4"
        params.mac_address = "DC:3D:46:E5:10:99"
        
        board = BoardShim(1, params)
        board.prepare_session()

        board.start_stream() # use this for default options
        data = board.get_current_board_data(256) # get latest 256 packages or less, doesnt remove them from internal buffer
        board.stop_stream()
        board.release_session()

        # return 'a string'

        # CONNECT THE DATA TO THE MODEL FOR PREDICTIONS

        # Test Sample Data
        # data = 'https://archlife.org/wp-content/uploads/2020/03/OpenBCI-RAW-right0.txt'

        # column_names = ['index', 'channel1','channel2', 'channel3', 'channel4', 'accel1', 'accel2', 'accel3', 'timestamp', 'aux']
        # dropped_row_indices = [0, 1, 2, 3, 4, 5]

        # df = pd.DataFrame(data=data, columns=column_names)

        # df = df.drop(dropped_row_indices, axis=0).reset_index()
        # df = df.drop(['level_0', 'index', 'timestamp'], axis=1)

        df = pd.DataFrame({'channel1': data[0], 'channel2': data[1], 'channel3': data[2], 'channel4': data[3], 'accel1': data[4], 'accel2': data[5], 'accel3': data[6], 'aux': data[8]})
        
        df = df.dropna(axis=0)

        model = joblib.load('flask_test/rfc.joblib')

        commands_proba = model.predict_proba(df)
        commands_pred = model.predict(df)

        commands_df = pd.DataFrame({'index': df.index, 'predictions':commands_pred})
        commands_df['predictions'] = commands_df['predictions'].astype('int64')
        command_count = commands_df['predictions'].value_counts()
        ccdf = pd.DataFrame({'index': command_count.index, 'predictions':command_count})
        preds = ccdf['index'].values
        command_pred = preds[0]

        return str(command_pred)

    return app
