import os.path

rel_path = '../data/hightemp.txt'
# file_abs_path = os.path.dirname(os.path.abspath(__file__))
# data_abs_path = os.path.normpath(os.path.join(file_abs_path, rel_path))
file_rel_path = os.path.dirname(__file__)
data_rel_path = os.path.normpath(os.path.join(file_rel_path, rel_path))


f = open(data_rel_path)
count = 0
for l in f:
    count += 1
print(count)
f.close()

f = open(data_rel_path)
for i, l in enumerate(f, 1):
    pass
print(i)
f.close()

f = open(data_rel_path)
print(sum(1 for line in f))
f.close()

# Unix command
# wc -l ./chapter2/data//hightemp.txt
