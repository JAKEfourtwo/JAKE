"""Automated Intelligence Reports for J.A.K.E

Generates daily or weekly summary reports from the knowledge graph.
"""

from core.query import JAKEQuery
from datetime import datetime

class IntelligenceReport:
    def __init__(self):
        self.query = JAKEQuery()
    
    def generate_daily_report(self, focus_areas: list = None):
        if focus_areas is None:
            focus_areas = ["AI infrastructure", "Geopolitics", "Capital markets"]
        
        report = f"# Daily Intelligence Report - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        for area in focus_areas:
            insights = self.query.ask(f"Key developments and risks in {area}")
            report += f"## {area}\n{insights}\n\n"
        
        return report
    
    def generate_weekly_summary(self):
        return self.generate_daily_report() + "\n\n## Weekly Trends\n(Trends would be computed from historical data)"

if __name__ == "__main__":
    reporter = IntelligenceReport()
    print(reporter.generate_daily_report())