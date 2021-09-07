import pytest
from django.contrib.auth.models import User
from faker import Faker

from utils import fake_user_data_for_sign_up

faker = Faker("pl_PL")


@pytest.mark.django_db
def test_add_user(client, set_up):
    users_before = User.objects.count()
    new_user = fake_user_data_for_sign_up()
    response = client.post("/register/", {**new_user})
    assert response.status_code == 302
    assert User.objects.count() == users_before + 1


@pytest.mark.django_db
def test_login_and_logout(client, set_up):
    user = User.objects.first()
    # assert user.authenticated() is not None  # ???
    response = client.post("/login/", {"login": user.username, "password": user.password})
    assert response.status_code == 200
    # assert user.authenticated() is not None

    response = client.get("/logout/")
    # assert response.status_code == 200
    assert not user.is_authenticated()

#
# @pytest.mark.django_db
# def test_get_cinemas_list(client, set_up):
#     response = client.get("/cinemas/", {}, format='json')
#
#     assert response.status_code == 200
#     assert Cinema.objects.count() == len(response.data)
#
#
# @pytest.mark.django_db
# def test_get_cinema_detail(client, set_up):
#     cinema = Cinema.objects.first()
#     response = client.get(f"/cinemas/{cinema.id}/", {}, format='json')
#
#     assert response.status_code == 200
#     for field in ("name", "city", "movies"):
#         assert field in response.data
#
#
# @pytest.mark.django_db
# def test_delete_cinema(client, set_up):
#     cinema = Cinema.objects.first()
#     response = client.delete(f"/cinemas/{cinema.id}/", {}, format='json')
#     assert response.status_code == 204
#     cinema_ids = [cinema.id for cinema in Cinema.objects.all()]
#     assert cinema.id not in cinema_ids
#
#
# @pytest.mark.django_db
# def test_update_cinema(client, set_up):
#     cinema = Cinema.objects.first()
#     response = client.get(f"/cinemas/{cinema.id}/", {}, format='json')
#     cinema_data = response.data
#     new_city = "bERLINnn"
#     cinema_data["city"] = new_city
#     response = client.patch(f"/cinemas/{cinema.id}/", cinema_data, format='json')
#     assert response.status_code == 200
#     cinema_obj = Cinema.objects.get(id=cinema.id)
#     assert cinema_obj.city == new_city
#
#
# @pytest.mark.django_db
# def test_add_screening(client, set_up):
#     screening_count = Screening.objects.count()
#     new_screening_data = {"cinema": Cinema.objects.first().id, "movie": Movie.objects.first().id,
#                           "date": faker.date_time(tzinfo=TZ).isoformat()}
#     response = client.post("/screening/", new_screening_data, format='json')
#     assert response.status_code == 201
#     assert Screening.objects.count() == screening_count + 1
#
#     new_screening_data["date"] = new_screening_data["date"].replace('+00:00', 'Z')
#
#     for key, value in new_screening_data.items():
#         assert key in response.data
#         assert response.data[key] == value
#
#
# @pytest.mark.django_db
# def test_get_screening_list(client, set_up):
#     response = client.get("/screening/", {}, format='json')
#     assert response.status_code == 200
#     assert Screening.objects.count() == len(response.data)
#
#
# @pytest.mark.django_db
# def test_get_screening_detail(client, set_up):
#     screening = Screening.objects.first()
#     response = client.get(f"/screening/{screening.id}/", {}, format='json')
#     assert response.status_code == 200
#     for field in ('movie', 'cinema', 'date'):
#         assert field in response.data
#
#
# @pytest.mark.django_db
# def test_delete_screening(client, set_up):
#     screening = Screening.objects.first()
#     response = client.delete(f"/screening/{screening.id}/", {}, format='json')
#     assert response.status_code == 204
#     screenings_ids = [screening.id for screening in Screening.objects.all()]
#     assert screening.id not in screenings_ids
#
#
# @pytest.mark.django_db
# def test_update_screening(client, set_up):
#     screening = Screening.objects.first()
#     response = client.get(f"/screening/{screening.id}/", {}, format='json')
#     screening_data = response.data
#     new_cinema = Cinema.objects.last()
#     screening_data["cinema"] = new_cinema.id
#     response = client.patch(f"/screening/{screening.id}/", screening_data, format='json')
#     assert response.status_code == 200
#     screening_obj = Screening.objects.get(id=screening.id)
#     assert screening_obj.cinema == new_cinema
