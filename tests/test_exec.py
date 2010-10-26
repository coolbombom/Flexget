from __future__ import with_statement
from tests import FlexGetBase
import os
import os.path
from tests.util import maketemp


class TestExec(FlexGetBase):

    __yaml__ = """
        presets:
          global:
            set:
              temp_dir: autogenerated in setup()
        feeds:
          replace_from_entry:
            mock:
              - {title: 'replace'}
              - {title: 'replace with spaces'}
            exec: python tests/exec.py %(temp_dir)s %(title)s
            accept_all: yes
          test_adv_format:
            mock:
              - {title: entry1, location: '/path/with spaces/thefile'}
            exec:
              on_download:
                for_entries: python tests/exec.py %(temp_dir)s %(title)s %(location)s '/the/final destinaton/'
    """

    def __init__(self):
        self.test_home = None
        FlexGetBase.__init__(self)

    def setup(self):
        FlexGetBase.setup(self)
        # generate config
        self.test_home = maketemp()
        self.manager.config['presets']['global']['set']['temp_dir'] = self.test_home

    def teardown(self):
        import shutil
        shutil.rmtree(self.test_home)
        FlexGetBase.teardown(self)

    def test_replace_from_entry(self):
        self.execute_feed('replace_from_entry')
        assert len(self.feed.accepted) == 2, "not all entries were accepted"
        for entry in self.feed.accepted:
            assert os.path.exists(os.path.join(self.test_home, entry['title'])), "exec.py did not create a file for %s" % entry['title']

    def test_adv_format(self):
        self.execute_feed('test_adv_format')
        for entry in self.feed.accepted:
            with open(os.path.join(self.test_home, entry['title']), 'r') as infile:
                line = infile.readline().rstrip('\n')
                assert line == '/path/with spaces/thefile', '%s != /path/with spaces/thefile' % line
                line = infile.readline().rstrip('\n')
                assert line == '/the/final-destinaton/', '%s != /the/final destinaton/' % line