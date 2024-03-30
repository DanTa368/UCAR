#! /usr/bin/python3
from typing import List

import rospy

from darknet_result import DarknetResult
import darknet_sdk


def judging_crops(detect_result: List[DarknetResult]):
    rs = []
    for i in detect_result:
        if i.w*i.y <= 1035:
            return
        if "hgzb" in i.label:
            rs.append("黄瓜")
        elif "sd" in i.label:
            rs.append("水稻")
        elif "xm" in i.label:
            rs.append("小麦")
        elif "ymzb" in i.label:
            rs.append("玉米")
    return rs


def F_judging_crops(detect_result: List[DarknetResult]):
    rs = []
    for i in detect_result:
        rs.append(i.label)
    return rs


def F_result(result):
    if "hg" in result:
        return "黄瓜"
    elif "xg" in result:
        return "西瓜"
    elif "ym" in result:
        return "玉米"


def count(result):
    rs = []
    set_result = set(result)
    dict_result = {
        'hg_count': 0,
        'ym_count': 0,
        'xg_count': 0
    }
    max_result = 0
    if 'hg1' in set_result:
        dict_result['hg_count'] += 1
    if 'hg2' in set_result:
        dict_result['hg_count'] += 2
    if 'hg3' in set_result:
        dict_result['hg_count'] += 3
    if 'hg4' in set_result:
        dict_result['hg_count'] += 2
    if 'ym1' in set_result:
        dict_result['ym_count'] += 2
    if 'ym2' in set_result:
        dict_result['ym_count'] += 2
    if 'ym3' in set_result:
        dict_result['ym_count'] += 1
    if 'ym4' in set_result:
        dict_result['ym_count'] += 1
    if 'xg1' in set_result:
        dict_result['xg_count'] += 1
    if 'xg2' in set_result:
        dict_result['xg_count'] += 1
    if 'xg3' in set_result:
        dict_result['xg_count'] += 1
    if 'xg4' in set_result:
        dict_result['xg_count'] += 1
    _count = max(dict_result.values())
    rs.append(str(_count))
    _key = list(dict_result.keys())[list(dict_result.values()).index(_count)]
    rs.append(_key)
    return rs

# if __name__ == '__main__':

