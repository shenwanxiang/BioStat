import importlib
import os


def GlobalConf():
    cates = ["common","advance","special"]
    base_path = os.path.dirname(__file__)
    common_child = list()
    advance_child = list()
    special_child = list()
    for cate in cates:
        for files in os.listdir(base_path+'/../'+cate):
            if cate in files:
                module_name = files.split('.')[0]
                module = importlib.import_module(
                    'CeleryTasks.statistics_algorithm.'+cate+'.'+module_name)
                c = getattr(module, module_name)
                obj = c()
                info = getattr(obj, 'get_info')()
                if files.startswith('common'):
                    common_child.append(info)
                elif files.startswith('advance'):
                    advance_child.append(info)
                elif files.startswith('special'):
                    special_child.append(info)
            else:
                continue

    GlobalConf = [
        {"id": "comman",
         "name": "通用方法",
            "children": common_child
         },
         {"id": "advance",
         "name": "进阶方法",
            "children": advance_child
         }, {"id": "special",
         "name": "实验/医学研究",
            "children": special_child
         },


    ]
    return GlobalConf
