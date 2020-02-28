from flask import Flask, json
from flask_cors import CORS
import pandas as pd
from sklearn.externals import joblib
from sklearn.neighbors import NearestNeighbors
import numpy as np


def make_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    @app.route('/id/<int:post_id>')

    def home(post_id)

        ms = post_id
        txt = connect_eeg_to_txt(ms)

        column_names = ['index', 'channel1','channel2', 'channel3', 'channel4', 'accel1', 'accel2', 'accel3', 'timestamp', 'aux']
        dropped_row_indices = [0, 1, 2, 3, 4, 5]

        df = pd.read_csv(txt, sep=',', header=None, names=column_names)
        df = df.drop(dropped_row_indices, axis=0).reset_index()
        df = df.drop(['level_0', 'index'], axis=1)

        # Is my destination address formatted correctky?
        model = joblib.load('flask_test/rfc.joblib')
        
        commands = model.predict(df)
        commands_df = pd.DataFrame({'index': commands.index, 'predictions':commands})
        commands_df['predictions'] = commands_df['predictions'].astype('int64')
        commands_sum += commands['predictions']
        commands_avg = (sommands_sum / commands_df.shape[1])
        command = commands_avg.astype('int64')

        return command

    return app


if __name__ == "__main__":
     app.run(debug=True, port = 8080)



# r = requests.get(url = URL, params = PARAMS)
