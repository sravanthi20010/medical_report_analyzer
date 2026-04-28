from deep_translator import GoogleTranslator


def translate_text(text, lang):
    if not text:
        return text
    if lang == 'en':
        return text

    try:
        max_chars = 4000
        if len(text) <= max_chars:
            translated_text = GoogleTranslator(source='auto', target=lang).translate(text)
        else:
            translated_parts = []
            start = 0
            while start < len(text):
                chunk = text[start:start + max_chars]
                translated_parts.append(GoogleTranslator(source='auto', target=lang).translate(chunk))
                start += max_chars
            translated_text = ''.join(translated_parts)

        if not translated_text or translated_text.strip() == text.strip():
            print(f"TRANSLATION WARNING: no change for lang={lang}")
        return translated_text
    except Exception as e:
        print(f"TRANSLATION ERROR ({lang}): {e}")
        return text


def translate_list(items, lang):
    if lang == 'en' or not items:
        return items
    translated = []
    for item in items:
        translated.append(translate_text(item, lang))
    return translated


def translate_lab_results_keys(lab_results, lang):
    if lang == 'en' or not lab_results:
        return lab_results
    translated = {}
    for key, value in lab_results.items():
        translated_key = translate_text(key, lang)
        translated[translated_key] = value
    return translated