#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import subprocess

token='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'

subprocess.check_call(['git', 'add', '--all'], cwd='/root/GitHub/energynewz.github.io')
subprocess.check_call(['git', 'commit', '-m', 'python push'], cwd='/root/GitHub/energynewz.github.io')
subprocess.check_call(['git', 'push', 'https://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@github.com/DmitryBrown/energynewz.github.io', 'main'], cwd='/root/GitHub/energynewz.github.io')

# git push --set-upstream https://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@github.com/DmitryBrown/energynewz.github.io main
# git push https://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@github.com/DmitryBrown/energynewz.github.io main

