import sys
import os

def get_rel_path_from_working_directory(wd_ef_rel, ed_sf_rel):
    """
    ワーキングディレクトリ-実行ファイル間の相対パスと、実行ファイルのディレクトリ-ソーフファイル間の相対パスからワーキングディレクトリ-ソースファイル間の相対パスを返す。

    Args:
        wd_ef_rel(str): カレントディレクトリ(working directory)と実行ファイルと(executable file)の相対パス
        ed_sf_rel(str): 実行ファイル(executable file)とimportファイル(source file)との相対パス
    Returns:
        str: working_directoryとimportファイルとの相対パス
    """
    wd_ed_rel = os.path.dirname(wd_ef_rel)
    return os.path.normpath(os.path.join(wd_ed_rel, ed_sf_rel))
