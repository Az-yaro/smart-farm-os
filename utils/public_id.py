import secrets

ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def generate_public_id(length=10):
    first_part = "".join(
        secrets.choice(ALPHABET)
        for _ in range(4)
    )

    second_part = "".join(
        secrets.choice(ALPHABET)
        for _ in range(2)
    )

    return f"SFO-{first_part}-{second_part}"

for _ in range(10):
    print(generate_public_id())
