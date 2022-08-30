#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import subprocess

token='##################'

subprocess.check_call(['git', 'add', '--all'], cwd='/root/GitHub/energynewz.github.io')
subprocess.check_call(['git', 'commit', '-m', 'python push'], cwd='/root/GitHub/energynewz.github.io')
subprocess.check_call(['git', 'push', 'https://############@github.com/DmitryBrown/energynewz.github.io', 'main'], cwd='/root/GitHub/energynewz.github.io')

# git push --set-upstream https://#############@github.com/DmitryBrown/energynewz.github.io main
# git push https://#################i@github.com/DmitryBrown/energynewz.github.io main

