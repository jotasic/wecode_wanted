import datetime
from unittest import mock

from django.contrib.auth import get_user_model
from rest_framework      import status
from rest_framework.test import APITestCase

from .models import Post


class PostTestCase(APITestCase):
    maxDiff = None

    def setUp(self):
            self.user_wanted = get_user_model().objects.create_user(
                email    = 'wanted@gmail.com',
                password = '12345678',
                nickname = '원티드',
            )

            self.user_wecode = get_user_model().objects.create_user(
                email    = 'wecode@gmail.com',
                password = '12345678',
                nickname = '위코드',
            )

            self.mocked_date_time = datetime.datetime(2021,1,1,0,0,0)

            with mock.patch('django.utils.timezone.now', mock.Mock(return_value=self.mocked_date_time)):
                self.post_today_study =Post.objects.create(
                    author      = self.user_wanted,
                    title     = '스터디 활동',
                    content   = '오늘은 팀원들과 만나서 Python에 대해서 공부하였습니다.'
                )

                self.post_today_hooby = Post.objects.create(
                    author      = self.user_wanted,
                    title     = '오늘의 취미 활동',
                    content   = '오늘은 등산을 하였습니다.'
                )
    
    def test_get_post_list(self):
        response = self.client.get('/posts')
        expected_data = [
        {
            "id": self.post_today_study.id,
            "author": self.user_wanted.nickname,
            "title": "스터디 활동",
            "content": "오늘은 팀원들과 만나서 Python에 대해서 공부하였습니다.",
            "created_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "edited_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
        },
        {
            "id": self.post_today_hooby.id,
            "author": self.user_wanted.nickname,
            "title": "오늘의 취미 활동",
            "content": "오늘은 등산을 하였습니다.",
            "created_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "edited_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
        }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)

    def test_get_post_list_using_pagination(self):
        response = self.client.get('/posts?offset=1&limit=1')
        expected_data = {
            'count': 2,
            'next': None,
            'previous': 'http://testserver/posts?limit=1',
            "results" : [
                {
                    "id": self.post_today_hooby.id,
                    "author": self.user_wanted.nickname,
                    "title": "오늘의 취미 활동",
                    "content": "오늘은 등산을 하였습니다.",
                    "created_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    "edited_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),}
        ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)

    def test_create_blog_post_no_token(self):
        data = {
            'title'     : '오늘의 영화',
            'content'   : '오늘의 영화는 코미디 입니다!',
        }
        response = self.client.post('/posts', data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post(self):
        self.client.force_authenticate(self.user_wanted)
        data = {
            'title'     : '오늘의 영화',
            'content'   : '오늘의 영화는 코미디 입니다!',
        }
        response = self.client.post('/posts', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_post(self):
        self.client.force_authenticate(self.user_wanted)
        data = {
            'content' : '오늘은 등산을 하였습니다. 재미있었습니다.',
        }
        response = self.client.patch(f'/posts/{self.post_today_hooby.id}', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_post_no_token(self):
        data = {
            'content' : '오늘은 등산을 하였습니다. 재미있었습니다.',
        }
        response = self.client.patch(f'/posts/{self.post_today_hooby.id}', data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_post_diffent_user(self):
        self.client.force_authenticate(self.user_wecode)
        data = {
            'content' : '오늘은 등산을 하였습니다. 재미있었습니다.',
        }
        response = self.client.patch(f'/posts/{self.post_today_hooby.id}', data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post(self):
        self.client.force_authenticate(self.user_wanted)
        response = self.client.delete(f'/posts/{self.post_today_hooby.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_diffent_user(self):
        self.client.force_authenticate(self.user_wecode)
        response = self.client.delete(f'/posts/{self.post_today_hooby.id}')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_no_token(self):
        response = self.client.delete(f'/posts/{self.post_today_hooby.id}')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)