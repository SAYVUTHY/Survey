from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS, cross_origin
import pandas as pd
import uuid

app = Flask(__name__, static_folder="build", template_folder="templates", static_url_path='/')
CORS(app)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/ManholeData", methods=['GET', 'POST'])
def ManholeData():
    if request.method == 'POST':
        data = {
            'x' : request.form['X'],
            'y': request.form['Y'],
            'ID': request.form['IDManhole'],
            'toplevel': request.form['toplevel'],
            'bottomlevel': request.form['bottomlevel'],
            'waterlevel' : request.form['Waterlevel'],
            'settinglevel' : request.form['Settinglevel']
            }
        try:
            ds = pd.read_pickle(f'Data\Manhole.data')
            for i in range(100000):
                uid = str(uuid.uuid4()).replace('-','')
                if uid not in ds.UUID.values:
                    data['UUID'] = uid
                    break

            ds = pd.concat([ds, pd.DataFrame([data])])
        except:
            data['UUID'] = str(uuid.uuid4()).replace('-','')
            ds = pd.DataFrame([data])
        ds.to_pickle(f'Data\Manhole.data')
        return jsonify({'success': 'Completes'})
    if request.method == 'GET':
        ds = pd.read_pickle(f'Data\Manhole.data')

        return jsonify({'success': ds.to_json(orient='records', lines=False)})

if __name__ == '__main__':
    app.run()
