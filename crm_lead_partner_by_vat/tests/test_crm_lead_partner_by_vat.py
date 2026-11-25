# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import TransactionCase, tagged


# Partners are created here, so every module extending res.partner must be
# loaded already: at install time the registry only knows this module's
# dependencies, while the database columns of the other ones are there.
@tagged("post_install", "-at_install")
class TestCrmLeadPartnerByVat(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # ``no_vat_validation`` lets us store arbitrary VATs without the
        # base_vat format/country checks getting in the way.
        cls.partner = cls.env["res.partner"].with_context(no_vat_validation=True)
        cls.company = cls.partner.create(
            {"name": "Acme A/S", "is_company": True, "vat": "DK12345678"}
        )

    def _lead(self, **kw):
        return self.env["crm.lead"].create({"name": "Test Lead", "type": "lead", **kw})

    # -------------------------------------------------------------------- VAT
    def test_matched_by_vat(self):
        lead = self._lead(vat="DK12345678", email_from="whatever@acme.com")
        self.assertEqual(lead._find_matching_partner(), self.company)

    def test_vat_ignores_spaces_and_dots(self):
        for value in ("DK 123 456 78", "DK.123.456.78"):
            lead = self._lead(vat=value)
            self.assertEqual(lead._find_matching_partner(), self.company)

    def test_vat_stored_verbatim_is_matched(self):
        """The VAT is free text, so a lower-case one must be found as typed."""
        lowercase = self.partner.create(
            {"name": "Lower Co", "is_company": True, "vat": "dk99999999"}
        )
        lead = self._lead(vat="dk99999999")
        self.assertEqual(lead._find_company_by_vat(), lowercase)

    def test_vat_wildcards_never_match(self):
        for junk in ("%", "DK%", "DK______"):
            lead = self._lead(vat=junk)
            self.assertFalse(lead._find_company_by_vat())

    def test_person_with_the_vat_is_ignored(self):
        self.partner.create(
            {"name": "Sole Trader", "is_company": False, "vat": "DK55555555"}
        )
        lead = self._lead(vat="DK55555555")
        self.assertFalse(lead._find_company_by_vat())

    def test_oldest_company_wins(self):
        older = self.partner.create(
            {"name": "Old Co", "is_company": True, "vat": "DK77777777"}
        )
        self.partner.create({"name": "New Co", "is_company": True, "vat": "DK77777777"})
        lead = self._lead(vat="DK77777777")
        self.assertEqual(lead._find_company_by_vat(), older)

    # ----------------------------------------------------------- email fallback
    def test_falls_back_to_email_without_vat(self):
        """No VAT on the lead: keep the native email lookup."""
        contact = self.partner.create({"name": "Jane", "email": "jane@example.com"})
        lead = self._lead(email_from="jane@example.com")
        self.assertEqual(lead._find_matching_partner(), contact)

    def test_vat_takes_priority_over_email(self):
        """When both match, the VAT company wins over the email partner."""
        self.partner.create({"name": "Emailed", "email": "dup@example.com"})
        lead = self._lead(vat="DK12345678", email_from="dup@example.com")
        self.assertEqual(lead._find_matching_partner(), self.company)
