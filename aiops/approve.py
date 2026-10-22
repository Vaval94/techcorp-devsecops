"""Enregistre une décision humaine sur une remédiation proposée.

N'EXÉCUTE RIEN : l'action approuvée doit ensuite être réalisée par l'opérateur,
selon le plan de restauration (docs/plan-restauration.md).

    python -m aiops.approve --action 1 --decision approuvé --by "Prénom Nom" --comment "rollback validé"
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from aiops.report import render_markdown


def record(report: dict, index: int, decision: str, by: str, comment: str = "") -> dict:
    actions = report["analyse_ia"]["remediation_proposee"]
    if not 1 <= index <= len(actions):
        raise ValueError(f"action {index} inexistante (1..{len(actions)})")
    if not by.strip():
        raise ValueError("le nom de l'approbateur est obligatoire")
    action = actions[index - 1]
    action["statut"] = "approuvé (à exécuter manuellement)" if decision == "approuvé" else "refusé"
    report.setdefault("approbations", []).append({
        "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "action_index": index, "action": action["action"], "decision": decision,
        "par": by.strip(), "commentaire": comment,
    })
    return report


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--action", type=int, required=True)
    p.add_argument("--decision", choices=["approuvé", "refusé"], required=True)
    p.add_argument("--by", required=True)
    p.add_argument("--comment", default="")
    a = p.parse_args(argv)
    report = json.loads(Path("report.json").read_text(encoding="utf-8"))
    record(report, a.action, a.decision, a.by, a.comment)
    Path("report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    Path("incident-report.md").write_text(render_markdown(report), encoding="utf-8")
    print(f"Décision enregistrée : action {a.action} {a.decision} par {a.by}. Rien n'a été exécuté.")


if __name__ == "__main__":
    main()
