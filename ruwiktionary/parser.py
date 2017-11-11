import re


ii = 0
page_started = False
current_word = None
synonyms_started = False
current_synonyms = ''

def brackets_del(s):
    reg = re.compile('\[\[[^\]]+\]\]')
    words = reg.findall(s)
    return 'synonyms:' + ', '.join([x.replace('[', '').replace(']', '') for x in words])

with open('../../graph/ruwiktionary-20171020-pages-articles-multistream.xml', 'r', encoding='utf-8') as f:
    for line in f:
        ll = line.strip()
        if '<page>' in line.strip():
            if current_word and current_synonyms:
                print(current_word)
                print(brackets_del(current_synonyms))

            page_started = True
            current_word = None
            current_synonyms = ''
        if '</page>' in line.strip():
            page_started = False

        if page_started and '<title>' in ll and '</title>' in ll:
            current_word = ll.replace('<title>', '').replace('</title>', '')

        if current_word is not None and '==== Синонимы ====' in ll:
            synonyms_started = True
            continue

        if synonyms_started and '====' in ll:
            synonyms_started = False

        if synonyms_started:
            current_synonyms += ll

        # ii += 1
        # print(line)
        # if ii > 100:
        #     break