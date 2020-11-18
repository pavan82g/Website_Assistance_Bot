from translate import Translator


def translateText(strString, strTolang):
    translator = Translator(to_lang=strTolang,from_lang='de')
    translation = translator.translate(strString)
    return (str(translation))


print(translateText('Hallo', 'en'))
