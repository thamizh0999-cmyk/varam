from pathlib import Path

path = Path("clinical/views.py")
source = path.read_text(encoding="utf-8-sig")


def patch_report(source, function_name, model_query, old_filter, new_filter):
    marker = f"def {function_name}(request):"
    start = source.find(marker)

    if start < 0:
        raise SystemExit(f"Function not found: {function_name}")

    next_view = source.find("\n@login_required\ndef ", start + len(marker))
    if next_view < 0:
        next_view = len(source)

    section = source[start:next_view]

    if "facility = get_user_facility(request)" not in section:
        section = section.replace(
            marker,
            marker + "\n    facility = get_user_facility(request)",
            1,
        )

    query_start = section.find(model_query)
    if query_start < 0:
        raise SystemExit(f"Query not found in {function_name}")

    query_end = section.find(")", query_start)
    if query_end < 0:
        raise SystemExit(f"Query boundary not found in {function_name}")

    query = section[query_start:query_end + 1]

    if new_filter in query:
        print(f"{function_name}: facility filter already present.")
    else:
        if old_filter not in query:
            raise SystemExit(
                f"Expected filter not found in {function_name}. "
                "No changes saved."
            )
        query = query.replace(old_filter, new_filter, 1)
        section = (
            section[:query_start]
            + query
            + section[query_end + 1:]
        )
        print(f"{function_name}: facility filter added.")

    return source[:start] + section + source[next_view:]


source = patch_report(
    source,
    "monthly_top20_op_report",
    "DailyDiseaseCount.objects.filter(",
    "disease=disease,",
    "facility=facility,\n                  disease=disease,",
)

source = patch_report(
    source,
    "monthly_top20_ip_report",
    "IPDiseaseRecord.objects.filter(",
    "disease=disease,",
    "patient__facility=facility,\n                  disease=disease,",
)

path.write_text(source, encoding="utf-8")
print("Top 20 report patch completed.")