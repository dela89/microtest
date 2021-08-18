import time
import redis
from flask import Flask, render_template

app = Flask(__name__)
redis_db = redis.StrictRedis(host='172.17.0.1', port=6379)

@app.route('/')
def get_statistics():
    #redis_db.set("book.average_word_len", 2)
    #redis_db.set("book.ratio_vowel", 3)
    #redis_db.set("book.occurrences_of_boat_derivatives", 4)
    #redis_db.set("book.occurrences_of_boat", 5)

    retries = 5
    while True:
        try:
            average_word_len = redis_db.get("book.average_word_len")
            ratio_vowel = redis_db.get("book.ratio_vowel")
            occurrences_of_boat_derivatives = redis_db.get("book.occurrences_of_boat_derivatives")
            occurrences_of_boat = redis_db.get("book.occurrences_of_boat")


        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

        return render_template('home.html', ratio_vowel=ratio_vowel, average_word_len = average_word_len,
                               occurrences_of_boat_derivatives=occurrences_of_boat_derivatives,
                               occurrences_of_boat=occurrences_of_boat, totalWords=5)


if __name__ == '__main__':
    get_statistics()

