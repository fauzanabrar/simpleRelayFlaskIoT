from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


dataList = []

firstData = {
    "message": "off",
    "timeout": 0,
    "cron": None,
}

dataList.append(firstData)

@app.route('/')
def hello_world():  # put application's code here
    # return jsonify({"hello":"world"})
    return render_template('index.html')


@app.route('/info')
def info():
    return jsonify(dataList[0])

@app.route('/on')
def on():
    data = {
        "message": "on",
        "timeout": 0,
        "cron": None,
    }
    dataList[0] = data
    return jsonify(data)

@app.route('/off')
def off():
    data = {
        "message": "off",
        "timeout": 0,
        "cron": None,
    }
    dataList[0] = data
    return jsonify(data)

@app.route('/timer', methods=['POST'])
def timer():
    timeout = request.args.get('timeout', type=int)
    data = {
        "message": "timer",
        "timeout": timeout,
        "cron": None,
    }
    if len(dataList) != 1:
        dataList[0] = data
    else:
        dataList.insert(0, data)
    return jsonify(data)

@app.route('/timerform', methods=['POST'])
def timerForm():
    timeout = request.form['timer']
    data = {
        "message": "timer",
        "timeout": int(timeout),
        "cron": None,
    }
    if len(dataList) != 1:
        dataList[0] = data
    else:
        dataList.insert(0, data)
    return jsonify(data)

@app.route('/cron', methods=['POST'])
def cron():
    timeout = request.args.get('timeout', type=int)
    cron = request.args.get('cron', type=str)
    data = {
        "message": "cron",
        "timeout": timeout,
        "cron": cron,
    }
    if len(dataList) != 1:
        dataList[0] = data
    else:
        dataList.insert(0,data)
    return jsonify(data)

@app.route('/cronform', methods=['POST'])
def cronform():
    timeout = request.form['timeout']
    cron = request.form['cron']
    data = {
        "message": "cron",
        "timeout": int(timeout),
        "cron": cron,
    }
    if len(dataList) != 1:
        dataList[0] = data
    else:
        dataList.insert(0,data)
    return jsonify(data)

@app.route('/list')
def show_data_list():
    return jsonify(dataList)

@app.route('/delete', methods=['POST'])
def delete():
    if len(dataList) != 1:
        dataList.pop(0)
    else:
        dataList[0]= firstData
    return jsonify(dataList)

if __name__ == '__main__':
    app.run(debug=True)
