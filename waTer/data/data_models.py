# -*- coding: utf-8 -*-

class WaterData:
    def __init__(self, data_frame):
        self.data = data_frame.sort_index()
        self.loc = len(data_frame) - 1
        pass

    def update_bar(self):
        """
        每调用一次，返回一个bar的数据
        :return: 
        """

        if self.loc == 0:
            return None, -1
        else:
            data = self.data.iloc[self.loc]
            self.loc -= 1
            return data, 0




            # if __name__ == '__main__':
            #     WaterData()
