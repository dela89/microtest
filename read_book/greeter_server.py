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

from concurrent import futures
import logging
import codecs
import grpc

import book_pb2
import book_pb2_grpc


class Greeter(book_pb2_grpc.GreeterServicer):

    def SendWord(self, request_iterator, context):
        num_words = 0
        punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
        with codecs.open('ToTheLighthouse.txt', encoding='utf-8') as f:
            text = f.read()
            f.close()
            words = text.split()
            for word in words:
                word = word.lower()
                for ele in word:
                    if ele in punc:
                        word = word.replace(ele, "")
                response = book_pb2.WordReply(word=word)
                yield response
        response = book_pb2.WordReply(word='END_OF_FILE')
        yield response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    book_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

