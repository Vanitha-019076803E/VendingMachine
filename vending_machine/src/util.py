from decimal import Decimal


def sub_list_sum(list, num):
    if Decimal(str(sum(list))) == num:
        return list
    if len(list) > 1:
        for subset in (list[:-1], list[1:]):
            result = sub_list_sum(subset, num)
            if result is not None:
                return result
            

def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
