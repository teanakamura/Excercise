"""
指定した番号のファイルのdocstringを読む。
docstringは定義直後のコメントしか該当しない。
"""

import sys
import os
import importlib
from mymodule.path_helpers import get_rel_path_from_working_directory

# 環境変数PYTHONPATHにこのファイルのディレクトリを追加
this_directory_path = os.path.dirname(os.path.realpath(__file__))
# subprocess.run(["export", "PYTHONPATH=$PYTHONPATH:%s" % directory_path], shell = True)
# os.putenv("PYTHONPATH", os.pathsep.join([os.getenv("PYTHONPATH", ""), this_directory_path, execute_directory_path]))
sys.path.append(this_directory_path)

if len(sys.argv) == 1:
    # sys.exit()
    print("実行したい問題の番号（0~99）を入力してください。")
    sys.argv.append(input())
file_num = sys.argv[1]
chapter_num = int(file_num[0]) + 1
import_rel_path = "chapter%d/code/nlp100_%s" % (chapter_num, file_num)
# exexute.pyと違い、importするだけなのでsys.pathには実行ファイルのディレクトリは追加されず、実行ファイルと同ディレクトリのファイルからimportしようとするとerrorとなってしまう。あらかじめsys.pathに追加しておく。
import_abs_path = os.path.join(this_directory_path, import_rel_path)
sys.path.append(os.path.dirname(import_abs_path))
executable_file = importlib.import_module(os.extsep.join(import_rel_path.split('/')))
print(executable_file.__doc__)

sys.path.pop(); sys.path.pop()
