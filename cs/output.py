from sqlalchemy.engine.row import Row


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
            "descriptionText": dict_row["description_text"],
        }

        output.append(output_row)
    return output


def build_sumamry_stats(rows):
    pass
