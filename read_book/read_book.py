import codecs

def read_book(file_name):

    num_words = 0
    punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''

    with codecs.open(file_name, encoding='utf-8') as f:
        text = f.read()
        f.close()
        words = text.split()
        for word in words:
            word = word.lower()
            for ele in word:
                if ele in punc:
                    word = word.replace(ele, "")

            num_words += 1
            print(word)

    print("Total words read: ", num_words)

if __name__ == '__main__':
    read_book('ToTheLighthouse.txt')
