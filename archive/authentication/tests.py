from django.contrib.auth.models import User
from django.conf import settings
from unittest.mock import patch
from archive.authentication.models import Profile
from archive.frames.tests.factories import FrameFactory
from archive.test_helpers import ReplicationTestCase
from rest_framework.test import APITestCase
from django.urls import reverse
import responses
import json

class TestRevokeTokenAPI(APITestCase):
    def setUp(self) -> None:
        super(TestRevokeTokenAPI, self).setUp()
        self.user = User.objects.create(username='test_revoke_token_user')
        Profile.objects.create(user=self.user)
        self.client.force_login(self.user)

    def test_revoke_token(self):
        initial_token = self.user.auth_token
        response = self.client.post(reverse('revoke_api_token'))
        self.assertContains(response, 'API token revoked', status_code=200)
        self.user.refresh_from_db()
        self.assertNotEqual(initial_token, self.user.auth_token)

    def test_unauthenticated(self):
        self.client.logout()
        initial_token = self.user.auth_token
        response = self.client.post(reverse('revoke_api_token'))
        self.assertEqual(response.status_code, 401)
        self.user.refresh_from_db()
        self.assertEqual(initial_token, self.user.auth_token)

class TestAuthentication(ReplicationTestCase):
    @patch('requests.get')
    @patch('requests.post')
    def setUp(self, post_mock, get_mock):
        self.admin_user = User.objects.create_superuser('admin', 'admin@lcgot.net', 'password')
        self.normal_user = User.objects.create(username='frodo')
        Profile.objects.create(user=self.normal_user)
        Profile.objects.create(user=self.admin_user)

    @patch('requests.get')
    @patch('requests.post')
    def test_model_backend(self, post_mock, get_mock):
        self.assertTrue(self.client.login(username='admin', password='password'))
        self.assertFalse(get_mock.called)

    @responses.activate
    def test_oauth_backend_success(self):
        responses.add(
            responses.POST,
            settings.OCS_AUTHENTICATION['OAUTH_TOKEN_URL'],
            body=json.dumps({'access_token': 'test_access', 'refresh_token': 'test_refresh'}),
            status=200,
            content_type='application/json'
        )
        self.assertTrue(self.client.login(username='testuser', password='password'))
        u = User.objects.get(username='testuser')
        self.assertEqual(u.profile.access_token, 'test_access')
        self.assertEqual(u.profile.refresh_token, 'test_refresh')
        self.assertTrue(u.auth_token)

        # Test relog
        self.client.logout()
        self.assertTrue(self.client.login(username='testuser', password='password'))

    @responses.activate
    def test_oauth_backend_failure(self):
        responses.add(
            responses.POST,
            settings.OCS_AUTHENTICATION['OAUTH_TOKEN_URL'],
            body=json.dumps({'non_field_errors': 'Unable to log in with provided credentials'}),
            status=400,
            content_type='application/json'
        )
        self.assertFalse(self.client.login(username='testuser', password='password'))
        self.assertFalse(User.objects.filter(username='testuser').exists())

    @responses.activate
    def test_proposals(self):
        responses.add(
            responses.GET,
            settings.OCS_AUTHENTICATION['OAUTH_PROFILE_URL'],
            body=json.dumps({'proposals': [{'id': 'TestProposal'}]}),
            status=200,
            content_type='application/json'
        )
        self.assertIn('TestProposal', self.normal_user.profile.proposals)

    @responses.activate
    def test_proposals_bad_token(self):
        responses.add(
            responses.GET,
            settings.OCS_AUTHENTICATION['OAUTH_PROFILE_URL'],
            body=json.dumps({'error': 'Bad credentials'}),
            status=401,
            content_type='application/json'
        )
        self.assertFalse(self.normal_user.profile.proposals)

    @patch('requests.get')
    @patch('requests.post')
    def test_superuser_all_proposals(self, post_mock, get_mock):
        self.admin_user.backend = settings.AUTHENTICATION_BACKENDS[0]
        self.client.force_login(self.admin_user)
        FrameFactory.create(proposal_id='prop1')
        FrameFactory.create(proposal_id='prop2')
        self.assertCountEqual(['prop1', 'prop2'], self.admin_user.profile.proposals)
        self.assertFalse(get_mock.called)
