import re


page_started = False
current_word = None

connection_types = ['Синонимы', 'Антонимы', 'Гиперонимы', 'Гипонимы']
connection_labels = ['==== {} ===='.format(x) for x in connection_types]
current_connection_words = ['', '', '', '']
type_started = None

def brackets_del(s):
    reg = re.compile('\[\[[^\]]+\]\]')
    words = reg.findall(s)
    return ', '.join([x.replace('[', '').replace(']', '') for x in words])

with open('../../graph/ruwiktionary-20171020-pages-articles-multistream.xml', 'r', encoding='utf-8') as f:
    for line in f:
        ll = line.strip()
        if '<page>' in line.strip():
            if current_word and any(x for x in current_connection_words):
                print(current_word)
                for k, el in enumerate(current_connection_words):
                    if not brackets_del(el):
                        continue
                    print(connection_types[k], brackets_del(el))

            page_started = True
            current_word = None
            current_connection_words = ['', '', '', '']
            type_started = None
        if '</page>' in line.strip():
            page_started = False

        if page_started and '<title>' in ll and '</title>' in ll:
            current_word = ll.replace('<title>', '').replace('</title>', '')

        if current_word is not None and ll in connection_labels:
            type_started = connection_labels.index(ll)
            continue

        if type_started is not None and '====' in ll:
            type_started = None

        if type_started is not None:
            current_connection_words[type_started] += ll
