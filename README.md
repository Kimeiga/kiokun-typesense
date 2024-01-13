# kiokun-typesense

get dictionary_char_xxx.jsonl
get dictionary_word_xxx.jsonl
both from dong-chinese.com/wiki dumps

copy the born child second to last entry from the bottom of the char jsonl to the word jsonl
{"_id":"AwEHQD3qJqA3KjGaw","simp":"𠫓","trad":"𠫓","gloss":"birth","items":[{"source":"unicode","pinyin":"yù","simpTrad":"both","definitions":["give birth","(ancient variant of 育)"]},{"definitions":["(ancient variant of 突)","dash forward"],"pinyin":"tū"}],"pinyinSearchString":"tū tu1 tu"}

looks like its there erroneously

run typesense via systemd (use the tutorial)
probably on the arm server try docker, so that means you should try docker locally first (TODO)         

run prepare_data.py to get all_data.jsonl

feed that to typesense to generate index
using typesense.js, uncomment relevant lines

(you can also make sure that it's working by commenting out the setup lines and uncommenting the search lines at the bottom of that file and running it)
