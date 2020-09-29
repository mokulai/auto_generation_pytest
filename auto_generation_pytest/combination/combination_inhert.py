def all_case_and_singel_inhert(key1, value1, key2, value2):
    a = []
    if key2 in value2[0]:
        for i in value1:
            item = {}
            item[key1] = i
            for j in value2:
                a.append({**item, **j})
    else:
        for i in value1:
            for j in value2:
                item = {}
                item[key1] = i
                item[key2] = j
                a.append(item)
    return a


def all_case_and_loop_inhert(key1, value1, data2):
    if key1 in data2:
        return data2
    a = []
    for i in value1:
        item = {}
        item[key1] = i
        for j in data2:
            if key1 in j:
                return data2
            a.append(dict(j, **item))
    return a


def singel_case_and_loop_inhert(key1, value1, data):
    a = []
    for i in data:
        item = {}
        item[key1] = value1
        for key, value in i.items():
            if key in item:
                continue
            else:
                item[key] = value
        a.append(item)
    return a


def singel_case_and_singel_inhert(key1, value1, name, data):
    a = []
    for i in data:
        item = {}
        item[key1] = value1
        item[name] = i
        a.append(item)
    return a


