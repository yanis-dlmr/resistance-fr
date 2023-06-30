#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Make the README file <details> section.

  Usage:
    `python3 ./scripts/details.py`

"""

from typing import List


def get_changes() -> List[str]:
  """
  Gets the changes from the changelog.md file.

  ## Output format
  [version and message, first change, second change, ...]
  """
  with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
    changelog = f.readlines()
  changelog = [e.strip() for e in changelog]
  chg: List[str] = []
  for e in reversed(changelog):
    chg.append(e)
    if len(e) > 0 and e[0] == '#':
      break
  return list(reversed(chg))


def update(chg: List[str]) -> None:
  """
  Updates README.md with changelog

  ## Parameters
  ```py
  >>> chg : list[str]
  ```
  changelog extract
  """
  with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.readlines()
  index0: int = None
  index1: int = None
  seen = False
  for i, e in enumerate(readme):
    e.strip()
    if seen:
      if '<details>' in e:
        index0 = i
      elif '</details>' in e:
        index1 = i
    else:
      if ('Changelog' in e or 'changelog' in e) and '##' in e:
        seen = True
  if not seen:
    raise RuntimeError('Error [README make] : no changelog subsection found')
  if index0 is None or index1 is None:
    raise RuntimeError('Error [README make] : bad format, <details> tag not found')

  head = chg[0]
  index_of = head.find('#')
  head = head[index_of::].strip('##')

  details: List[str] = []
  details.append(f'  <summary> {head.strip()} (click here to expand) </summary>')
  details.append('\n')
  for e in chg[1:]:
    details.append(f'{e}\n')
  details.append('\n')

  readme = readme[:index0 + 1] + details + readme[index1:]
  with open('README.md', 'w', encoding='utf-8') as f:
    f.writelines(readme)


if __name__ == '__main__':
  # it just works
  update(get_changes())
  print('README.md updated')
