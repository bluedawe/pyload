# -*- coding: utf-8 -*-

import re

from module.plugins.internal.Hoster import Hoster


class VeehdCom(Hoster):
    __name__    = "VeehdCom"
    __type__    = "hoster"
    __version__ = "0.26"
    __status__  = "testing"

    __pattern__ = r'http://veehd\.com/video/\d+_\S+'
    __config__  = [("activated", "bool", "Activated", True),
                   ("filename_spaces", "bool", "Allow spaces in filename", False),
                   ("replacement_char", "str", "Filename replacement character", "_")]

    __description__ = """Veehd.com hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("cat", "cat@pyload")]


    def setup(self):
        self.multiDL = True
        self.req.canContinue = True


    def process(self, pyfile):
        self.download_html()
        if not self.file_exists():
            self.offline()

        pyfile.name = self.get_file_name()
        self.download(self.get_file_url())


    def download_html(self):
        url = self.pyfile.url
        self.log_debug("Requesting page: %s" % url)
        self.html = self.load(url)


    def file_exists(self):
        if not self.html:
            self.download_html()

        if '<title>Veehd</title>' in self.html:
            return False
        return True


    def get_file_name(self):
        if not self.html:
            self.download_html()

        m = re.search(r'<title.*?>([^<]+) on Veehd</title>', self.html)
        if m is None:
            self.error(_("Video title not found"))

        name = m.group(1)

        #: Replace unwanted characters in filename
        if self.get_config('filename_spaces'):
            pattern = '[^\w ]+'
        else:
            pattern = '[^\w.]+'

        return re.sub(pattern, self.get_config('replacement_char'), name) + '.avi'


    def get_file_url(self):
        """
        Returns the absolute downloadable filepath
        """
        if not self.html:
            self.download_html()

        m = re.search(r'<embed type="video/divx" src="(http://([^/]*\.)?veehd\.com/dl/.+?)"',
                          self.html)
        if m is None:
            self.error(_("Embedded video url not found"))

        return m.group(1)
