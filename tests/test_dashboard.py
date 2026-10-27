from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DashboardSmokeTests(unittest.TestCase):
    def test_data_file_contains_actual_search_console_period_data(self):
        data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
        self.assertEqual(data["event"], "ITB Fun Run 2026")
        self.assertEqual(data["brand"], "RFID Total Solution")
        self.assertFalse(data["isIllustrative"])
        instagram = data["accountComparison"]
        self.assertEqual(instagram["pre"]["views"], 34939)
        self.assertEqual(instagram["post"]["views"], 25922)
        self.assertEqual(data["searchPerformance"]["pre"]["clicks"], 132)
        self.assertEqual(data["searchPerformance"]["pre"]["impressions"], 13864)
        self.assertEqual(data["searchPerformance"]["post"]["clicks"], 62)
        self.assertEqual(data["searchPerformance"]["post"]["impressions"], 7837)
        self.assertTrue(any("Total Search Console: 194 klik, 21.701 tayangan, CTR 0,89%, posisi rata-rata 5,76" in note for note in data["searchPerformance"]["notes"]))
        self.assertEqual(data["searchPerformance"]["pre"]["days"], 17)
        self.assertEqual(data["searchPerformance"]["post"]["days"], 10)
        self.assertEqual(data["searchPerformance"]["pre"]["topPages"][0]["clicks"], 41)
        self.assertEqual(data["searchPerformance"]["post"]["topPages"][0]["clicks"], 18)

    def test_report_uses_website_search_performance_instead_of_illustrative_social_sections(self):
        data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertEqual(data["searchPerformance"]["source"], "Google Search Console")
        self.assertIn('id="search-performance"', html)
        self.assertIn('id="account-comparison"', html)
        self.assertIn('Perbandingan Instagram sebelum dan sesudah acara', html)
        self.assertNotIn('id="illustration-notice"', html)
        self.assertNotIn('id="period-filter"', html)
        self.assertNotIn('id="kpi-grid"', html)
        self.assertNotIn('id="awareness-chart"', html)
        self.assertNotIn('id="activity-line"', html)
        self.assertNotIn('id="next-grid"', html)

    def test_search_console_report_replaces_illustrative_dashboard_sections(self):
        data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        search = data["searchPerformance"]
        self.assertEqual(search["pre"]["clicks"], 132)
        self.assertEqual(search["pre"]["impressions"], 13864)
        self.assertEqual(search["post"]["clicks"], 62)
        self.assertEqual(search["post"]["impressions"], 7837)
        self.assertEqual(search["pre"]["days"], 17)
        self.assertEqual(search["post"]["days"], 10)
        self.assertIn('id="search-performance"', html)
        self.assertIn('aria-label="Legenda perbandingan periode"', html)
        self.assertIn('Pra-acara', html)
        self.assertIn('Pasca-acara', html)
        for table_id in ("search-query-pre-table", "search-query-post-table", "search-page-pre-table", "search-page-post-table"):
            self.assertIn(f'id="{table_id}"', html)
        self.assertNotIn('id="illustration-notice"', html)
        self.assertNotIn('id="period-filter"', html)
        self.assertNotIn('id="kpi-grid"', html)
        self.assertNotIn('id="awareness-chart"', html)
        self.assertIn('id="comparison-chart"', html)
        self.assertNotIn('id="activity-line"', html)
        self.assertNotIn('id="next-grid"', html)
        self.assertFalse(data["isIllustrative"])

    def test_page_exposes_search_report_and_loads_dashboard_data(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for expected in (
            "data.json",
            "renderSearchPerformance",
            "Performa website di Google Search",
            'id="search-query-pre-table"',
            'id="search-query-post-table"',
            'id="search-page-pre-table"',
            'id="search-page-post-table"',
            "$('page-title').textContent = data.event",
        ):
            self.assertIn(expected, html)
        self.assertNotIn("$('page-title').innerHTML", html)

    def test_documentation_explains_github_pages_and_data_replacement(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("GitHub Pages", readme)
        self.assertIn("data.json", readme)


if __name__ == "__main__":
    unittest.main()
