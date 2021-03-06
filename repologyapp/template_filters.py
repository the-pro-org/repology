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

from repologyapp.packageformatter import PackageFormatter

from repology.package import VersionClass


__all__ = ['maintainer_to_links', 'maintainers_to_group_mailto', 'pkg_format', 'css_for_versionclass']


def maintainer_to_links(maintainer):
    links = []

    if '@' in maintainer:
        name, domain = maintainer.split('@', 1)

        if domain == 'cpan':
            links.append('http://search.cpan.org/~' + name)
        elif domain == 'aur':
            links.append('https://aur.archlinux.org/account/' + name)
        elif domain in ('altlinux.org', 'altlinux.ru'):
            links.append('http://sisyphus.ru/en/packager/' + name + '/')
        elif domain == 'github':
            links.append('https://github.com/' + name)
        elif domain == 'freshcode':
            links.append('http://freshcode.club/search?user=' + name)

        if '.' in domain:
            links.append('mailto:' + maintainer)

    return links


def maintainers_to_group_mailto(maintainers, subject=None):
    emails = []

    for maintainer in maintainers:
        if '@' in maintainer and '.' in maintainer.split('@', 1)[1]:
            emails.append(maintainer)

    if not emails:
        return None

    return 'mailto:' + ','.join(sorted(emails)) + ('?subject=' + subject if subject else '')


def pkg_format(value, pkg):
    return PackageFormatter().format(value, pkg)


def css_for_versionclass(value):
    if value == VersionClass.ignored:
        return 'ignored'
    elif value == VersionClass.unique:
        return 'unique'
    elif value == VersionClass.devel:
        return 'devel'
    elif value == VersionClass.newest:
        return 'newest'
    elif value == VersionClass.legacy:
        return 'legacy'
    elif value == VersionClass.outdated:
        return 'outdated'
    elif value == VersionClass.incorrect:
        return 'incorrect'
    elif value == VersionClass.untrusted:
        return 'untrusted'
    elif value == VersionClass.noscheme:
        return 'noscheme'
    elif value == VersionClass.rolling:
        return 'rolling'
