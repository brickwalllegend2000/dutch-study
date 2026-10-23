import csv
import io
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from library import parse_tables, consolidate, validate_rows, FIELDS, to_markdown

class LibraryTests(unittest.TestCase):
    def test_markdown_escaped_pipe_and_accents(self):
        tables = parse_tables('| Dutch | English |\n| --- | --- |\n| één | one \\| single |\n')
        self.assertEqual(tables[0][1], ['één', 'one | single'])

    def test_html_table_preserves_breaks(self):
        tables = parse_tables('<table><tr><td>Verb</td><td>Example</td></tr><tr><td>gaan</td><td>Ik ben gegaan.<br/>Naar België.</td></tr></table>')
        self.assertEqual(tables[0][1], ['gaan', 'Ik ben gegaan. Naar België.'])

    def test_duplicate_terms_keep_provenance_and_variants(self):
        rows = consolidate([{'dutch': 'vergeten', 'auxiliary': 'hebben', 'source_id': 'a', 'locator': 'row 1'}, {'dutch': 'vergeten', 'auxiliary': 'hebben / zijn', 'source_id': 'b', 'locator': 'row 2'}])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['source_ids'], 'a;b')
        self.assertIn('hebben / zijn', rows[0]['auxiliary'])
        self.assertEqual(rows[0]['review_status'], 'needs-review')

    def test_ids_stable_when_input_order_changes(self):
        occurrences = [{'dutch': 'eten', 'source_id': 'a'}, {'dutch': 'één', 'source_id': 'b'}]
        self.assertEqual({r['dutch']:r['id'] for r in consolidate(occurrences)}, {r['dutch']:r['id'] for r in consolidate(occurrences[::-1])})

    def test_csv_roundtrip_quotes_and_newlines(self):
        row = consolidate([{'dutch':'zeggen', 'examples':'Hij zegt: "ja",\nzij ook.', 'source_id':'a'}])[0]
        buf=io.StringIO(); writer=csv.DictWriter(buf, fieldnames=FIELDS); writer.writeheader(); writer.writerow(row); buf.seek(0)
        self.assertEqual(list(csv.DictReader(buf))[0], row)

    def test_validation_rejects_duplicates_and_missing_sources(self):
        row = consolidate([{'dutch':'eten', 'source_id':'a'}])[0]
        errors=validate_rows([row,row], {'b'})
        self.assertTrue(any('duplicate' in x for x in errors))
        self.assertTrue(any('unknown source' in x for x in errors))

    def test_conversion_preserves_links_and_tables(self):
        text='<mention url="https://app.notion.com/p/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa">Home</mention>\n<table><tr><td>A</td><td>B</td></tr><tr><td>één</td><td>one</td></tr></table>'
        md=to_markdown(text, {'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': ('README.md','Home')}, 'grammar/topic.md')
        self.assertIn('[Home](../README.md)',md)
        self.assertIn('| één | one |',md)

if __name__=='__main__': unittest.main()

class CorpusFixture(unittest.TestCase):
    def setUp(self):
        import tempfile, json
        from library import build
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        (self.root/'sources').mkdir()
        (self.root/'sources/pages').mkdir()
        (self.root/'sources/pages/a.md').write_text('# Evidence\n')
        (self.root/'sources/raw.txt').write_text('original')
        (self.root/'README.md').write_text('# Home\n')
        self.row=consolidate([{'dutch':'eten','source_id':'a','occurrence_id':'OCC-1'}])[0]
        with (self.root/'vocabulary.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerow(self.row)
        self.manifest={'pages':[{'id':'a','raw_path':'sources/raw.txt','snapshot_path':'sources/pages/a.md'}],'attachments':[]}
        self.write_manifest()
        self.occurrence={'occurrence_id':'OCC-1','source_id':'a','record_id':self.row['id']}
        (self.root/'sources/vocabulary-occurrences.json').write_text(json.dumps([self.occurrence]))
        build(self.root)
    def write_manifest(self):
        import json
        (self.root/'sources/manifest.json').write_text(json.dumps(self.manifest))

class CorpusValidationTests(CorpusFixture):
    def test_changed_csv_requires_regeneration(self):
        from library import validate
        path=self.root/'vocabulary.csv'
        path.write_text(path.read_text().replace('eten','drinken'))
        self.assertTrue(any('stale generated' in e for e in validate(self.root)))
    def test_provenance_cannot_point_to_another_record(self):
        import json
        from library import validate
        self.occurrence['record_id']='VOC-000000000000'
        (self.root/'sources/vocabulary-occurrences.json').write_text(json.dumps([self.occurrence]))
        self.assertTrue(any('record mismatch' in e for e in validate(self.root)))
    def test_archived_attachment_must_exist(self):
        from library import validate
        self.manifest['attachments']=[{'name':'photo.jpg','status':'archived','local_path':'sources/originals/photo.jpg','sha256':'0'*64}]
        self.write_manifest()
        self.assertTrue(any('archived attachment missing' in e for e in validate(self.root)))
    def test_broken_relative_link_fails(self):
        from library import validate
        (self.root/'README.md').write_text('[Missing](missing.md)')
        self.assertTrue(any('broken link' in e for e in validate(self.root)))

class CompleteProvenanceTests(CorpusFixture):
    def test_every_source_occurrence_requires_a_reverse_record_link(self):
        from library import validate
        self.row['occurrence_ids']=''
        with (self.root/'vocabulary.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerow(self.row)
        self.assertTrue(any('unlinked occurrence' in e for e in validate(self.root)))

    def test_multiline_vocabulary_renders_as_single_table_row(self):
        from library import rendered
        self.row['english']='to eat,\nconsume'
        with (self.root/'vocabulary.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerow(self.row)
        self.assertIn('to eat,<br>consume', rendered(self.root)['wiki/vocabulary/VOCABULARY.md'])
