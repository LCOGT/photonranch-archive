from archive.frames.tests.factories import FrameFactory, VersionFactory
from unittest.mock import MagicMock
import boto3
from django.core.urlresolvers import reverse
from django.test import TestCase
import json
import os
import random


class TestFrameGet(TestCase):
    def setUp(self):
        boto3.client = MagicMock()
        self.frames = FrameFactory.create_batch(5)
        self.frame = self.frames[0]

    def test_get_frame(self):
        response = self.client.get(reverse('frame-detail', args=(self.frame.id, )))
        self.assertEqual(response.json()['filename'], self.frame.filename)

    def test_get_frame_list(self):
        response = self.client.get(reverse('frame-list'))
        self.assertEqual(response.json()['count'], 5)
        self.assertContains(response, self.frame.filename)

    def test_get_frame_list_filter(self):
        response = self.client.get(
            '{0}?filename={1}'.format(reverse('frame-list'), self.frame.filename)
        )
        self.assertEqual(response.json()['count'], 1)
        self.assertContains(response, self.frame.filename)

    def test_filter_area(self):
        frame = FrameFactory.create(
            area='POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))'
        )
        response = self.client.get(
            '{0}?covers=POINT(5 5)'.format(reverse('frame-list'))
        )
        self.assertContains(response, frame.filename)
        response = self.client.get(
            '{0}?covers=POINT(20 20)'.format(reverse('frame-list'))
        )
        self.assertNotContains(response, frame.filename)

    def test_filer_area_wrap_0RA(self):
        frame = FrameFactory.create(
            area='POLYGON((350 -10, 350 10, 10 10, 10 -10, 350 -10))'
        )
        response = self.client.get(
            '{0}?covers=POINT(0 0)'.format(reverse('frame-list'))
        )
        self.assertContains(response, frame.filename)
        response = self.client.get(
            '{0}?covers=POINT(340 0)'.format(reverse('frame-list'))
        )
        self.assertNotContains(response, frame.filename)


class TestFramePost(TestCase):
    def setUp(self):
        boto3.client = MagicMock()
        self.header_json = json.load(open(os.path.join(os.path.dirname(__file__), 'frames.json')))
        f = self.header_json[random.choice(list(self.header_json.keys()))]
        f['filename'] = FrameFactory.filename.fuzz()
        f['area'] = FrameFactory.area.fuzz()
        f['version_set'] = [
            {'md5': VersionFactory.md5.fuzz(), 'key': VersionFactory.key.fuzz()}
        ]
        self.single_frame_payload = f

    def test_post_frame(self):
        total_frames = len(self.header_json)
        for extension in self.header_json:
            frame_payload = self.header_json[extension]
            frame_payload['filename'] = FrameFactory.filename.fuzz()
            frame_payload['area'] = FrameFactory.area.fuzz()
            frame_payload['version_set'] = [
                {'md5': VersionFactory.md5.fuzz(), 'key': VersionFactory.key.fuzz()}
            ]
            response = self.client.post(
                reverse('frame-list'), json.dumps(frame_payload), content_type='application/json'
            )
            self.assertContains(response, frame_payload['filename'], status_code=201)
        response = self.client.get(reverse('frame-list'))
        self.assertEqual(response.json()['count'], total_frames)

    def test_post_missing_data(self):
        frame_payload = self.single_frame_payload
        del frame_payload['filename']
        response = self.client.post(
            reverse('frame-list'), json.dumps(frame_payload), content_type='application/json'
        )
        self.assertEqual(response.json()['filename'], ['This field is required.'])
        self.assertEqual(response.status_code, 400)

    def test_post_duplicate_data(self):
        frame = FrameFactory()
        version = frame.version_set.all()[0]
        frame_payload = self.single_frame_payload
        frame_payload['version_set'] = [{'md5': version.md5, 'key': 'random_key'}]
        response = self.client.post(
            reverse('frame-list'), json.dumps(frame_payload), content_type='application/json'
        )
        self.assertEqual(response.json()['version_set'], [{'md5': ['Version with this md5 already exists.']}])
        self.assertEqual(response.status_code, 400)
