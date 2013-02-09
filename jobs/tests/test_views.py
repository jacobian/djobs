from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings

from ..models import JobListing, Flag
from ..views import PublishJob, ArchiveJob

class ListingTestCase(TestCase):
    fixtures = ['test_views.json']

    def test_display_listings(self):
        user2 = User.objects.create_user('test', 'test@example.com', 'test')
        JobListing.objects.create(creator=user2, title='test', status='active',
            description='test')

        self.client.login(username='apollo13', password='secret')
        response = self.client.get('/mine/')
        data = ['<JobListing: draft post>', '<JobListing: super position>']
        self.assertQuerysetEqual(response.context['jobs'], data)

        response = self.client.get('/')
        data = ['<JobListing: test>', '<JobListing: draft post>',
                '<JobListing: super position>']
        self.assertQuerysetEqual(response.context['jobs'], data)

        # Testuser shouldn't see drafts by apollo13
        self.client.login(username='test', password='test')
        response = self.client.get('/')
        data = ['<JobListing: test>', '<JobListing: super position>']
        self.assertQuerysetEqual(response.context['jobs'], data)

    def test_feed(self):
        response = self.client.get('/feed/')
        self.assertContains(response, 'super position')
        self.assertNotContains(response, 'draft post')


class JobManagementTestCase(TestCase):
    fixtures = ['test_views.json']

    def setUp(self):
        self.client.login(username='apollo13', password='secret')
        self.listing = JobListing.objects.get(pk=1)

    def test_archive(self):
        response = self.client.post('/%d/archive/' % self.listing.pk, follow=True)
        self.assertContains(response, ArchiveJob.success_message)
        listing = JobListing.objects.get(pk=self.listing.pk)
        self.assertEqual(listing.status, 'archived')

    def test_publish(self):
        self.listing.status = 'draft'
        self.listing.save()
        response = self.client.post('/%d/publish/' % self.listing.pk, follow=True)
        self.assertContains(response, PublishJob.success_message)
        listing = JobListing.objects.get(pk=self.listing.pk)
        self.assertEqual(listing.status, 'active')


class FlagTestCase(TestCase):
    fixtures = ['test_views.json']

    def setUp(self):
        User.objects.filter(username='apollo13').update(is_superuser=True)
        self.listing = JobListing.objects.get(pk=1)

    def test_flagging(self):
        self.assertEqual(Flag.objects.count(), 0)
        response = self.client.post('/%d/flag/' % self.listing.pk)
        self.assertEqual(Flag.objects.count(), 1)
        self.assertRedirects(response, '/%d/' % self.listing.pk)

        # Verify that reflagging doesn't work
        response = self.client.post('/%d/flag/' % self.listing.pk)
        self.assertEqual(Flag.objects.count(), 1)

    def test_review_invalid_perms(self):
        User.objects.create_user('invalid', 'invalid', 'invalid')
        response = self.client.get('/flags/')
        self.assertRedirects(response, '/login/?next=/flags/')
        s = self.client.login(username='invalid', password='invalid')
        self.assertTrue(s)
        response = self.client.get('/flags/')
        self.assertRedirects(response, '/login/?next=/flags/')

    def test_review_get(self):
        self.client.login(username='apollo13', password='secret')

        response = self.client.get('/flags/')
        self.assertContains(response, 'No flags to review - good job!')

        self.listing.flags.create()
        response = self.client.get('/flags/')
        self.assertContains(response, 'Kill')
        self.assertContains(response, 'Keep')

    def test_review_post(self):
        self.client.login(username='apollo13', password='secret')

        self.listing.flags.create()
        data = {'job_id': self.listing.pk, 'action': 'keep'}
        response = self.client.post('/flags/', data, follow=True)
        self.assertContains(response, "&#39;%s&#39; kept." % self.listing)
        self.assertFalse(Flag.objects.filter(cleared=False).exists())

        self.listing.flags.create()
        data = {'job_id': self.listing.pk, 'action': 'kill'}
        response = self.client.post('/flags/', data, follow=True)
        self.assertContains(response, "&#39;%s&#39; removed." % self.listing)
        self.assertFalse(Flag.objects.filter(cleared=False).exists())
        listing = JobListing.objects.get(pk=self.listing.pk)
        self.assertEqual(listing.status, JobListing.STATUS_REMOVED)

    def test_review_invalid_data(self):
        self.client.login(username='apollo13', password='secret')
        data = {'job_id': -1}
        response = self.client.post('/flags/', data, follow=True)
        self.assertRedirects(response, '/flags/')
        self.assertEqual(len(response.context['messages']), 0)
