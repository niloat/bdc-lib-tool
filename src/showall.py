import glob
import dbf
import pickle

def read_words(filename):
    words = []
    table = dbf.Table(filename, codepage='cp936')
    tablesize = len(table)
    print("table size: %d" % tablesize)
    table.open()
    print(table[tablesize-1])
    #print(table)
    for record in table:
        for idx in range (1,26):
            f_w = '单词' + str(idx)
            w = record[f_w].strip()
            if len(w) == 0 :
                continue
            f_p = '音标' + str(idx)
            f_h = '词意' + str(idx)
            word = {'w':w, 'p': record[f_p].strip(), 'h': record[f_h].strip()}
            words.append(word)
            print("%d: %r" % (idx, word))

    table.close()
    return words



words = read_words('./ck/CK-JS.PMS.dbf')
#words = read_words('./ck/CK-E1.PMS.dbf')
#print(words)
