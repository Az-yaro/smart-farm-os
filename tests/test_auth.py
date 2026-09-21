
def test_login_success(client, db):
    from database import User, SmartFarmOS
    from security.password import hash_password

    farm = SmartFarmOS(
        farm_name="Test Farm",
        public_id="SF0-TEST-01"
    )
    db.add(farm)
    db.flush()

    user = User(
        name="Test User",
        email="mytestemail@gmail.com",
        username="newtestuser",
        password_hash=hash_password("test-correct-password"),
        farm_id=farm.id,
        role="Owner",
        is_active=True,
        is_verified=True
    )
    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "newtestuser",
            "password": "test-correct-password"
        },
    )


    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"]  == "bearer"

def test_password_failure(client, db):
    from database import User, SmartFarmOS
    from security.password import hash_password

    farm = SmartFarmOS(
        farm_name="Test Farm",
        public_id="SF0-TEST-02"
    )
    db.add(farm)
    db.flush()

    user = User(
        name="Test User",
        email="mytestemail@gmail.com",
        username="correct-username",
        password_hash=hash_password("correct-password"),
        farm_id=farm.id,
        role="Owner",
        is_active=True,
        is_verified=True
    )
    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "correct-username",
            "password": "wrong-password"
        },
    )

    assert response.status_code == 401

def test_username_failure(client, db):
    from database import User, SmartFarmOS
    from security.password import hash_password

    farm = SmartFarmOS(
        farm_name="Test Farm",
        public_id="SF0-TEST-03"
    )
    db.add(farm)
    db.flush()

    user = User(
        name="Test User",
        email="mytestemail@gmail.com",
        username="correct-username",
        password_hash=hash_password("correct-password"),
        farm_id=farm.id,
        role="Owner",
        is_active=True,
        is_verified=True
    )
    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "wrong-username",
            "password": "correct-password"
        },
    )

    assert response.status_code == 401
