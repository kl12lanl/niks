from pathlib import Path
import sys

# ============================================================
# Настройки
# ============================================================

# True  -> регистр учитывается, менять его НЕЛЬЗЯ
# False -> регистр НЕ учитывается, его можно менять для каждой буквы отдельно
case_sensitive = True

# Разрешить использовать неидеальные визуальные замены
not_ideal = False

# True  -> сначала пробовать сменить регистр, потом not_ideal
# False -> сначала not_ideal, потом сменить регистр
prefer_case = False

# Пути к файлам
input_file = Path("russian.txt")
output_ru = Path("russian_words.txt")
output_en = Path("russian_words_in_english.txt")
output_pairs = Path("pairs.txt")

# Кодировки файлов
input_encoding = "cp1251"
output_encoding = "utf-8"

# ============================================================
# Идеальные визуальные пары
# ============================================================

HOMOGLYPHS = {
    # Заглавные
    "А": "A",
    "В": "B",
    "Е": "E",
    "К": "K",
    "М": "M",
    "Н": "H",
    "О": "O",
    "Р": "P",
    "С": "C",
    "Т": "T",
    "Х": "X",
    "З": "3", # в моем шрифте похожи

    # Строчные
    "а": "a",
    "е": "e",
    "о": "o",
    "р": "p",
    "с": "c",
    "х": "x",
}

# ============================================================
# Неидеальные замены
# ============================================================

NOT_IDEAL = {
    "ш": "LLl",
    "и": "u",
    "у": "y", # в моем шрифте отличаются
    "к": "k",
    "Ы": "bl",
    "Ь": "b",
}

# ============================================================

if not case_sensitive and not prefer_case and not not_ideal:
    sys.exit(
        "Ошибка конфигурации.\n\n"
        "При case_sensitive=False и prefer_case=False программа должна "
        "сначала использовать неидеальные замены, однако они отключены "
        "(not_ideal=False).\n\n"
        "Исправьте одну из настроек:\n"
        "  • включите prefer_case=True;\n"
        "  • или включите not_ideal=True."
    )


def perfect_same_case(ch: str):
    return HOMOGLYPHS.get(ch)

def perfect_other_case(ch: str):
    return HOMOGLYPHS.get(ch.swapcase())

def not_ideal_same_case(ch: str):
    if not not_ideal:
        return None
    return NOT_IDEAL.get(ch)


def translate_char(ch: str):
    res = perfect_same_case(ch)
    if res:
        return res

    if case_sensitive:
        return not_ideal_same_case(ch)

    checks = (
        [perfect_other_case, not_ideal_same_case]
        if prefer_case
        else [not_ideal_same_case, perfect_other_case]
    )

    for check_func in checks:
        res = check_func(ch)
        if res:
            return res

    return None

def translate_word(word: str):
    result = []

    for ch in word:
        eng = translate_char(ch)

        if eng is None:
            return None

        result.append(eng)

    return "".join(result)


def main():

    if not input_file.exists():
        sys.exit(f"Файл {input_file} не найден.")

    russian_words = []
    english_words = []
    pairs = []

    total = 0
    found = 0

    with input_file.open(encoding=input_encoding) as f:

        for line in f:

            word = line.strip()

            if not word:
                continue

            total += 1

            translated = translate_word(word)

            if translated is None:
                continue

            russian_words.append(word)
            english_words.append(translated)
            pairs.append(f"{word} -> {translated}")

            found += 1

    output_ru.write_text(
        "\n".join(russian_words),
        encoding=output_encoding,
    )

    output_en.write_text(
        "\n".join(english_words),
        encoding=output_encoding,
    )

    output_pairs.write_text(
        "\n".join(pairs),
        encoding=output_encoding,
    )

    print("=" * 50)
    print("Готово.")
    print("=" * 50)
    print(f"Всего слов:          {total}")
    print(f"Подошло слов:        {found}")
    print(f"Не подошло слов:     {total - found}")
    print()
    print("Созданы файлы:")
    print(f"  {output_ru}")
    print(f"  {output_en}")
    print(f"  {output_pairs}")


if __name__ == "__main__":
    main()
