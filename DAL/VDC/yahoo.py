__author__ = 'ict'

import copy

data_offset = {
    "date":     0,
    "open":     1,
    "high":     2,
    "low":      3,
    "close":    4,
    "volume":   5,
    "adjclose": 6,
}


class Yahoo:
    def __init__(self, drivers=None):
        self.drivers = drivers
        self.data = {}

    # data选择有如下几种：
    #   date     - 日期
    #   open     - 开盘价
    #   high     - 最高价
    #   low      - 最低价
    #   close    - 收盘价
    #   volume   - 成交量
    #   adjclose - 复权价
    def create(self, drivers=None, option="adjclose", align=True):
        if drivers is None:
            drivers = self.drivers
        if drivers is None:
            raise Exception("Need input a list of drivers")
        date_set = set()
        tmp_dict = {}
        option_list = option.split(" ")
        for dv in drivers:
            tmp_data = {}
            loaded = True
            if not dv.done():
                loaded = False
                dv.load()
            for item in dv.get_data():
                date = int(item[data_offset["date"]])
                if len(option_list) > 1:
                    tmp_data[date] = []
                    for option_elem in option_list:
                        if len(option_elem) == 0:
                            continue
                        if option_elem not in data_offset:
                            raise Exception("Invalid data option: " + option_elem)
                        tmp_rst = item[data_offset[option_elem]]
                        if option_elem in ["open", "high", "low", "close", "adjclose"]:
                            tmp_rst = float(tmp_rst)
                        if option_elem == "volume":
                            tmp_rst = int(tmp_rst)
                        tmp_data[date].append(tmp_rst)
                elif len(option_list) == 1:
                    if option_list[0] not in data_offset:
                            raise Exception("Invalid data option: " + option_list[0])
                    tmp_data[date] = float(item[data_offset[option_list[0]]])
                else:
                    raise Exception("At least one data option")
                date_set.add(date)
            tmp_dict[dv.get_tag()] = tmp_data
            if not loaded:
                dv.clean()
        date_list = [int(date) for date in list(date_set)]
        date_list.sort()
        if align:
            for stock_id, tmp_data in tmp_dict.items():
                dataset_list = []
                zero_start = False
                nozero = 0
                for date in date_list:
                    if date in tmp_data:
                        if zero_start and nozero == 0:
                            nozero = len(dataset_list)
                        dataset_list.append(tmp_data[date])
                    elif len(dataset_list) == 0:
                        dataset_list.append(0)
                        zero_start = True
                    else:
                        dataset_list.append(copy.copy(dataset_list[-1]))
                if zero_start:
                    for i in range(nozero):
                        dataset_list[i] = copy.copy(dataset_list[nozero])
                self.data[stock_id] = dataset_list
        else:
            for stock_id, tmp_data in tmp_dict.items():
                dataset_list = []
                for date in date_list:
                    if date in tmp_data:
                        dataset_list.append(tmp_data[date])
                self.data[stock_id] = dataset_list

    def data(self, stock_id):
        if stock_id not in self.data:
            return None
        return self.data[stock_id]

    def get_data(self):
        return self.data