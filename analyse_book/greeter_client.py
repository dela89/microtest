# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging

import grpc
import redis
import book_pb2
import book_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    totalwords = 0
    try:
        with grpc.insecure_channel('greeter_server:50051') as channel:
            stub = book_pb2_grpc.GreeterStub(channel)
            test = True
            words = []
            while test:
                for response in stub.SendWord(book_pb2.WordRequest(word='word')):
                    if response.word == 'END_OF_FILE':
                        test = False
                    else:
                        totalwords += 1
                        words.append(response.word)

        redis_db = redis.StrictRedis(host='redis', port=6379)
        vowels = 'aeoiu'
        words_begin_vowel = 0
        ratio_vowel = 0
        total_words = 0
        total_word_len = 0
        average_word_len = 0
        occurrences_of_boat = 0
        occurrences_of_boat_derivatives = 0

        for word in words:
            if "boat" in word and word != "boat" and word != "boats":
                occurrences_of_boat_derivatives += 1

            if word == "boat" or word == "boats":
                occurrences_of_boat += 1

            if word != "" and word[0] in vowels:
                words_begin_vowel += 1

            total_word_len += len(word)

            total_words += 1

        average_word_len = total_word_len / total_words

        ratio_vowel = words_begin_vowel / total_words

        print("average_word_len:", average_word_len)
        print("ratio_vowel:", ratio_vowel)
        print("occurrences_of_boat_derivatives:", occurrences_of_boat_derivatives)
        print("occurrences_of_boat:", occurrences_of_boat)
        redis_db.set("book.average_word_len",average_word_len)
        redis_db.set("book.ratio_vowel",ratio_vowel)
        redis_db.set("book.occurrences_of_boat_derivatives",occurrences_of_boat_derivatives)
        redis_db.set("book.occurrences_of_boat",occurrences_of_boat)

    except Exception as ex:
        print('Client Error: ', ex)

if __name__ == '__main__':
    logging.basicConfig()
    run()

