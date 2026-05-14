"""Export J.A.K.E knowledge to Obsidian / Roam / Logseq format."""

from pathlib import Path
import sqlite3

def export_to_obsidian(output_dir: str = "export/obsidian"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect("graph/triples.db")
    
    # Export entities as Markdown files
    cursor = conn.execute("SELECT DISTINCT subject FROM triples")
    for (subject,) in cursor.fetchall():
        safe_name = subject.replace("/", "-").replace(" ", "_")[:50]
        content = f"# {subject}\n\n## Relations\n\n"
        rels = conn.execute("SELECT predicate, object FROM triples WHERE subject = ?", (subject,)).fetchall()
        for pred, obj in rels:
            content += f"- [[{obj}]] ({pred})\n"
        
        with open(f"{output_dir}/{safe_name}.md", "w") as f:
            f.write(content)
    
    print(f"Exported to {output_dir} (Obsidian compatible)")

if __name__ == "__main__":
    export_to_obsidian()