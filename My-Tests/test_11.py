from datetime import datetime;

def diff_between2(d1, d2):
    d1 = datetime.strptime(d1, '%Y-%m-%d %H:%M')
    d2 = datetime.strptime(d2, '%Y-%m-%d %H:%M')
    return abs((d2 - d1).total_seconds())

print(diff_between2("2023-12-12 5:30", "2023-12-12 4:30"));

"""
>>> from datetime import datetime
>>> datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
datetime.datetime(2005, 6, 1, 13, 33)

>>> datetime.strptime('Jun 1 2005', '%b %d %Y').date()
date(2005, 6, 1)

>>> from datetime import datetime
>>> datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
datetime.datetime(2005, 6, 1, 13, 33)


>>> datetime.strptime('Jun 1 2005', '%b %d %Y').date()
date(2005, 6, 1)

datetime.now().date()
datetime.now().time()
"""
