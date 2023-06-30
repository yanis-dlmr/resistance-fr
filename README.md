# <img src="assets/images/useful_moderator.png" alt="icon" width="4%"/> Resistance FR - Discord Bot

[![Linux](https://svgshare.com/i/Zhy.svg)](https://docs.microsoft.com/en-us/windows/wsl/tutorials/gui-apps)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
[![GitHub license](https://img.shields.io/github/license/yanis-dlmr/resistance-fr)](https://github.com/yanis-dlmr/resistance-fr/blob/master/LICENSE)
[![GitHub commits](https://badgen.net/github/commits/yanis-dlmr/resistance-fr)](https://GitHub.com/yanis-dlmr/resistance-fr/commit/)
[![GitHub latest commit](https://badgen.net/github/last-commit/yanis-dlmr/resistance-fr)](https://gitHub.com/yanis-dlmr/resistance-fr/commit/)
[![Maintenance](https://img.shields.io/badge/maintained%3F-yes-green.svg)](https://GitHub.com/yanis-dlmr/resistance-fr/graphs/commit-activity)

[![GitHub version](https://badge.fury.io/gh/yanis-dlmr%2Fresistance-fr.svg)](https://github.com/yanis-dlmr/resistance-fr)
[![Author](https://img.shields.io/badge/author-@ThomasByr-blue)](https://github.com/ThomasByr)
[![Author](https://img.shields.io/badge/author-@yanis-dlmr-blue)](https://github.com/yanis-dlmr)

1. [✏️ In short](#️-in-short)
2. [👩‍🏫 Usage \& Setup](#-usage--setup)
3. [💁 Get Help](#-get-help)
4. [🔰 Support](#-support)
5. [🧪 Testing](#-testing)
6. [🧑‍🏫 Contributing](#-contributing)
7. [⚖️ License](#️-license)
8. [⚖️ License](#️-license-1)
9. [🖼️ Icons](#️-icons)
10. [🔄 Changelog](#-changelog)
11. [🐛 Bugs and TODO](#-bugs-and-todo)

## ✏️ In short

## 👩‍🏫 Usage & Setup

> <picture>
>   <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/light-theme/info.svg">
>   <img alt="Info" src="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/dark-theme/info.svg">
> </picture><br>
>
> Please note we do not officially support Windows or MacOS, but we do provide some instructions for those who want to use it on these platforms.

You do not explicitly need a conda environment for the bot to run. But it is always recommended nontheless, especially because the next LTS of Ubuntu won't let users pip-install anything without a virtual environment. At the time of writing, this bot requires `python >= 3.11` to run.

```bash
# Clone the repository
git clone https://github.com/yanis-dlmr/resistance-fr.git
cd resistance-fr
```

You can create and activate a conda environment with the following commands :

```bash
# Creates environment and install dependencies
conda env create -f environment.yml -y
conda activate dsc
```

Finally, run the bot in the background with `bash run.bash` or type the following :

```bash
# Runs the bot (lets you Ctrl+C to stop it)
python resistance-fr.py
```

## 💁 Get Help

Inside the Discord app, you can type

```txt
/<GroupName> help
```

to get help about a specific group of commands. For example, you can type `/utils help` to get help about the `utils` group of commands.

You can try to ping the bot in your guild to start 👋 :

```txt
/utils ping
```

## 🔰 Support

## 🧪 Testing

## 🧑‍🏫 Contributing

If you ever want to contribute, either request the contributor status, or, more manually, fork the repo and make a full request !. On a more generic note, please do respect the [Python Coding Conventions](https://www.python.org/dev/peps/pep-0008/) and wait for your PR to be reviewed. Make sure you respect and read the [Contributing Guidelines](.github/CONTRIBUTING.md), make pull requests and be kind.

> The standard procedure is :
>
> ```txt
> fork -> git branch -> push -> pull request
> ```
>
> Note that we won't accept any PR :
>
> - that does not follow our Contributing Guidelines
> - that is not sufficiently commented or isn't well formated
> - without any proper test suite
> - with a failing or incomplete test suite

Happy coding ! 🙂

## ⚖️ License

## ⚖️ License

This project is licensed under the AGPL-3.0 new or revised license. Please read the [LICENSE](LICENSE.md) file. Additionally :

- Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

- Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

- Neither the name of the Useful Moderator authors nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

```LICENSE
Useful Moderator - Discord Bot
Copyright (C) 2023 Thomas BOUYER

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
```

## 🖼️ Icons

Icons (except [the logo(s)](assets/images/resistance-fr.png)) are made by [Freepik](https://www.flaticon.com/authors/freepik) and [pixelmeetup](https://www.flaticon.com/authors/pixelmeetup) from [www.flaticon.com](https://www.flaticon.com/).

Unless otherwise stated, all icons and logos are made by the authors.
Copyright (C) 2023 Thomas BOUYER, Yanis DELAMARE, all rights reserved.

Tools used :

- [Microsoft Designer](https://designer.microsoft.com/)
- [Clip Studio Paint](https://www.clipstudio.net/en)
- [Canva](https://www.canva.com/)

## 🔄 Changelog

Please read the [changelog](changelog.md) file for the full history !

<details>
    <summary> (click here to expand) </summary>

</details>

## 🐛 Bugs and TODO

**TODO** (first implementation version)

- [x] MongoDB integration
- [ ] polls, auto responses and reactions, ...
- [ ] ...

**Known Bugs** (latest fix)
