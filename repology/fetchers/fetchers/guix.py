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
import time
from string import ascii_uppercase

import lxml.html

from repology.fetchers import ScratchDirFetcher
from repology.fetchers.http import do_http


class GuixFetcher(ScratchDirFetcher):
    def __init__(self, url, fetch_timeout=5, fetch_delay=0):
        self.url = url
        self.fetch_timeout = fetch_timeout
        self.fetch_delay = fetch_delay

    def do_fetch(self, statedir, logger):
        for letter in ['0-9'] + [l for l in ascii_uppercase]:
            page = 1
            numpages = 1
            while True:
                logger.Log('fetching {} page {}'.format(letter, page))

                pageurl = '{}/{}/page/{}/'.format(self.url, letter, page)

                # fetch HTML
                response = do_http(pageurl, timeout=self.fetch_timeout)
                response.encoding = 'utf-8'  # is not detected properly
                text = response.text

                # get number of pages, if there are more than 1 of them
                if numpages == 1:
                    for pagebutton in lxml.html.document_fromstring(text).xpath('.//nav[@class="page-selector"]/a'):
                        numpages = max(numpages, int(pagebutton.text))

                # save HTML
                with open(os.path.join(statedir, '{}-{}.html'.format(letter, page)), 'w', encoding='utf-8') as pagefile:
                    pagefile.write(text)

                # end if that was last (or only) page
                if page >= numpages:
                    break

                # proceed with the next page
                page += 1

                if self.fetch_delay:
                    time.sleep(self.fetch_delay)
