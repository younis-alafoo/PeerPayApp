#user_data
from models.user import UserModel
#from models import UserModel

def create_test_users():
    user1 = UserModel(user_id=1,username="aa", role='User', full_name="Ali Ahmed", email="ali.ahmed@email.com")
    user1.set_password("securepassword2")
    user2 = UserModel(user_id=2,username="bb", role='User', full_name="Brain brown", email="brain.brown@email.com")
    user2.set_password("securepassword3")
    user3 = UserModel(user_id=3,username="cc", role='User', full_name="Cate Clark", email="cate.clark@email.com")
    user3.set_password("securepassword4")
    user4 = UserModel(user_id=4,username="dd", role='User', full_name="David Dixon", email="david.dixon@email.com")
    user4.set_password("securepassword5")
    user5 = UserModel(user_id=5,username="ee", role='User', full_name="Eli Evans", email="eli.evans@email.com")
    user5.set_password("securepassword6")
    user6 = UserModel(user_id=6,username="Yunis", role='Admin', full_name="Yunis Abdulla", email="yunis.abdulla@email.com")
    user6.set_password("securepassword1")

    return [user1, user2, user3, user4, user5, user6]

user_list = create_test_users()