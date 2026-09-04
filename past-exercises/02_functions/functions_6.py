def sort_words(text):
    words = text.split("-")
    words.sort()
    return "-".join(words)


words_text = "python-variable-funcion-computadora-monitor"
print(sort_words(words_text))