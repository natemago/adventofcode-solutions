#!/usr/bin/python3

import hashlib
from threading import Thread, Lock

key = 'ckczppom'
# 5 - 117946
lock = Lock()
block = 117
number_of_threads = 4
found = False
block_size = 10000


def calc_block():
  global block
  global found
  while not found:
    with lock:
      start = block * block_size
      end = (block+1) * block_size
      block = block + 1
    i = start
    while i < end:
       m = '%s%d' % (key,i)
       md5 = hashlib.md5(m.encode('utf-8')).hexdigest()
       if md5[0:6] == '000000':
         print(i)
         found = True
         break
       i = i + 1
    if not found:
      print('None in %d-%d' % (start, end))


threads = []
for i in range(0, number_of_threads):
  threads.append(Thread(target=calc_block))


for thread in threads:
  thread.start()

  