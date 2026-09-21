
def test_user_a_can_not_access_user_b_farm(client, db):
    from database import User, SmartFarmOS, Tank
    from security.password import hash_password

    farm_a = SmartFarmOS(
        farm_name="Test Farm A",
        public_id="SF0-TEST-08"
    )

    farm_b = SmartFarmOS(
        farm_name="Test Farm B",
        public_id="SF0-TEST-09"
    )

    db.add_all([farm_a, farm_b])
    db.flush()

    tank_b = Tank(
        tank_id="tank-alpha",
        capacity_liters=10000,
        ammonia_ppm=0.0,
        ph=7.0,
        temp_c=27,
        is_active=True,
        smart_farm_os_id=farm_b.id,

    )

    user_a = User(
        name="Test User A",
        email="user0a@gmail.com",
        username="user-a",
        password_hash=hash_password("user-a-password"),
        farm_id=farm_a.id,
        role="Owner",
        is_active=True,
        is_verified=True,
    )

    user_b = User(
        name="Test User B",
        email="user0b@gmail.com",
        username="user-b",
        password_hash=hash_password("user-b-password"),
        farm_id=farm_b.id,
        role="Owner",
        is_active=True,
        is_verified=True,
    )

    db.add_all([tank_b, user_a, user_b])
    db.commit()

    login_response = client.post(
        "/auth/login",
        data={
            "username": "user-a",
            "password": "user-a-password",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.get(
        "/tanks/tank-alpha",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404

def test_user_only_has_access_to_own_farm(client, db):
    from database import User, SmartFarmOS, Tank
    from security.password import hash_password

    farm_a = SmartFarmOS(
        farm_name="Test Farm A",
        public_id="SF0-TEST-10"
    )

    farm_b = SmartFarmOS(
        farm_name="Test Farm B",
        public_id="SF0-TEST-11"
    )

    db.add_all([farm_a, farm_b])
    db.flush()

    tank_a = Tank(
        tank_id="tank-alpha",
        capacity_liters=10000,
        ammonia_ppm=0.0,
        ph=7.0,
        temp_c=27,
        is_active=True,
        smart_farm_os_id=farm_a.id,
    )

    tank_b = Tank(
        tank_id="tank-beta",
        capacity_liters=20000,
        ammonia_ppm=0.0,
        ph=6.5,
        temp_c=28.0,
        is_active=True,
        smart_farm_os_id=farm_b.id,
    )

    user_a = User(
        name="Test User A",
        email="user0a@gmail.com",
        username="user-a",
        password_hash=hash_password("user-a-password"),
        farm_id=farm_a.id,
        role="worker",
        is_active=True,
        is_verified=True,
    )

    db.add_all([tank_a, tank_b, user_a])
    db.commit()

    login_response = client.post(
        "/auth/login",
        data={
            "username": "user-a",
            "password": "user-a-password",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.get(
        "/tanks/",
        headers={
            f"Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    tanks = response.json()
    tank_ids = [tank["tank_id"] for tank in tanks]

    assert "tank-alpha" in tank_ids
    assert "tank-beta" not in tank_ids
