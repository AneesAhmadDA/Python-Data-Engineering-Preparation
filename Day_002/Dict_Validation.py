# Day 002: Python Dictionary Validation


# Function to validate an individual event record
def validate_record(record):

    # Step 1: Check whether the input is a dictionary
    if not isinstance(record, dict):
        print("Invalid record: Input must be a dictionary.")
        return False

    # Step 2: Define the mandatory fields
    required_fields = [
        "record_id",
        "event_type",
        "event_timestamp"
    ]

    # Step 3: Check whether required keys exist
    missing_fields = [
        field for field in required_fields
        if field not in record
    ]

    if missing_fields:
        print(f"Invalid record: Missing fields {missing_fields}")
        return False

    # Step 4: Check whether required values are empty
    empty_fields = [
        field for field in required_fields
        if record[field] is None
        or (isinstance(record[field], str) and not record[field].strip())
    ]

    if empty_fields:
        print(f"Invalid record: Empty fields {empty_fields}")
        return False

    # Step 5: If all conditions pass, accept the record
    print(f"Valid record: {record}")

    return True


# Creating five independent dictionaries

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



# Passing individual dictionaries to the function

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