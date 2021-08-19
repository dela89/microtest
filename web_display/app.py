import time
import redis
from flask import Flask, render_template

app = Flask(__name__)
redis_db = redis.Redis(host='redis', port=6379)


@app.route('/')
def get_statistics():

    retries = 5
    
    try:
        average_word_len = redis_db.get("book.average_word_len").decode('utf-8')
        ratio_vowel = redis_db.get("book.ratio_vowel").decode('utf-8')
        occurrences_of_boat_derivatives = redis_db.get("book.occurrences_of_boat_derivatives").decode('utf-8')
        occurrences_of_boat = redis_db.get("book.occurrences_of_boat").decode('utf-8')


    except redis.exceptions.ConnectionError as exc:
        if retries == 0:
            raise exc
        retries -= 1
        time.sleep(0.5)

    return render_template('home.html', ratio_vowel=ratio_vowel, average_word_len=average_word_len,
                           occurrences_of_boat_derivatives=occurrences_of_boat_derivatives,
                           occurrences_of_boat=occurrences_of_boat)


if __name__ == '__main__':
    get_statistics()

