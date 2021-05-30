def get_webservertime(host):
    import http.client
    import time
    import datetime
    conn = http.client.HTTPConnection(host)
    conn.request("GET", "/")
    r = conn.getresponse()
    # r.getheaders() #获取所有的http头
    ts = r.getheader('date')  # 获取http头date部分
    # 将GMT时间转换成北京时间
    ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")

    # dt = datetime.datetime(ltime.tm_year, ltime.tm_mon, ltime.tm_mday, ltime.tm_hour, ltime.tm_min, ltime.tm_sec)
    dt = datetime.datetime(ltime.tm_year, ltime.tm_mon, ltime.tm_mday, ltime.tm_hour, ltime.tm_min)
    # time_out = datetime.datetime(2021,6,30,23,59,59)
    # print(dt)
    return dt


def get_beijing_time(host_list=['baidu.com']):
    last_dt = None
    ac_beijing_time = True
    for host in host_list:
        dt = get_webservertime(host)
        if last_dt is None:
            last_dt = dt
        if dt != last_dt:
            return None
    return last_dt


# ['baidu.com','lol.qq.com','qq.com']
# print(get_beijing_time())
