import subprocess
from time import sleep
import atexit

def stanford_corenlp_with_server(**kwargs):
    """
    """
    cmd = ['java', '-mx4g', 'edu.stanford.nlp.pipeline.StanfordCoreNLPServer', '-annotators "tokenize,ssplit,pos,lemma,parse,sentiment"', '-port', '9000', '-timeout', '30000']
    env = {'CLASSPATH': '/usr/local/lib/stanford-corenlp-full-2018-10-05/*'}
    process = subprocess.Popen(cmd, env=env)
    sleep(3) # サーバー起動前に処理が実行されるのを防ぐ
    atexit.register(lambda proc: proc.kill(), process)
