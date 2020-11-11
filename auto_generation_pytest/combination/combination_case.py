from functools import reduce
from allpairspy import AllPairs


class Comb(object):
    def __init__(self, data):
        self.data = data
        self.var_type = []
        if data['var'] is not None:
            self.save_type(data['var'])

    def save_type(self, data):
        for i, j in data.items():
            if not isinstance(j[0], str):
                self.var_type.append(i)

    def allpairs(self):
        result = []
        items = []
        for key, value in self.data['var'].items():
            items.append(['"' + key + '":"' + str(i) + '"' for i in value])

        if len(items) == 1:
            return items[0]

        for i in AllPairs(items, n=2):
            if i not in result:
                result.append(','.join(i))

        return result

    def normal(self):

        zipped = []
        need = []

        for key, value in self.data['var'].items():
            zipped.append(['"' + key + '":"' + str(i) + '"' for i in value])
        if len(zipped) != 1:
            for i in zipped[1:]:
                zipped[0] = list(zip(zipped[0], i))
                for j in range(len(zipped[0])):
                    zipped[0][j] = ', '.join(zipped[0][j])

        for i in zipped[0]:
            i = str(i)
            need.append(i)
        return need

    def multiply(self):

        lists = []
        for key, value in self.data['var'].items():
            lists.append(['"' + key + '":"' + str(i) + '"' for i in value])

        def myfunc(list1, list2):
            return [str(i) + ',' + str(j) for i in list1 for j in list2]

        return reduce(myfunc, lists)

    def random(self):
        result = []
        for key, value in self.data['data'].items():
            items = self.data.copy()
            items[key] = ''
            result.append(items)
        return result

    def fusion(self, data):
        need = []
        for i in data['var']:
            i = '{' + i + '}'
            i = eval(i)
            for key, value in i.items():
                if key in self.var_type:
                    i[key] = eval(value)
            if data['data'] and isinstance(data['data'],dict):
                i = dict(i, **self.data['data'])
            elif data['data'] and not isinstance(data['data'],dict):
                print('存在data数据不为dict的情况')
            need.append(i)

        return need
