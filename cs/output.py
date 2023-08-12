import json
from collections import Counter

from sqlalchemy.engine.row import Row


def build_output(rows: list[Row]) -> str:
    """Formats the results ready to be displayed"""
    results = build_policy_sequence(rows)
    summary = build_summary_stats(rows)
    summary["matches"] = results

    return json.dumps(summary, indent=2)


def build_policy_sequence(rows: list[Row]) -> list[dict]:
    """Convert rows to dictionary for output

    Args:
        rows (_type_): policy rows from a sqlalchemy query

    Returns:
        list[dict]: iterable of policy objects
    """
    output = []
    for row in rows:
        dict_row = row._asdict()

        output_row = {
            "policyTitle": dict_row["policy_title"],
            "policyId": dict_row["policy_id"],
            "sectors": dict_row["sectors"].split(";"),
        }

        output.append(output_row)
    return output


def build_summary_stats(rows: list[Row]) -> dict:
    """Build summary stats from a sequence of row objects

    Args:
        rows (list[Row]): rsults of an sqlalchemy query

    Returns:
        dict: formatted summary stats
    """
    all_sectors = []
    for row in rows:
        sectors = row._asdict().get("sectors")
        all_sectors.extend(sectors.split(";"))
    sector_counts = Counter(all_sectors)
    output = {
        "sectors": sector_counts,
        "totalMatches": len(rows),
    }

    return output
