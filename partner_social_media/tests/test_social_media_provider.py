from odoo.tests.common import TransactionCase


class TestSocialMediaProvider(TransactionCase):
    def setUp(self):
        super().setUp()
        self.social_media_provider = self.env[
            "res.partner.social.media.provider"
        ].create(
            {
                "name": "Test Social Media Provider",
                "url_format": "https://www.example.com/%s",
                "font_awesome": "fa-test",
            }
        )
        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )

    def test_social_media_provider_url(self):
        social_media_id = self.env["res.partner.social.media"].create(
            {
                "partner_id": self.partner.id,
                "provider_id": self.social_media_provider.id,
                "account": "test123",
            }
        )

        self.assertEqual(
            social_media_id.website,
            "https://www.example.com/test123",
        )

        social_media_id.account = "test456"

        self.assertEqual(
            social_media_id.website,
            "https://www.example.com/test456",
        )

        social_media_id.account = False

        self.assertFalse(
            social_media_id.website,
        )

    def test_social_media_provider_link(self):
        social_media_id = self.env["res.partner.social.media"].create(
            {
                "partner_id": self.partner.id,
                "provider_id": self.social_media_provider.id,
                "account": "test123",
            }
        )

        self.assertEqual(
            social_media_id.link,
            '<a href="https://www.example.com/test123" target="_blank"><i'
            ' class="fa-test"></i> test123</a>',
        )

        social_media_id.account = "test456"

        self.assertEqual(
            social_media_id.link,
            '<a href="https://www.example.com/test456" target="_blank"><i'
            ' class="fa-test"></i> test456</a>',
        )

        social_media_id.account = False

        self.assertFalse(
            social_media_id.link,
        )
