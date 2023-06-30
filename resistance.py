#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#! Resistance-Fr
#!
#! Copyright (c) 2022, ThomasByr & yanis-dlmr
#! AGPL-3.0-or-later (https://www.gnu.org/licenses/agpl-3.0.en.html)
#! All rights reserved.
#!
#! Redistribution and use in source and binary forms, with or without
#! modification, are permitted provided that the following conditions are met:
#!
#! * Redistributions of source code must retain the above copyright notice,
#!   this list of conditions and the following disclaimer.
#!
#! * Redistributions in binary form must reproduce the above copyright notice,
#!   this list of conditions and the following disclaimer in the documentation
#!   and/or other materials provided with the distribution.
#!
#! * Neither the name of this software's authors nor the names of its
#!   contributors may be used to endorse or promote products derived from
#!   this software without specific prior written permission.
#!
#! This program is free software: you can redistribute it and/or modify
#! it under the terms of the GNU Affero General Public License as published by
#! the Free Software Foundation, either version 3 of the License, or
#! (at your option) any later version.
#!
#! This program is distributed in the hope that it will be useful,
#! but WITHOUT ANY WARRANTY; without even the implied warranty of
#! MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#! GNU Affero General Public License for more details.
#!
#! You should have received a copy of the GNU Affero General Public License
#! along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys

if sys.version_info < (3, 11):
  raise RuntimeError('This program requires Python 3.11 or later.')

from src import UsefulClient

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_PREFIX = os.getenv('BOT_PREFIX', '!')
BOT_INVITE = os.getenv('BOT_INVITE')

if __name__ == '__main__':

  client = UsefulClient(BOT_PREFIX, BOT_INVITE, help_command=None)
  client.run(BOT_TOKEN)
