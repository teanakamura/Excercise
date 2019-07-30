"""
指定した番号のファイルを実行する。
"""

import subprocess
import sys
import os
from mymodule.path_helpers import get_rel_path_from_working_directory
from IPython import embed

# 環境変数PYTHONPATHにこのファイルのディレクトリを追加
# sys.path.append()だとsubprocess実行時にsys.pathが初期化されるので意味がないことに注意。
directory_path = os.path.dirname(os.path.realpath(__file__))
# subprocess.run(["export", "PYTHONPATH=$PYTHONPATH:%s" % directory_path], shell = True)
os.putenv("PYTHONPATH", os.pathsep.join([os.getenv("PYTHONPATH", ""), directory_path]))

if len(sys.argv) == 1:
    # sys.exit()
    print("実行したい問題の番号（0~99）を入力してください。")
    sys.argv.append(input())
file_num = sys.argv[1]
chapter_num = int(file_num[0]) + 1
rel_path = "./chapter%d/code/nlp100_%s.py" % (chapter_num, file_num)
execute_file_path = get_rel_path_from_working_directory(__file__, rel_path)
subprocess.run(["python", execute_file_path, *sys.argv[2:]])
