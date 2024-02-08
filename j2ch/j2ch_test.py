import json

with open("j2ch_new.json", "r", encoding="utf-8") as file:
    j2ch = json.load(file)

with open("shin2kyuu.json", "r", encoding="utf-8") as file:
    shin2kyuu = json.load(file)

# print(len(j2ch))
# print(len(shin2kyuu))

# for j, c in shin2kyuu.items():
#     if j not in j2ch:
#         print(j, c)
#     elif j2ch[j] != c:
#         print(j, c, j2ch[j])


exceptions = {
    "仮託": "假託",  # 仮託
    "帰依": "歸依",  # 帰依, chosen because 歸依 is HSK 4, and 皈依 is not in HSK
    "結髪": "結髮",  # 結髪, 髮 and 髮 differ by one tiny stroke on top right of the 犮
    "元勲": "元勛",  # 元勲, src: wiktionary
    "広州": "廣州",  # 広州
    "行政区画": "行政區劃",  # 行政区画
    "賛同": "贊同",  # 賛同
    "製図": "製圖",  # 製図
    "素麺": "素麵",  # 素麺
    "痴呆": "痴呆",  # 痴呆 https://zh.wikipedia.org/wiki/%E5%A4%B1%E6%99%BA%E7%97%87
    "弁証": "辯證",  # 弁証
    "砲撃": "炮擊",  # 砲撃
    # 招来 apparently 招來 is an alternate form (src wiktionary) and baike's 招徠 entry is way longer
    "招来": "招徠",
    "発布": "發布",  # 発布
    "分布図": "分佈圖",
    "冷麺": "冷麵",  #
    "身分証": "身份證",  #
    "台子": "檯子",  #

    # jmnedict
    "円月": "元月",
    "径直": "徑直",
    "広安": "廣安",
    "広元": "廣元",
    "広陽": "廣陽",
    "日円": "日元",
    "弁別": "辨別",
    "輪廻": "輪迴",

    '剣尖': '劍尖',
    '不穏': '不穩',
    '応変': '應變',
    '散発': '散發',
    '平穏': '平穩',
    '収獲': '收獲',
    '収穫': '收穫',
    '旧制': '舊制',
    '暗々': '暗暗',
    '声誉': '聲譽',
    '自尽': '自盡',
    '燻蒸剤': '燻蒸劑',
    '余熱': '餘熱',
    '余震': '餘震',
    '発毛': '發毛',
    '病状': '病状',
}


def generate_combinations(key, j2ch):
    # Map each character in key to its variant in j2ch, or to itself if not found
    return [''.join(j2ch.get(char, char) for char in key)]


for j, c in exceptions.items():
    c2 = generate_combinations(j, j2ch)
    if c not in c2:
        print(j, c, c2)
