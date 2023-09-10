import pickle
import dbf
import signal
import globalvar
import conf
import csv


def load_word_lib(filename):
    pk_file = open(filename, "rb")
    data = pickle.load(pk_file)
    pk_file.close()
    return data


def open_result_table(filename):
    table = dbf.Table(filename, codepage='cp936')
    table.open(dbf.DbfStatus.READ_WRITE)
    return table


def sigint_handler(signum, frame):
    global is_sigint_up
    is_sigint_up = True
    print(f"Catch signal {signum}")


def process_word(lib, word):
    found = [tri for tri in lib if tri['w'].lower() == word.lower()]
    cnt = len(found)
#    print("found %d" % cnt)
    if cnt == 0:
        print("Cannot find word %r" % word)
        return False
    sel = 0
    if cnt > 1:
        for item in found:
            if len(item['p']) > 0:
                return item
    return found[0]


def track_lib(table):
    if globalvar.rec_idx != -1:
        return
    globalvar.rec_idx = len(table)
    record = table[globalvar.rec_idx-1]
    for idx in range(1, conf.maxword + 1):
        fw = conf.fw + str(idx)
        w = record[fw].strip()
        if len(w) == 0:
            globalvar.word_idx = idx
            break
    print("the last rec: %d, word: %d" % (globalvar.rec_idx,
                                          globalvar.word_idx))


def import_word_to_lib0(word, table):
    record = table[globalvar.rec_idx-1]
    idx = globalvar.word_idx
    f_w = conf.fw + str(idx)
    f_p = conf.fp + str(idx)
    f_h = conf.fh + str(idx)
    record[f_w] = word['w']
    record[f_p] = word['p']
    record[f_h] = word['h']
    idx = idx + 1
    if idx == 26:
        idx = 1
        globalvar.rec_idx += 1
        table.append()
    globalvar.word_idx = idx


def import_word_to_lib(word, table):
    record = table[globalvar.rec_idx-1]
    for rec in dbf.Process([record]):
        idx = globalvar.word_idx
        f_w = conf.fw + str(idx)
        f_p = conf.fp + str(idx)
        f_h = conf.fh + str(idx)
        record[f_w] = word['w']
        record[f_p] = word['p']
        record[f_h] = word['h']
    idx = idx + 1
    if idx == 26:
        idx = 1
        globalvar.rec_idx += 1
        table.append()
    globalvar.word_idx = idx


def run():
    global is_sigint_up
    signal.signal(signal.SIGINT, sigint_handler)
    src_list = []
    data = load_word_lib("word.pk")
    with open('x3.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            src_list.append(row)

    """
        print(src_list)
        for row in src_list:
            print(f"{row[0]} : {row[1]}")

        for row in src_list:
            key = row[0]
            word = process_word(data, key)
#        if word == False:
#            break
        return

    if len(src_list) > 0:
        return
    """

    dst_lib = './ck/CK-X3.PMS.dbf'
    dst_table = open_result_table(dst_lib)
    track_lib(dst_table)
    print("words in lib: " + str(len(data)))

    for row in src_list:
        key = row[0]
        word = process_word(data, key)
        if word == False:
            word = {'w': key, 'p': '', 'h': row[1]}
        word['h'] = row[1]
        print(f"got word: {word}")
        import_word_to_lib(word, dst_table)
        print("")
    dst_table.close()


run()
