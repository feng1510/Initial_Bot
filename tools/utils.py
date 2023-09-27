import datetime


def get_datetime_str(style=0):
    '''
    style=0返回日期_时间字符串
    style=1返回日期字符串
    style=2返回时间字符串
    '''
    time_now = datetime.datetime.now()
    strData = time_now.strftime('%y%m%d')
    strTime = time_now.strftime('%H%M%S')

    if style == 1:
        return strData
    elif style == 2:
        return strTime
    else:
        return strData + '_' + strTime