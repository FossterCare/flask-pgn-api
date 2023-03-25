import chess
import chess.pgn
import chess.svg
import cairosvg

from flask import Flask, Response, flash, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
import io

#import tempfile
import cv2
import uuid
import numpy as np

UPLOAD_FOLDER = 'tmp'
ALLOWED_EXTENSIONS = {'pgn' }


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

@app.route('/')
def hello_world():
	return redirect("/pgn")

@app.route('/png/<path:path>')
def render_png(path):
	board = chess.Board(path)
	svg = chess.svg.board(board=board)
	png_data2x = cairosvg.svg2png(bytestring=svg,output_height=800,output_width=800)
	return Response(png_data2x,mimetype='image/png')



@app.route('/svg/<path:path>')
def render_svg(path):
	board = chess.Board(path)
	svg = chess.svg.board(board=board)
	return Response(svg,mimetype='image/svg+xml')


@app.route('/<fen>')
def render_fen2(fen):
	return 'fen'



def pgn_to_mp4(pgn_filename,uuid_filename):
	#pgn = io.StringIO(pgn_upload_filename.read().decode("utf-8") )
	pgn = open(pgn_filename)
	first_game = chess.pgn.read_game(pgn)
	board = first_game.board()
	frame_array = []
	fps = 1
	index = 0
	#uuid_filename = str(uuid.uuid4())

	pathOut = "tmp/" + uuid_filename + ".mp4" #mp4_filename
	width = 800
	height = 800
	size = (width,height)
	out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'MP4V'), fps, size)

	index = 1

	for move in first_game.mainline_moves():
		board.push(move)
		print(move)
		print(index)
		lastmove = board.peek()
		data = chess.svg.board(board=board,lastmove=lastmove)
		##png_data = cairosvg.svg2png(bytestring=data)
		png_data2x = cairosvg.svg2png(bytestring=data,output_height=800,output_width=800)
		nparr = np.fromstring(png_data2x, np.uint8)
		img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		frame_array.append(img_np)
		#	file_write(index,board,new_directory )
		index += 1

	print(len(frame_array))
	for i in range(len(frame_array)):
		# writing to a image array
		out.write(frame_array[i])

	out.release()
	return pathOut



def pgn_to_images(pgn_filename,uuid_filename):
	#pgn = io.StringIO(pgn_upload_filename.read().decode("utf-8") )
	pgn = open(pgn_filename)
	first_game = chess.pgn.read_game(pgn)
	board = first_game.board()
	frame_array = []
	fps = 1
	index = 0
	#uuid_filename = str(uuid.uuid4())

	pathOut = "tmp/" + uuid_filename + ".mp4" #mp4_filename
	width = 800
	height = 800
	size = (width,height)
	out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'MP4V'), fps, size)

	index = 1

	for move in first_game.mainline_moves():
		board.push(move)
		print(move)
		print(index)
		lastmove = board.peek()
		data = chess.svg.board(board=board,lastmove=lastmove)
		##png_data = cairosvg.svg2png(bytestring=data)
		png_data2x = cairosvg.svg2png(bytestring=data,output_height=800,output_width=800)
		nparr = np.fromstring(png_data2x, np.uint8)
		img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		frame_array.append(img_np)
		#	file_write(index,board,new_directory )
		index += 1

	print(len(frame_array))
	for i in range(len(frame_array)):
		# writing to a image array
		out.write(frame_array[i])
		filename = "tmp/" + uuid_filename + "_" + str(i+1) + ".png"
		cv2.imwrite(filename, frame_array[i])

	out.release()
	return pathOut



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/pgn/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uuid_filename = str(uuid.uuid4())
            pgn_filename= os.path.join(app.config['UPLOAD_FOLDER'], uuid_filename + '.pgn')
            file.save(pgn_filename)

            mp4_file = pgn_to_mp4(pgn_filename,uuid_filename)
            print(mp4_file)

            return send_file(mp4_file,mimetype="video/mp4",as_attachment=True)
    return '''
    <!doctype html>
    <title>Upload PGN File with one game</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/pgn2/', methods=['GET', 'POST'])
def upload_file_images():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uuid_filename = str(uuid.uuid4())
            pgn_filename= os.path.join(app.config['UPLOAD_FOLDER'], uuid_filename + '.pgn')
            file.save(pgn_filename)

            mp4_file = pgn_to_images(pgn_filename,uuid_filename)
            print(mp4_file)

            return send_file(mp4_file,mimetype="video/mp4",as_attachment=True)
    return '''
    <!doctype html>
    <title>Upload PGN File with one game</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''



if __name__ == "__main__":
	app.run()