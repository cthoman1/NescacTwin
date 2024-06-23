import re

imperial_pattern = r'\d+\'\s*\d+(\.\d+)?"'
# defining what jumps look like in feet and inches to remove those in case I want to expand this to jumps later


def remove_imperial(result):
    result = re.sub(imperial_pattern, '', result).strip()
    result = re.sub('m', '', result)
    result = re.sub(r'\([^)]*\)', '', result).strip()
    return result

