import json
import codecs

try:
    with codecs.open('errors.txt', 'r', encoding='cp1252') as f:
        lines = f.readlines()
    with codecs.open('errors.json', 'w', encoding='utf-8') as f:
        json.dump({"errors": lines}, f, indent=2)
except Exception as e:
    print(e)
