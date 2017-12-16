import pickle
import dbf
import signal
import globalvar
import conf 

def load_word_lib(filename):
    pk_file = open(filename, "rb")
    data = pickle.load(pk_file)
    pk_file.close()
    return data

def open_result_table(filename):
    table = dbf.Table(filename, codepage='cp936')
    table.open()
    return table

def sigint_handler(signum, frame):
    global is_sigint_up
    is_sigint_up = True
    print("Catch signal %r" % signum)

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
            print(" %d: %s \t %s \t %s" % (idx, item['w'], item['p'], item['h']))
            idx += 1
        sel = cnt + 1;
        while sel < 1 or sel > cnt:
            try:
                sel = input("which word should be use[1-%d]: " % cnt)
                sel = int(sel)
            except ValueError:
                sel = cnt + 1
                pass
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
    for idx in range (1,conf.maxword):
        fw = conf.fw + str(idx)
        w = record[fw].strip()
        if len(w) == 0 :
            globalvar.word_idx = idx
            break
    print("the last rec: %d, word: %d" % (globalvar.rec_idx, globalvar.word_idx));


def import_word_to_lib(word, table):
    pass

def run():
    global is_sigint_up
    signal.signal(signal.SIGINT, sigint_handler)
    dst_lib = './ck/CK-99.PMS.dbf'
    dst_table = open_result_table(dst_lib)
    track_lib(dst_table)
    data = load_word_lib("word.pk")
    print("words in lib: " + str(len(data)))

    while 1:
        try:
            key = input("Search for word:")
            if is_sigint_up == True:
                raise EOFError
            word = process_word(data, key)
            if word != False:
                print("got word: %r" % word)
                import_word_to_lib(word, dst_table)
            print("")
        except EOFError:
            print("EOF caught")
            dst_table.close()
            break


    dst_table.close()

is_sigint_up = False
run()
