

def print_progress(progress, total):
    barwidth = 50
    percent = (progress+1)*100./ total
    unit_lngth = 100. / barwidth
    count = 0
    for ibar in range(barwidth):
        if ibar * unit_lngth < percent:
            count = count + 1
    finish = "#"*count
    unfinish = " "*(barwidth-count)
    print('['+finish+unfinish+']' + '{:2.2f}%'.format(percent)+'\r', end='', flush=True)