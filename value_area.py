def intervals(start: int, end: int, no_intervals: int):
    """Return evenly spaced numbers over a specified interval. It includes the
    start and end.\nReturns a generator"""
    assert end > start, "start cannot be less than end"
    assert no_intervals > 1, "Number of intervals should be two or more"
    difference = (end - start) / (no_intervals-1)
    while start <= end:
        yield start
        start += difference

def cal_dist(high_prices: iter, low_prices: iter) -> dict:
    """Calculates the distribution of prices. Returns a dictionary with price as key
    and number of times its traded (frequency) as values"""
    assert len(high_prices) == len(low_prices), "Length of high_prices != low_prices"
    high = max(high_prices)
    low = min(low_prices)
    interval = intervals(low, high, no_intervals=50)
    dist = {f: 0 for f in interval}
    for index in range(len(high_prices)):
        for key in dist:
            if high_prices[index] >= key >= low_prices[index]:
                dist[key] += 1
    return dist

def value(dist: dict, percentage: int) -> tuple:
    """Returns the VAH, VAl, POC as a tuple.\n
    :param dist: distribution of the price, gotten from cal_dist()
    :param percentage: the percentage of the distribution used to calculate VAH and VAL
    """
    tpo_list = list(dist.values())
    poc = max(tpo_list)
    poc_price = get_key(poc, dist)
    poc_index = tpo_list.index(poc)
    tpo = sum(tpo_list)
    area_range = percentage * tpo / 100

    price_list = list(dist.keys())

    value_area = poc
    vah_index, val_index = poc_index + 1, poc_index - 1
    len_tpo = len(tpo_list)
    val, vah = 0, 0
    while value_area < area_range:
        if val_index >= 0:
            val = tpo_list[val_index]
        if vah_index < len_tpo:
            vah = tpo_list[vah_index]
        if val_index == 0 and vah_index > len_tpo-1:
            break
        if vah > val or val_index < 0:
            value_area += vah
            vah_index += 1
        elif vah < val or vah_index > len_tpo-1:
            value_area += val
            val_index -= 1
        elif val == vah:
            value_area += val + vah
            vah_index += 1
            val_index -= 1
    vah_index = vah_index if vah_index < len_tpo-1 else len_tpo-1
    val_index = val_index if vah_index >= 0 else 0

    return price_list[vah_index], price_list[val_index], poc_price

def get_key(g_val: any, dictionary: dict) -> any:
    """Finds and returns the first occurrence of a key corresponding to the value in the 'occurrence' dictionary
    Example:
        dic = {A: 10, B: 1, G: 4}
    >> get_key(10, dic)
    A
    """
    for k, val in dictionary.items():
        if g_val == val:
            return k
    return 'value doesn\'t exist'

