import re
import datetime

import transliterate


def get_normalized_post_header(post_header):
    normalized_post_header = '-'.join(re.findall(r'\w+', post_header.lower()))

    if transliterate.detect_language(normalized_post_header):
        normalized_post_header = transliterate.translit(
            normalized_post_header,
            reversed=True,
        )
    return normalized_post_header


def get_post_path(post_header):
    normalized_post_header = get_normalized_post_header(post_header)
    today_date = datetime.date.today()

    return '{}-{}-{}'.format(
        normalized_post_header, today_date.month, today_date.day)
