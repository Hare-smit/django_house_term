from visual.cx import cx
from visual.ditu import ditu
from visual.huxingtu import huxingtu
from visual.sdt import sdts
from visual.zztxt import zzt

def make_visual(pl):
    cx(pl)
    ditu(pl)
    huxingtu(pl)
    sdts(pl)
    zzt(pl)


def make_main():
    plce_list = ["东莞","广州","惠州","江门","清远","深圳","珠海","湛江","中山","佛山"]
    for plce in plce_list:
        make_visual(plce)

if __name__=="__main__":
    make_main()