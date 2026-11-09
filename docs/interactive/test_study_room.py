"""Static smoke tests for the offline-only OmniMaster study-room HTML."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit


PAGE = Path(__file__).with_name("index.html")
ROOT = PAGE.parents[2]


class DocumentInspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.scripts = []
        self.script_sources = []
        self.meta_csp = []
        self._inside_script = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"])
        if tag == "a":
            self.links.append(attributes.get("href", ""))
        if tag == "script":
            self.script_sources.append(attributes.get("src"))
            self._inside_script = True
        if tag == "meta" and attributes.get("http-equiv") == "Content-Security-Policy":
            self.meta_csp.append(attributes.get("content", ""))

    def handle_endtag(self, tag):
        if tag == "script":
            self._inside_script = False

    def handle_data(self, data):
        if self._inside_script:
            self.scripts.append(data)


class StudyRoomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.parser = DocumentInspector()
        cls.parser.feed(cls.html)
        cls.script = "\n".join(cls.parser.scripts)

    def test_has_accessible_structure(self):
        for expected in ['lang="en"', 'name="viewport"', '<main id="main">',
                         'aria-live="polite"', 'aria-label="Page sections"',
                         'id="progress-track"', 'type="button"']:
            self.assertIn(expected, self.html)

    def test_no_external_script_src(self):
        self.assertEqual(self.parser.script_sources, [None])

    def test_content_security_policy_blocks_network(self):
        self.assertTrue(self.parser.meta_csp)
        self.assertIn("connect-src 'none'", self.parser.meta_csp[0])
        self.assertIn("default-src 'none'", self.parser.meta_csp[0])

    def test_no_network_or_telemetry_calls(self):
        for prohibited in ("fetch(", "XMLHttpRequest", "sendBeacon(", "WebSocket(", "import(",
                           "analytics.", "gtag(", "http://", "https://"):
            self.assertNotIn(prohibited, self.script)

    def test_unique_element_ids(self):
        self.assertEqual(len(self.parser.ids), len(set(self.parser.ids)))

    def test_local_links_exist(self):
        for uri in self.parser.links:
            parsed = urlsplit(uri)
            if not parsed.path or parsed.path.startswith("#"):
                continue
            if uri == "/downloads/omnimaster-fullstack.pdf":
                # The hosted Worker generates a PDF; no static file exists offline.
                continue
            if parsed.scheme or parsed.netloc:
                self.assertEqual(
                    uri,
                    "https://github.com/CayelaemJ/CayelaemJ/blob/main/docs/interactive/index.html",
                    "Only the explicitly labelled HTML-source link may leave this offline page",
                )
                continue
            path = (PAGE.parent / parsed.path).resolve()
            self.assertTrue(path.is_relative_to(ROOT), uri)
            self.assertTrue(path.exists(), uri)

    def test_seven_lessons_are_linked(self):
        for n in range(1, 8):
            self.assertIn(f"../academy/0{n}_", self.html)

    def test_exactly_six_scenarios_have_explanations(self):
        questions = self.script.split("const questions = [", 1)[1].split("];", 1)[0]
        self.assertEqual(len(re.findall(r"\{q:", questions)), 6)
        self.assertEqual(len(re.findall(r",why:", questions)), 6)

    def test_exactly_thirty_mission_titles(self):
        titles = self.script.split("const titles=[", 1)[1].split("];", 1)[0]
        self.assertEqual(len(re.findall(r'"[^"]+"', titles)), 30)
        self.assertIn('forEach(function(title,i)', self.script)

    def test_local_progress_can_be_reset(self):
        self.assertIn("omnimaster.studyroom.days.v1", self.script)
        self.assertIn("localStorage", self.script)
        self.assertIn('window.confirm("Clear the 30-day checklist', self.script)
        self.assertIn("completed=[]", self.script)

    def test_untrusted_values_are_displayed_as_text(self):
        self.assertIn("text.textContent=", self.script)
        self.assertIn("question.textContent=", self.script)
        self.assertIn("feedback.textContent=", self.script)
        self.assertNotIn("innerHTML", self.script)


if __name__ == "__main__":
    unittest.main()
