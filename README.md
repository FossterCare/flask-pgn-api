# flask-pgn-api
python flask api to convert chess single game pgn to mp4 videos and fen to png images



### Installing

install all dependencies

`
pip install -r requirements.txt
`


### running app in development mode

`
export FLASK_APP=pgn-api.py
$ python -m flask run
 * Running on http://127.0.0.1:5000/
`

### runing app in production mode

`
gunicorn --bind 0.0.0.0:5000 -w 4  pgn-api:app
`
use procfile if possible


## usage

### rendering fen as svg and png

 http://127.0.0.1:5000/svg/2b3k1/8/2pqp3/p1p2r2/2PbN3/3PQN2/PP3PP1/4R1K1%20b%20-%20-%208%2035

 http://127.0.0.1:5000/png/2b3k1/8/2pqp3/p1p2r2/2PbN3/3PQN2/PP3PP1/4R1K1%20b%20-%20-%208%2035


### pgn to mp4

http://127.0.0.1:5000/pgn/

upload file from form and submit to download mp4 video

api style usage or scripted approach to convert large number of pgn files

`
pip install httpie
brew install httpie
`

`
http --download -f POST http://127.0.0.1:5000/pgn/  file@file.pgn
`

where file.pgn is the actual filename for single game

you can split a multi game pgn to multiple single game pgn with [pgn-extract](https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/)





## Authors

* **Senthil Nayagam** - *Initial work* - [senthilnayagam](https://github.com/senthilnayagam)



## License

This project is licensed under the MIT License 



## Contributing
 create a issue, and then submit pull requests
