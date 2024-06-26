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


event_codes = {
    '55': '1',
    '60': '2',
    '100': '3',
    '200': '4',
    '400': '5',
    '500': '6',
    '600': '7',
    '800': '8',
    '1000': '9',
    '1500': '10',
    'Mile': '11',
    '3000': '12',
    '5000': '13',
    '10000': '14',
    '55H': '15',
    '60H': '16',
    '110H': '17',
    '400H': '18',
    '3000S': '19',
    '4x100': '20',
    '4x400': '21',
    '4x800': '22',
    'DMR': '23',
    'HJ': '24',
    'PV': '25',
    'LJ': '26',
    'TJ': '27',
    'SP': '28',
    'DT': '29',
    'HT': '30',
    'JT': '31',
    'WT': '32',
    'Dec': '33',
    'Hep': '34'
}

