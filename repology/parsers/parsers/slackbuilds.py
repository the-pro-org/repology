# Copyright (C) 2016-2017 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

import os

from repology.logger import Logger
from repology.parsers import Parser
from repology.parsers.maintainers import extract_maintainers


class SlackBuildsParser(Parser):
    def iter_parse(self, path, factory):
        for category in os.listdir(path):
            if category.startswith('.'):
                continue

            category_path = os.path.join(path, category)
            if not os.path.isdir(category_path):
                continue

            for package in os.listdir(category_path):
                package_path = os.path.join(category_path, package)
                if not os.path.isdir(package_path):
                    continue

                info_path = os.path.join(category_path, package, package + '.info')
                if not os.path.isfile(info_path):
                    factory.log('{} does not exist, package skipped'.format(info_path), severity=Logger.ERROR)
                    continue

                with open(info_path, encoding='utf-8', errors='ignore') as infofile:
                    variables = {}

                    key = None
                    total_value = []

                    for line in infofile:
                        line = line.strip()
                        if not line:
                            continue

                        value = None
                        if key:  # continued
                            value = line
                        else:  # new variable
                            key, value = line.split('=', 1)
                            value = value.lstrip('"').lstrip()

                        if value.endswith('\\'):  # will continue
                            total_value.append(value.rstrip('\\').rstrip())
                        elif not value or value.endswith('"'):
                            total_value.append(value.rstrip('"').rstrip())
                            variables[key] = ' '.join(total_value)
                            key = None
                            total_value = []

                    pkg = factory.begin()
                    pkg.category = category

                    pkg.name = variables['PRGNAM']
                    pkg.version = variables['VERSION']
                    pkg.homepage = variables['HOMEPAGE']
                    pkg.maintainers = extract_maintainers(variables['EMAIL'])
                    for key in ['DOWNLOAD', 'DOWNLOAD_x86_64']:
                        if variables[key] not in ['', 'UNSUPPORTED', 'UNTESTED']:
                            pkg.downloads.extend(variables[key].split())

                    if pkg.name is not None and pkg.version is not None:
                        yield pkg
                    else:
                        factory.log('{} skipped, likely due to parsing problems'.format(info_path), severity=Logger.ERROR)
