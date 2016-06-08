from datetime import date

def get_elements_per_page():
    return int(Prefs['elements_per_page'])

def get_start_music_year():
    value = Prefs['start_music_year']

    if value == 'Now':
        return date.today().year
    else:
        return value

def get_end_music_year():
    value = Prefs['end_music_year']

    if value == 'Now':
        return date.today().year
    else:
        return value

