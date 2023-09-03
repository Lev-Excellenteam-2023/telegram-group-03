import random
from DB import firebase_handler as fh


def generate_mock_users(num=1):
    first_names = ["John", "Jane", "Mike", "Sarah", "Tom", "Linda", "Robert", "Emily", "Steve", "Lucy"]
    last_names = ["Doe", "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez"]

    symptoms_list = ["coughing", "fever", "fatigue", "headache", "sore throat"]

    users = []

    for _ in range(num):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        phone = "555-{:04d}".format(random.randint(0, 9999))

        symptoms = random.sample(symptoms_list, k=random.randint(1, 3))
        severity = random.randint(1, 10)

        conversation_txt = "Patient mentioned feeling {}. They've been experiencing {} for a few days." \
                           " Recommended to rest and monitor symptoms.".format(
            symptoms[0],
            " and ".join(symptoms)
        )

        user = {
            'name': f"{first_name} {last_name}",
            'phone': phone,
            'symptom': ", ".join(symptoms),
            'severity': severity,
            'conversation_txt': conversation_txt
        }

        users.append(user)

    return users


def main():
    mock_users = generate_mock_users()

    fh.initialize_db()

    for user in mock_users:
        fh.add_record(user['name'], user['phone'], user['symptom'], user['conversation_txt'], user['severity'])

    print(f"{len(mock_users)} users added to the database.")


if __name__ == "__main__":
    main()
