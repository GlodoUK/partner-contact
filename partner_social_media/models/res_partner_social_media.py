from odoo import api, fields, models


class ResPartnerSocialMediaProvider(models.Model):
    _name = "res.partner.social.media.provider"
    _description = "Social Media Type"
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one("res.partner", required=True, index=True)
    font_awesome = fields.Char()
    url_format = fields.Char()

    def _get_website_and_link_for_account(self, account):
        self.ensure_one()

        if not self.url_format or not account:
            return (False, False)

        url = self.url_format % (account,)

        link = '<a href="%s" target="_blank"><i class="%s"></i> %s</a>' % (
            url,
            self.font_awesome,
            account,
        )

        return (
            url,
            link,
        )


class ResPartnerSocialMedia(models.Model):
    _name = "res.partner.social.media"
    _description = "Partner Social Media"

    partner_id = fields.Many2one("res.partner", required=True)
    provider_id = fields.Many2one(
        "res.partner.social.media.provider",
        required=True,
    )
    image_128 = fields.Binary(related="provider_id.image_128")
    image_256 = fields.Binary(related="provider_id.image_256")
    image_512 = fields.Binary(related="provider_id.image_512")
    image_1024 = fields.Binary(related="provider_id.image_1024")
    image_1920 = fields.Binary(related="provider_id.image_1920")
    account = fields.Char()
    website = fields.Char(compute="_compute_website")
    link = fields.Html(compute="_compute_website")

    @api.depends("account", "provider_id")
    def _compute_website(self):
        for record in self:
            if not record.provider_id:
                record.website = False
                record.link = False
                continue

            website, link = record.provider_id._get_website_and_link_for_account(
                record.account
            )

            record.website = website
            record.link = link
