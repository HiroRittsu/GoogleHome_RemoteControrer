from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)


@app.route('/')
def hello_world():
	speaker = request.args.get('speaker')
	pitch = request.args.get('pitch')
	range = request.args.get('range')
	rate = request.args.get('rate')
	volume = request.args.get('volume')
	return 'Hello World!'


@app.route('/ja')
def hello_world_ja():
	return 'こんにちは 世界！'


@app.route('/media/<path:path>')
def send_js(path):
	print(path)
	return send_from_directory("./media/", path)


if __name__ == '__main__':
	app.run()
