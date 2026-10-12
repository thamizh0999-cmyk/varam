from .models import DailyCensus, IPPatient


# ---------------------------------------------------------
# 8 October 2026 is the transition date.
#
# Before this date:
#   Use historical DailyCensus IP data.
#
# From this date:
#   Use IP Patient Register.
#
# This can be changed later if required.
# ---------------------------------------------------------
IP_REGISTER_START_DATE = "2026-10-08"


def _empty_summary():
    return {
        "morning_new_male": 0,
        "morning_new_female": 0,
        "morning_new_male_child": 0,
        "morning_new_female_child": 0,

        "morning_old_male": 0,
        "morning_old_female": 0,
        "morning_old_male_child": 0,
        "morning_old_female_child": 0,

        "morning_new_total": 0,
        "morning_old_total": 0,
        "morning_total": 0,

        "evening_new_male": 0,
        "evening_new_female": 0,
        "evening_new_male_child": 0,
        "evening_new_female_child": 0,

        "evening_old_male": 0,
        "evening_old_female": 0,
        "evening_old_male_child": 0,
        "evening_old_female_child": 0,

        "evening_new_total": 0,
        "evening_old_total": 0,
        "evening_total": 0,

        "new_male": 0,
        "new_female": 0,
        "new_male_child": 0,
        "new_female_child": 0,
        "new_total": 0,

        "old_male": 0,
        "old_female": 0,
        "old_male_child": 0,
        "old_female_child": 0,
        "old_total": 0,

        "total": 0,
        "source": "none",
    }


def _count(group, sex, child):
    return sum(
        1
        for patient in group
        if patient.sex == sex and patient.is_child == child
    )


def _historical_ip_summary(target_date, facility):

    record = DailyCensus.objects.filter(
        facility=facility,
        date=target_date
    ).first()

    if not record:
        return _empty_summary()

    result = _empty_summary()

    # Historical morning IP
    result["morning_old_male"] = record.ip_morning_male
    result["morning_old_female"] = record.ip_morning_female
    result["morning_old_male_child"] = record.ip_morning_male_child
    result["morning_old_female_child"] = record.ip_morning_female_child

    # Historical evening IP
    result["evening_old_male"] = record.ip_evening_male
    result["evening_old_female"] = record.ip_evening_female
    result["evening_old_male_child"] = record.ip_evening_male_child
    result["evening_old_female_child"] = record.ip_evening_female_child

    result["morning_old_total"] = sum([
        result["morning_old_male"],
        result["morning_old_female"],
        result["morning_old_male_child"],
        result["morning_old_female_child"],
    ])

    result["morning_total"] = result["morning_old_total"]

    result["evening_old_total"] = sum([
        result["evening_old_male"],
        result["evening_old_female"],
        result["evening_old_male_child"],
        result["evening_old_female_child"],
    ])

    result["evening_total"] = result["evening_old_total"]

    result["old_male"] = (
        result["morning_old_male"]
        + result["evening_old_male"]
    )

    result["old_female"] = (
        result["morning_old_female"]
        + result["evening_old_female"]
    )

    result["old_male_child"] = (
        result["morning_old_male_child"]
        + result["evening_old_male_child"]
    )

    result["old_female_child"] = (
        result["morning_old_female_child"]
        + result["evening_old_female_child"]
    )

    result["old_total"] = (
        result["old_male"]
        + result["old_female"]
        + result["old_male_child"]
        + result["old_female_child"]
    )

    result["total"] = result["old_total"]

    result["source"] = "Historical Daily Census"

    return result


def calculate_ip_summary(target_date, facility):

    # =========================================================
    # BEFORE 08-10-2026
    # =========================================================

    if target_date.isoformat() < IP_REGISTER_START_DATE:
        return _historical_ip_summary(target_date, facility)


    # =========================================================
    # FROM 08-10-2026
    # USE IP PATIENT REGISTER
    # =========================================================

    patients = IPPatient.objects.filter(
        facility=facility,
        admission_date__lte=target_date
    )

    morning_active = []
    evening_active = []

    for patient in patients:

        # -----------------------------------------------
        # MORNING
        # -----------------------------------------------

        # Evening admission today is not present in
        # morning census.
        if (
            patient.admission_date == target_date
            and patient.admission_session == "EVENING"
        ):
            pass

        else:

            discharged_before = (
                patient.discharge_date
                and patient.discharge_date < target_date
            )

            discharged_morning = (
                patient.discharge_date == target_date
                and patient.discharge_session == "MORNING"
            )

            if not discharged_before and not discharged_morning:
                morning_active.append(patient)


        # -----------------------------------------------
        # EVENING
        # -----------------------------------------------

        discharged_for_evening = (
            patient.discharge_date
            and patient.discharge_date <= target_date
        )

        if not discharged_for_evening:
            evening_active.append(patient)


    # =========================================================
    # NEW / OLD
    # =========================================================

    morning_new = [
        p for p in morning_active
        if p.admission_date == target_date
    ]

    morning_old = [
        p for p in morning_active
        if p.admission_date < target_date
    ]

    evening_new = [
        p for p in evening_active
        if p.admission_date == target_date
    ]

    evening_old = [
        p for p in evening_active
        if p.admission_date < target_date
    ]


    result = _empty_summary()


    # =========================================================
    # MORNING NEW
    # =========================================================

    result["morning_new_male"] = _count(
        morning_new, "M", False
    )

    result["morning_new_female"] = _count(
        morning_new, "F", False
    )

    result["morning_new_male_child"] = _count(
        morning_new, "M", True
    )

    result["morning_new_female_child"] = _count(
        morning_new, "F", True
    )


    # =========================================================
    # MORNING OLD
    # =========================================================

    result["morning_old_male"] = _count(
        morning_old, "M", False
    )

    result["morning_old_female"] = _count(
        morning_old, "F", False
    )

    result["morning_old_male_child"] = _count(
        morning_old, "M", True
    )

    result["morning_old_female_child"] = _count(
        morning_old, "F", True
    )


    # =========================================================
    # EVENING NEW
    # =========================================================

    result["evening_new_male"] = _count(
        evening_new, "M", False
    )

    result["evening_new_female"] = _count(
        evening_new, "F", False
    )

    result["evening_new_male_child"] = _count(
        evening_new, "M", True
    )

    result["evening_new_female_child"] = _count(
        evening_new, "F", True
    )


    # =========================================================
    # EVENING OLD
    # =========================================================

    result["evening_old_male"] = _count(
        evening_old, "M", False
    )

    result["evening_old_female"] = _count(
        evening_old, "F", False
    )

    result["evening_old_male_child"] = _count(
        evening_old, "M", True
    )

    result["evening_old_female_child"] = _count(
        evening_old, "F", True
    )


    # =========================================================
    # TOTALS
    # =========================================================

    result["morning_new_total"] = sum([
        result["morning_new_male"],
        result["morning_new_female"],
        result["morning_new_male_child"],
        result["morning_new_female_child"],
    ])

    result["morning_old_total"] = sum([
        result["morning_old_male"],
        result["morning_old_female"],
        result["morning_old_male_child"],
        result["morning_old_female_child"],
    ])

    result["morning_total"] = (
        result["morning_new_total"]
        + result["morning_old_total"]
    )


    result["evening_new_total"] = sum([
        result["evening_new_male"],
        result["evening_new_female"],
        result["evening_new_male_child"],
        result["evening_new_female_child"],
    ])

    result["evening_old_total"] = sum([
        result["evening_old_male"],
        result["evening_old_female"],
        result["evening_old_male_child"],
        result["evening_old_female_child"],
    ])

    result["evening_total"] = (
        result["evening_new_total"]
        + result["evening_old_total"]
    )


    result["new_male"] = (
        result["morning_new_male"]
        + result["evening_new_male"]
    )

    result["new_female"] = (
        result["morning_new_female"]
        + result["evening_new_female"]
    )

    result["new_male_child"] = (
        result["morning_new_male_child"]
        + result["evening_new_male_child"]
    )

    result["new_female_child"] = (
        result["morning_new_female_child"]
        + result["evening_new_female_child"]
    )

    result["new_total"] = (
        result["new_male"]
        + result["new_female"]
        + result["new_male_child"]
        + result["new_female_child"]
    )


    result["old_male"] = (
        result["morning_old_male"]
        + result["evening_old_male"]
    )

    result["old_female"] = (
        result["morning_old_female"]
        + result["evening_old_female"]
    )

    result["old_male_child"] = (
        result["morning_old_male_child"]
        + result["evening_old_male_child"]
    )

    result["old_female_child"] = (
        result["morning_old_female_child"]
        + result["evening_old_female_child"]
    )

    result["old_total"] = (
        result["old_male"]
        + result["old_female"]
        + result["old_male_child"]
        + result["old_female_child"]
    )

    result["total"] = (
        result["new_total"]
        + result["old_total"]
    )

    result["source"] = "IP Patient Register"

    return result
