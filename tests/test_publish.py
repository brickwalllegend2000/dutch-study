import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from publish_github import check_destination

class PublishingTests(unittest.TestCase):
    def test_public_repository_is_rejected_before_upload(self):
        with self.assertRaisesRegex(ValueError,'private'):
            check_destination({'isPrivate':False,'isEmpty':True},False)
    def test_nonempty_unrelated_repository_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'nonempty'):
            check_destination({'isPrivate':True,'isEmpty':False},False)
    def test_existing_matching_library_can_be_resumed(self):
        self.assertIsNone(check_destination({'isPrivate':True,'isEmpty':False},True))

class RemoteDestinationTests(unittest.TestCase):
    def test_separate_unchecked_push_url_is_rejected(self):
        from publish_github import check_remote_urls
        with self.assertRaisesRegex(ValueError,'push'):
            check_remote_urls('brickwalllegend2000/dutch-study','https://github.com/brickwalllegend2000/dutch-study.git',['https://github.com/elsewhere/public-notes.git'])
    def test_multiple_push_destinations_are_all_checked(self):
        from publish_github import check_remote_urls
        with self.assertRaisesRegex(ValueError,'push'):
            check_remote_urls('brickwalllegend2000/dutch-study','https://github.com/brickwalllegend2000/dutch-study.git',['https://github.com/brickwalllegend2000/dutch-study.git','git@github.com:elsewhere/public-notes.git'])
