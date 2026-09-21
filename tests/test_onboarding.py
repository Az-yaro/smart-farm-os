
def test_onboarding(client, db):
    response = client.post(
        "/onboarding/",
        json={
            "farm_name": "Test Farm",
            "name": "Test User",
            "email": "mytestemail@gmail.com",
            "username": "test-user",
            "password": "test-password",
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["farm_name"] == "Test Farm"
    assert data["username"] == "test-user"
    assert data["public_id"].startswith("SFO-")
    assert data["role"] == "Owner"
    assert data["is_verified"] is False

def test_onboarding_with_existing_farm_and_user(client, db):
    from database import User, SmartFarmOS

    response = client.post(
        "/onboarding/",
        json={
            "farm_name": "Test Farm",
            "name": "Test User",
            "email": "dbtest@gmail.com",
            "username": "test-user",
            "password": "test-password",
        }
    )
    assert response.status_code == 200

    farm = db.query(SmartFarmOS).filter(
        SmartFarmOS.farm_name == "Test Farm"
    ).first()

    user = db.query(User).filter(
        User.username == "test-user"
    ).first()

    assert farm is not None
    assert user is not None

    assert user.farm_id == farm.id
    assert user.role == "Owner"
    assert user.is_verified is False

def test_onboarding_with_existing_email(client, db):

    first_response = client.post(
        "/onboarding/",
        json={
            "farm_name": "First Farm",
            "name": "First User",
            "email": "sample1@gmail.com",
            "username": "user1",
            "password": "test-password",
        }
    )
    assert first_response.status_code == 200

    second_response = client.post(
        "/onboarding/",
        json={
            "farm_name": "Second Farm",
            "name": "Second User",
            "email": "sample1@gmail.com",
            "username": "user2",
            "password": "test-password",
        }
    )
    assert second_response.status_code == 400
    assert "email" in second_response.json()["message"].lower()

def test_onboarding_with_existing_username(client, db):
    first_response = client.post(
        "/onboarding/",
        json={
            "farm_name": "First Farm_b",
            "name": "First User_b",
            "email": "sample2@gmail.com",
            "username": "user1",
            "password": "test-password",
        }
    )
    assert first_response.status_code == 200

    second_response = client.post(
        "/onboarding/",
        json={
            "farm_name": "Second Farm_b2",
            "name": "Second User_b2",
            "email": "sample3@gmail.com",
            "username": "user1",
            "password": "test-password",
        }
    )
    assert second_response.status_code == 400
    assert "username" in second_response.json()["message"].lower()

def test_onboarding_with_existing_farm_name(client, db):
    first_response = client.post(
        "/onboarding/",
        json={
            "farm_name": "Farm_c",
            "name": "User_c",
            "email": "sample4@gmail.com",
            "username": "user3",
            "password": "test-password",
        }
    )
    assert first_response.status_code == 200

    second_response = client.post(
        "/onboarding/",
        json={
            "farm_name": "Farm_c",
            "name": "User_c2",
            "email": "sample5@gmail.com",
            "username": "user4",
            "password": "test-password",
        }
    )
    assert second_response.status_code == 400
    assert "farm" in second_response.json()["message"].lower()
