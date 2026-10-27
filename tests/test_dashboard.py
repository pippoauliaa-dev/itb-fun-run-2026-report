from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DashboardSmokeTests(unittest.TestCase):
    def test_data_file_has_event_identity_and_placeholder_values(self):
        data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
        self.assertEqual(data["event"], "ITB Fun Run 2026")
        self.assertEqual(data["brand"], "RFID Total Solution")
        self.assertTrue(data["isIllustrative"])
        self.assertTrue(all(kpi["value"] is None or data["isIllustrative"] for kpi in data["kpis"]))

    def test_report_focuses_on_awareness_and_engagement_not_leads(self):
        data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertEqual([kpi["id"] for kpi in data["kpis"]], ["reach", "engagement", "participation"])
        self.assertNotIn("Leads terkumpul", json.dumps(data, ensure_ascii=False))
        self.assertNotIn("Rekap leads", json.dumps(data, ensure_ascii=False))
        self.assertNotIn("leads", html.lower())

    def test_account_comparison_reports_neutral_pre_and_post_event_insights(self):
        data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        comparison = data["accountComparison"]
        self.assertEqual(comparison["eventDate"], "2026-10-18")
        self.assertEqual(comparison["pre"]["views"], 34939)
        self.assertEqual(comparison["post"]["views"], 25922)
        self.assertEqual(round(comparison["pre"]["views"] / comparison["pre"]["days"]), 1941)
        self.assertEqual(round(comparison["post"]["views"] / comparison["post"]["days"]), 2880)
        self.assertEqual(comparison["pre"]["interactionsByContent"], 28)
        self.assertEqual(comparison["post"]["interactionsByContent"], 45)
        self.assertIn('id="account-comparison"', html)
        self.assertIn("periode pasca-acara lebih singkat", html.lower())

    def test_evaluation_is_split_into_people_and_event(self):
        data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertEqual(set(data["evaluation"].keys()), {"people", "event"})
        self.assertTrue(any("rfid" in item["label"].lower() for item in data["evaluation"]["people"]))
        self.assertTrue(any("backup" in item["label"].lower() for item in data["evaluation"]["people"]))
        self.assertTrue(any("qr" in item["label"].lower() for item in data["evaluation"]["event"]))
        self.assertTrue(any("subtitle" in item["label"].lower() for item in data["evaluation"]["event"]))
        self.assertTrue(all(item["status"] != "Belum dievaluasi" for group in data["evaluation"].values() for item in group))
        self.assertIn('id="people-evaluation"', html)
        self.assertIn('id="event-evaluation"', html)
        self.assertLess(html.index('aria-label="Evaluasi SDM dan acara"'), html.index('id="awareness-title"'))
        self.assertNotIn("Yang terlihat berhasil", html)
        self.assertNotIn("Peluang berikutnya", html)

    def test_page_exposes_filters_charts_table_and_placeholder_notice(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for expected in (
            'id="period-filter"',
            'id="channel-filter"',
            'id="awareness-chart"',
            'id="engagement-chart"',
            'id="data-table"',
            "data.json",
            "Data ilustrasi untuk contoh tampilan.",
            "[...new Set(data.periods)]",
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
