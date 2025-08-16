from controllers.users import create_user, login
from serializers.user import UserSchema, UserLogin
from models.user import UserModel
from fastapi import HTTPException

def test_login_success():
    payload = UserLogin(username="aa", password="securepassword2")

    user = UserModel(
        user_id=2,
        username="aa",
        full_name="Ali Ahmed",
        email="ali.ahmed@email.com",
        role="User"
    )
    user.set_password("securepassword2")  # hash the correct password

    db = type("DB", (), {
        "query": lambda self, model: type("Query", (), {
            "filter": lambda self, *args: self,
            "first": lambda self: user
        })()
    })()

    result = login(user=payload, db=db)
    assert "token" in result
    assert result["message"] == "Login successful"

def test_login_user_not_found():
    payload = UserLogin(username="doesnotexists", password="anything")

    db = type("DB", (), {
        "query": lambda self, model: type("Query", (), {
            "filter": lambda self, *args: self,
            "first": lambda self: None  # simulate user not found
        })()
    })()

    try:
        login(user=payload, db=db)
        assert False, "Expected HTTPException"
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Invalid username or password"

def test_create_user_success():
    payload = UserSchema(
        username="newuser",
        full_name="New User",
        email="new@example.com",
        password="securepass",
        currency="USD"
    )

    def fake_query(self, model):
        return type("Query", (), {
            "filter": lambda self, *args: self,
            "first": lambda self: None
        })()

    db = type("DB", (), {
        "query": fake_query,
        "add": lambda self, obj: None,
        "commit": lambda self: None,
        "refresh": lambda self, obj: setattr(obj, "user_id", 1)
    })()

    result = create_user(user=payload, db=db)
    assert isinstance(result, UserModel)
    assert result.username == "newuser"
    assert result.user_id == 1

def test_create_user_existing_user():
    payload = UserSchema(
        username="existinguser",
        full_name="Existing User",
        email="existing@example.com",
        password="securepass",
        currency="USD"
    )

    existing_user = UserModel(
        username="existinguser",
        full_name="Existing User",
        email="existing@example.com",
        role="User"
    )

    db = type("DB", (), {
        "query": lambda self, model: type("Query", (), {
            "filter": lambda self, *args: self,
            "first": lambda self: existing_user
        })()
    })()

    try:
        create_user(user=payload, db=db)
        assert False, "Expected HTTPException"
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Username or email already exists"