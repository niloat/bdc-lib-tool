import glob 
import dbf
import pickle

def read_words(filename):
    words = []
    table = dbf.Table(filename, codepage='cp936')
    table.open()
    for record in table:
        for idx in range (1,25):
            f_w = '单词' + str(idx)
            w = record[f_w].strip()
            if len(w) == 0 :
                continue
            f_p = '音标' + str(idx)
            f_h = '词意' + str(idx)
            word = {'w':w, 'p': record[f_p].strip(), 'h': record[f_h].strip()}
            words.append(word)
            
    table.close()
    return words


def walk_dir():
    path = "./ck/*.PMS.dbf"
    files = sorted(glob.glob(path))
    words = [];
    for f in files:
        words = words + read_words(f)
        print("%r words %r" % (f, len(words)))
    output = open("word.pk", "wb")
    pickle.dump(words, output);
    output.close()


walk_dir()
