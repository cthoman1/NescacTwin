import re

imperial_pattern = r'\d+\'\s*\d+(\.\d+)?"'
# defining what jumps look like in feet and inches to remove those in case I want to expand this to jumps later


def remove_imperial(result):
    result = re.sub(imperial_pattern, '', result).strip()
    result = re.sub('m', '', result)
    result = re.sub(r'\([^)]*\)', '', result).strip()
    return result


def time_to_seconds(time_str):
    if ':' in time_str:
        minutes, seconds = time_str.split(':')
        total_seconds = int(minutes) * 60 + float(seconds)
    return total_seconds


