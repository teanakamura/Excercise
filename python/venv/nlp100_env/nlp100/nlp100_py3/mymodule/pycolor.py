colors = {'black': '\033[30m',
           'red': '\033[31m',
           'green': '\033[32m',
           'yellow': '\033[33m',
           'blue': '\033[34m',
           'magenta': '\033[35m',
           'cyan': '\033[36m',
           'white': '\033[37m',
           'end': '\033[0m',
           'bold': '\033[1m', # 上書きではなく追加
           'underline': '\033[4m', # 上書きではなく追加
           'invisible': '\033[08m',
           'reverse': '\033[07m'} # 上書きではなく追加

class Pycolor(str):
    """
    出力の文字のフォントを変換するためのクラス
    e.g. Pycolor.black_str('example')
    e.g. Pycolor('example').in_black() or Pycolor().in_black('example')
    e.g. Pycolor.BLACK + 'example' + Pycolor.END
    """
    pass

for color, code in colors.items():
    @classmethod
    def _color_str(cls, str, code = code):
        return code + str + '\033[0m'
    def _in_color(self, code = code):
        return code + self + '\033[0m'
    setattr(Pycolor, color + '_str', _color_str)
    setattr(Pycolor, 'in_' + color, _in_color)
    setattr(Pycolor, color.upper(), code)

def check_color():
    for i in range(38):
        print('\\033[%dm:' % i, '\033[%dmcolor' % i, '\033[0m')
