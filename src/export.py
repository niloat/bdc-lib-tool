import glob
import dbf
import pickle
import conf


def read_words(filename):
    words = []
    table = dbf.Table(filename, codepage='cp936', unicode_errors='ignore')
    table.open()
    for record in table:
        for idx in range(1, 26):
            try:
                f_w = '单词' + str(idx)
                w = record[f_w].strip()
                if len(w) == 0:
                    continue
                f_p = '音标' + str(idx)
                f_h = '词意' + str(idx)
                print(record[f_w])
                tmp_p = record[f_p].strip()
                tmp_h = record[f_h].strip()
                word = {'w': w, 'p': tmp_p, 'h': tmp_h}
                words.append(word)
            except:
                print("exception=", record[f_w])
                continue

    table.close()
    return words


def walk_dir():
    path = "./ck/*.PMS.dbf"
    files = sorted(glob.glob(path))
    words = []
    for f in files:
        words = words + read_words(f)
        print("%r words %r" % (f, len(words)))
    output = open("word.pk", "wb")
    pickle.dump(words, output)
    output.close()


walk_dir()
