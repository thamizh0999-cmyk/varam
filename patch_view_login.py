from pathlib import Path
import ast

path = Path("clinical/views.py")
source = path.read_text(encoding="utf-8-sig")
tree = ast.parse(source)

targets = {
    "ip_fortnightly_report",
    "ip_disease_report",
    "ip_ncd_report",
    "disease_master",
    "daily_disease_count",
    "monthly_disease_report",
    "daily_ncd_count",
    "centre_profile",
    "anc_register",
    "anc_patient_add",
    "anc_patient_edit",
    "anc_patient_detail",
    "anc_visit_add",
    "anc_visit_edit",
    "anc_monthly_report_excel",
    "anc_monthly_report",
    "monthly_top20_op_report",
    "monthly_top20_ip_report",
}

lines = source.splitlines(keepends=True)
added = []

for node in sorted(
    (n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in targets),
    key=lambda n: n.lineno,
    reverse=True,
):
    decorator_names = []
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name):
            decorator_names.append(decorator.id)

    if "login_required" not in decorator_names:
        lines.insert(node.lineno - 1, "@login_required\n")
        added.append(node.name)

path.write_text("".join(lines), encoding="utf-8")
print("Added login decorators:", ", ".join(sorted(added)) or "none needed")
