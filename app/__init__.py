from flask import Flask, request, jsonify, render_template
events_flask = []
app = Flask(__name__)
@app.route('/', methods=['GET'])
def show_events():
    return render_template('index.html', events=events_flask)
if __name__ == '__main__':
    app.run(debug=True)
