import sqlite3
import tomli

class JAKEIntelligence:
    def __init__(self):
        with open("config.toml", "rb") as f:
            self.config = tomli.load(f)
        self.conn = sqlite3.connect(self.config["paths"]["root"] + "/" + self.config["paths"]["graph_db"])
    
    def run_health_check(self):
        print("🔍 Running Knowledge Health Check...")
        
        # Contradictions (same subject+predicate, different objects)
        cursor = self.conn.execute("""
            SELECT subject, predicate, COUNT(DISTINCT object) as conflicts
            FROM triples
            GROUP BY subject, predicate
            HAVING conflicts > 1
        """)
        issues = cursor.fetchall()
        
        if issues:
            print(f"⚠️ Found {len(issues)} potential contradictions:")
            for issue in issues[:5]:
                print(f"  • {issue[0]} {issue[1]}")
        else:
            print("✅ No obvious contradictions found.")
        
        print("Health check complete.")