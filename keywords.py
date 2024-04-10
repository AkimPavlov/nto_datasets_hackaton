import yake

kw_extractor = yake.KeywordExtractor(lan="ru", n=2, dedupLim=0.9, dedupFunc='seqm', windowsSize=1, top=15, features=None)

# Определите текст
text_to_summarize = """На территории Нижегородского кремля рядом с Георгиевской башней стоит памятник уроженцу нижегородской губернии славному лётчику-герою Валерию Чкалову. От памятника к Нижневолжской набережной спускается гигантская Чкаловская лестница. Монументальное сооружение в виде восьмёрки построено в 1949 году. Общее количество ступеней — 560. На пересечениях маршей организованы смотровые площадки. Нижняя часть лестницы выводит к памятнику — установленному на постаменте катеру «Герой», принимавшему участие в Сталинградской битве в составе Волжского военного флота."""

# Извлеките ключевые слова
keywords = kw_extractor.extract_keywords(text_to_summarize)

words = [i[0] for i in keywords]

import pymorphy3

# Инициализируйте объект MorphAnalyzer
morph = pymorphy3.MorphAnalyzer()

result = []
for word in words:
    # Приведите каждое слово к начальной форме
    result.append(' '.join([morph.parse(alone_word)[0].normal_form for alone_word in word.split()]))

# Выведите результат
print(result)

