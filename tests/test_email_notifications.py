from django.test import TestCase
from unittest import mock
from integrations.notifications.email_notification import EmailNotification, EmailNotificationService


class EmailNotificationServiceTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'to': ['test@example.com'],
            'subject': 'Test Subject',
            'body': 'Test Body',
            'template_html': 'test_template.html',
            'context': {'key': 'value'}
        }

    def test_initialization_with_valid_data(self):
        service = EmailNotificationService(**self.valid_data)
        self.assertEqual(service.to, self.valid_data['to'])
        self.assertEqual(service.subject, self.valid_data['subject'])
        self.assertEqual(service.body, self.valid_data['body'])
        self.assertEqual(service.template_html, self.valid_data['template_html'])
        self.assertEqual(service.context, self.valid_data['context'])

    def test_initialization_without_recipient(self):
        data = self.valid_data.copy()
        data['to'] = []
        with self.assertRaises(ValueError):
            EmailNotificationService(**data)

    def test_initialization_without_subject(self):
        data = self.valid_data.copy()
        data['subject'] = ''
        with self.assertRaises(ValueError):
            EmailNotificationService(**data)

    def test_initialization_without_body(self):
        data = self.valid_data.copy()
        data['body'] = ''
        with self.assertRaises(ValueError):
            EmailNotificationService(**data)


class EmailNotificationTests(TestCase):
    @mock.patch('integrations.notifications.email_notification.EmailNotificationService')
    def test_send_welcome_email(self, mock_email_service):
        data = {
            'email': 'test@example.com',
            'first_name': 'John'
        }
        EmailNotification.send_welcome_email(data)

        mock_email_service.assert_called_once_with(
            to=['test@example.com'],
            subject='Welcome',
            body='Welcome To our platform',
            template_html='email_verify.html',
            context={'firstName': 'John'}
        )
        mock_email_service.return_value.send_email.assert_called_once()
