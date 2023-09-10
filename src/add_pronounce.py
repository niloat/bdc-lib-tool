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
    print(f"Catch signal {signum}")

def get_word_pronounce(lib, word):
    found = [tri for tri in lib if tri['w'] == word]
    cnt = len(found)
    if cnt == 0:
        print("Cannot find word %r" % word)
        return "" 
    return found[0]['p']


def process_word(lib, word):
    found = [tri for tri in lib if tri['w'] == word]
    cnt = len(found)
    print("found %d" % cnt)
    if cnt == 0:
        print("Cannot find word %r" % word)
        return False
    sel = 0
    if cnt > 1:
        idx = 1
        for item in found:
            print(" %d: %s \t %s \t %s" % (idx, item['w'], item['p'],
                                           item['h']))
            idx += 1
        sel = cnt + 1
        while sel < 1 or sel > cnt:
            try:
                sel = input(f"which word should be use[1-{cnt}]: ")
                sel = int(sel)
            except ValueError:
                sel = cnt + 1
            except EOFError:
                return False
        sel -= 1

    sel_word = found[sel]
    return sel_word


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
    dst_lib = './ck/CK-JS.PMS.dbf'
    data = load_word_lib("word.pk")
    print("words in lib: " + str(len(data)))

    table = dbf.Table(dst_lib, codepage='cp936')
    tablesize = len(table)
    print("table size: %d" % tablesize)
    table.open(dbf.DbfStatus.READ_WRITE)
#print(table[tablesize-1])
    #print(table)
    for record in dbf.Process(table):
        for idx in range (1,26):
            f_w = conf.fw + str(idx)
            w = record[f_w].strip()
            if len(w) == 0 :
                continue
            f_p = conf.fp + str(idx)
            p = record[f_p].strip()
            if len(p) > 0:
                continue
            pronounce = get_word_pronounce(data, w)
            print(f"{w} [{pronounce}]")
            f_h = conf.fh + str(idx)
#            word = {'w':w, 'p': record[f_p].strip(), 'h': record[f_h].strip()}
#            print("%d: %r" % (idx, word))
            record[f_p] = pronounce

    table.close()


run()
