def table(data, cls = 'default', id = 'default'):
    '''
    Create HTML table
    data: dictionary
    cls: string class of the table
    id: id of the table
    '''
    
    html = ''.join('<th>' + x + '</th>' for x in data[0].keys())
    for d in data:
        html += '<tr>' + ''.join('<td>' + x + '</td>' for x in d.values()) + '</tr>'
    return f'<table class = {cls} id = {id}>' + html + '</table>'
