
def test_worker_can_not_create_tank(client, db):
    from database import User, SmartFarmOS
    from security.password import hash_password

    farm = SmartFarmOS(
        farm_name="Test Farm",
        public_id="SF0-TEST-04"
    )

    db.add(farm)
    db.flush()

    user = User(
        name="Test User",
        email="mytestemail@gmail.com",
        username="worker-user",
        password_hash=hash_password("worker-password"),
        farm_id=farm.id,
        role="worker",
        is_active=True,
        is_verified=True,
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/auth/login",
        data={
            "username": "worker-user",
            "password": "worker-password",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.post(
        "/tanks/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "tank_id": "tank-alpha",
            "capacity_liters": 10000,
            "ammonia_ppm": 0.0,
            "ph": 7.0,
            "temp_c": 27.0,
            "smart_farm_os_id":farm.id
        },
    )

    assert response.status_code == 403

def test_owner_can_create_tank(client, db):
    from database import User, SmartFarmOS
    from security.password import hash_password

    farm = SmartFarmOS(
        farm_name="Test Farm",
        public_id="SF0-TEST-05"
    )

    db.add(farm)
    db.flush()

    user = User(
        name="Test User",
        email="mytestemail@gmail.com",
        username="owner-user",
        password_hash=hash_password("owner-password"),
        farm_id=farm.id,
        role="Owner",
        is_active=True,
        is_verified=True,
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/auth/login",
        data={
            "username": "owner-user",
            "password": "owner-password",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.post(
        "/tanks/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "tank_id": "tank-alpha",
            "capacity_liters": 10000,
            "ammonia_ppm": 0.0,
            "ph": 7.0,
            "temp_c": 27,
            "smart_farm_os_id":farm.id
        },
    )

    assert response.status_code == 200

def test_admin_can_create_tank(client, db):
    from database import User, SmartFarmOS
    from security.password import hash_password

    farm = SmartFarmOS(
        farm_name="Test Farm",
        public_id="SF0-TEST-06"
    )

    db.add(farm)
    db.flush()

    user = User(
        name="Test User",
        email="mytestemail@gmail.com",
        username="admin-user",
        password_hash=hash_password("admin-password"),
        farm_id=farm.id,
        role="Admin",
        is_active=True,
        is_verified=True,
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/auth/login",
        data={
            "username": "admin-user",
            "password": "admin-password",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.post(
        "/tanks/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "tank_id": "tank-alpha",
            "capacity_liters": 10000,
            "ammonia_ppm": 0.0,
            "ph": 7.0,
            "temp_c": 2,
            "smart_farm_os_id":farm.id
        },
    )

    assert response.status_code == 200

def test_worker_can_not_delete_tank(client, db):
    from database import User, SmartFarmOS
    from security.password import hash_password

    farm = SmartFarmOS(
        farm_name="Test Farm",
        public_id="SF0-TEST-07"
    )

    db.add(farm)
    db.flush()

    user = User(
        name="Test User",
        email="mytestemail@gmail.com",
        username="worker-user",
        password_hash=hash_password("worker-password"),
        farm_id=farm.id,
        role="worker",
        is_active=True,
        is_verified=True,
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/auth/login",
        data={
            "username": "worker-user",
            "password": "worker-password",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.delete(
        "/tanks/tank-alpha",
        headers={
            "Authorization": f"Bearer {token}"
        },

    )
    assert response.status_code == 403
