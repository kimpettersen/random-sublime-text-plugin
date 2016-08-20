
def get_range(input_text):
    input_text = input_text.replace(' ', '')
    start, stop = input_text.split(',')
    start = int(start)
    stop = int(stop)

    if start > stop:
        raise ValueError('Invalid format. Maybe you meant: {},{}?'.format(stop, start))
    return start, stop
