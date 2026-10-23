import csv
import io
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from library import parse_tables, consolidate, validate_rows, FIELDS, DATA_CSV, GRAMMAR_DIR, VIEWS, to_markdown

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
        (self.root/Path(DATA_CSV).parent).mkdir(parents=True,exist_ok=True)
        self.row=consolidate([{'dutch':'eten','source_id':'a','occurrence_id':'OCC-1'}])[0]
        self.write_vocabulary(self.row)
        self.manifest={'pages':[{'id':'a','raw_path':'sources/raw.txt','snapshot_path':'sources/pages/a.md'}],'attachments':[]}
        self.write_manifest()
        self.occurrence={'occurrence_id':'OCC-1','source_id':'a','record_id':self.row['id']}
        (self.root/'sources/vocabulary-occurrences.json').write_text(json.dumps([self.occurrence]))
        build(self.root)
    def write_vocabulary(self, *rows):
        path=self.root/DATA_CSV
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader()
            for row in rows: w.writerow(row)
    def write_manifest(self):
        import json
        (self.root/'sources/manifest.json').write_text(json.dumps(self.manifest))

class CorpusValidationTests(CorpusFixture):
    def test_data_layer_fixture_validates_clean(self):
        from library import validate
        grammar=self.root/GRAMMAR_DIR; grammar.mkdir(parents=True)
        (grammar/'topic.md').write_text(
            '---\nreview_status: needs-review\n---\n# Topic\n\n[Home](../../README.md)\n',
            encoding='utf-8',
        )
        course=self.root/'course'; course.mkdir(exist_ok=True)
        links=[f'[Grammar]({GRAMMAR_DIR}/topic.md)']
        for n in range(1,9):
            (course/f'chapter-{n:02}.md').write_text(f'# Chapter {n}\n\n[Home](../README.md)\n',encoding='utf-8')
            links.append(f'[Chapter {n}](course/chapter-{n:02}.md)')
        (self.root/'README.md').write_text('\n'.join(links)+'\n',encoding='utf-8')
        # Generated PERFECTUM-STUDY-LIST links this source page; stub it for link checks.
        (self.root/'sources/pages/401f89e5e0fc80f29352c76d2b8204b7.md').write_text('# Study list source\n',encoding='utf-8')
        self.assertEqual(validate(self.root), [])
        self.assertTrue((self.root/DATA_CSV).is_file())
        self.assertTrue((self.root/VIEWS/'VOCABULARY.md').is_file())
        vocab=(self.root/VIEWS/'VOCABULARY.md').read_text(encoding='utf-8')
        self.assertIn(f'../../{DATA_CSV}', vocab)
        word=(self.root/VIEWS/'words'/f"{self.row['id']}.md").read_text(encoding='utf-8')
        self.assertIn(f'../../../{DATA_CSV}', word)

    def test_changed_csv_requires_regeneration(self):
        from library import validate
        path=self.root/DATA_CSV
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
    def test_unlinked_course_page_fails(self):
        from library import validate
        (self.root/'course').mkdir()
        (self.root/'course/chapter-09.md').write_text('# Chapter 9\n\n[Home](../README.md)')
        self.assertTrue(any('course/chapter-09.md: orphan page' in e for e in validate(self.root)))
        (self.root/'README.md').write_text('[Chapter 9](course/chapter-09.md)')
        self.assertFalse(any('orphan page' in e for e in validate(self.root)))
    def test_unlinked_cheat_sheet_fails(self):
        from library import validate
        (self.root/'wiki/cheat-sheets').mkdir(parents=True)
        (self.root/'wiki/cheat-sheets/perfectum.md').write_text('# Perfectum')
        self.assertTrue(any('wiki/cheat-sheets/perfectum.md: orphan page' in e for e in validate(self.root)))
    def test_grammar_missing_frontmatter_fails(self):
        from library import validate
        grammar=self.root/GRAMMAR_DIR; grammar.mkdir(parents=True)
        (grammar/'topic.md').write_text('# Topic without frontmatter\n',encoding='utf-8')
        (self.root/'README.md').write_text(f'[Grammar]({GRAMMAR_DIR}/topic.md)\n',encoding='utf-8')
        self.assertTrue(any('missing YAML frontmatter' in e for e in validate(self.root)))

class CompleteProvenanceTests(CorpusFixture):
    def test_every_source_occurrence_requires_a_reverse_record_link(self):
        from library import validate
        self.row['occurrence_ids']=''
        self.write_vocabulary(self.row)
        self.assertTrue(any('unlinked occurrence' in e for e in validate(self.root)))

    def test_multiline_vocabulary_renders_as_single_table_row(self):
        from library import rendered
        self.row['english']='to eat,\nconsume'
        self.write_vocabulary(self.row)
        self.assertIn('to eat,<br>consume', rendered(self.root)[f'{VIEWS}/VOCABULARY.md'])


class TextSearchTests(unittest.TestCase):
    def test_search_text_finds_lines_case_insensitively(self):
        import tempfile
        from library import search_text
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'course').mkdir()
            (root/'course'/'chapter-01.md').write_text('# Hoofdstuk\nIk ben VERGETEN.\nNiets\n',encoding='utf-8')
            (root/'course'/'notes.txt').write_text('vergeten\n',encoding='utf-8')
            hits=list(search_text('vergeten',root,['course','missing']))
        self.assertEqual(hits,[('course/chapter-01.md',2,'Ik ben VERGETEN.')])

    def test_default_text_dirs_include_data_grammar(self):
        import tempfile
        from library import search_text, TEXT_DIRS
        self.assertIn(GRAMMAR_DIR, TEXT_DIRS)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            grammar=root/GRAMMAR_DIR; grammar.mkdir(parents=True)
            (grammar/'topic.md').write_text('# Aan het\ncontinuous aspect\n',encoding='utf-8')
            hits=list(search_text('aan het', root))
        self.assertEqual(hits,[(f'{GRAMMAR_DIR}/topic.md',1,'# Aan het')])

    def test_search_cli_accepts_flags_before_query(self):
        import io
        import library
        buf=io.StringIO()
        old_out,old_argv=sys.stdout,sys.argv
        try:
            sys.stdout=buf
            sys.argv=['library.py','search','--all','vergeten']
            self.assertEqual(library.main(),0)
        finally:
            sys.stdout,sys.argv=old_out,old_argv
        self.assertIn('VOC-', buf.getvalue())


class ValidationGapTests(CorpusFixture):
    def test_extra_generated_word_note_is_rejected(self):
        from library import validate
        extra=self.root/VIEWS/'words'/'VOC-deadbeefdead.md'
        extra.write_text('# orphan generated note\n',encoding='utf-8')
        self.assertTrue(any('unexpected generated file' in e for e in validate(self.root)))

    def test_csv_row_with_extra_cell_is_rejected(self):
        from library import validate
        path=self.root/DATA_CSV
        path.write_text(path.read_text(encoding='utf-8').rstrip('\n')+',extra\n',encoding='utf-8')
        self.assertTrue(any('expected %d cells' % len(FIELDS) in e for e in validate(self.root)))

    def test_archived_pdf_must_look_like_pdf(self):
        from library import validate
        originals=self.root/'sources/originals'; originals.mkdir(parents=True)
        fake=originals/'agenda.pdf'; fake.write_text('not a pdf alias\n',encoding='utf-8')
        digest=__import__('hashlib').sha256(fake.read_bytes()).hexdigest()
        self.manifest['attachments']=[{'name':'agenda.pdf','status':'archived','local_path':'sources/originals/agenda.pdf','sha256':digest}]
        self.write_manifest()
        self.assertTrue(any('unexpected format' in e for e in validate(self.root)))

    def test_verb_listing_includes_auxiliary_and_participle(self):
        from library import listing
        row={**self.row,'english':'to eat','auxiliary':'hebben','participle':'gegeten','review_status':'needs-review'}
        table=listing([row],('dutch','english','auxiliary','participle','review_status'))
        self.assertIn('| Auxiliary | Participle |',table)
        self.assertIn('hebben',table)
        self.assertIn('gegeten',table)


class PublishHelperTests(unittest.TestCase):
    def test_credential_helper_unset_all_is_idempotent(self):
        import tempfile, subprocess
        from publish_github import command
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            subprocess.run(['git','init'],cwd=root,check=True,capture_output=True)
            # Simulate two publish runs: unset-all then add, twice.
            for _ in range(2):
                subprocess.run(['git','config','--local','--unset-all','credential.https://github.com.helper'],cwd=root,capture_output=True)
                r=subprocess.run(['git','config','--local','--add','credential.https://github.com.helper','!gh auth git-credential'],cwd=root,capture_output=True)
                self.assertEqual(r.returncode,0)
