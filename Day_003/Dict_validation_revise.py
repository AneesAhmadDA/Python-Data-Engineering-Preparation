def validate_record(record):
    if not isinstance(record,dict):
        print("Invalid record entry: it must needs to be dict")
        return False

    required_fields=[
        "record_id",
        "event_type",
        "event_timestamp"
    ]

    missing_fields =[
        field for field in required_fields
        if field not in record
    ]
    if missing_fields:
        print(f"Invalid entry for fields:{missing_fields}")
        return False

    empty_fields=[
        field for field in required_fields
        if record[field] is None
        or (isinstance(record[field],str) and not record[field].strip())
    ]

    if empty_fields:
        print(f"Empty fields error:{empty_fields}")

    print(f"valid records :{record}")
    return True

Record1 = {
    "record_id": 1,
    "event_type": "Login",
    "event_timestamp": "2026-11-09"
}

Record2 = {
    "record_id": 2,
    "event_type": "Logout",
    "event_timestamp": "2026-11-10"
}

Record3 = {
    "record_id": 3,
    "event_type": "Login",
    "event_timestamp": "2026-11-11"
}

Record4 = {
    "record_id": 4,
    "event_type": "Logout",
    "event_timestamp": "2026-11-09"
}

Record5 = {
    "record_id": 5,
    "event_type": "Login",
    "event_timestamp": "2026-11-08"
}

Record6 = {
    "record_id": 6,
    "Type": "Login",
    "event_timestamp": "2026-11-08"
}

Record7 = {
    "id": 7,
    "Type": "Login",
    "event_timestamp": "2026-11-08"
}

Record8 = {
    "record_id": 8,
    "event_type": " ",
    "event_timestamp": "2026-11-08"
}

Record9 = {
    "record_id": 9,
    "event_type": " ",
    "event_timestamp": "  "
}


Record10 = {
    "record_id": 10,
    "type": " ",
    "event_timestamp": "  "
}
validate_record(Record1)
validate_record(Record2)
validate_record(Record3)
validate_record(Record4)
validate_record(Record5)
validate_record(Record6)
validate_record(Record7)
validate_record(Record8)
validate_record(Record9)
validate_record(Record10)