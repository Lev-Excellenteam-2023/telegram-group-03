import firebase_handler as fh  # Assuming your previous code was saved in firebase_handler.py


def main():
    fh.initialize_db()

    fh.add_record("Yehuda", "123-456-7890", "cough", "Had a cough for a week.", 7)
    fh.add_record("Bez", "987-654-3210", "fever", "High fever and fatigue.", 9)

    records = fh.all_records()
    print("\nAll Records:")
    for record in records:
        print(record)

    sorted_users = fh.users_sorted_by_severity()
    print("\nUsers Sorted by Severity:")
    for user in sorted_users:
        print(user)

    fh.delete_by_name("Yehuda")
    fh.delete_by_name("Bez")

    records_after_delete = fh.all_records()
    print("\nRecords After Deletion:")
    for record in records_after_delete:
        print(record)


if __name__ == '__main__':
    main()
