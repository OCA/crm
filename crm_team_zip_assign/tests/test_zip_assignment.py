# Copyright 2025 Binhex
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2.errors import UniqueViolation

from odoo.exceptions import ValidationError

from odoo.addons.base.tests.common import BaseCommon


class TestZipAssignment(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create countries and states

        cls.state_ny = cls.env.ref("base.state_us_27")  # New York
        cls.state_ca = cls.env.ref("base.state_us_5")  # California
        cls.country_us = cls.state_ny.country_id  # USA
        cls.state_on = cls.env.ref("base.state_ca_on")  # Ontario
        cls.country_ca = cls.state_on.country_id  # Canada

        # Create companies
        cls.company_a = cls.env["res.company"].create(
            {
                "name": "Company A",
                "country_id": cls.country_us.id,
            }
        )
        cls.company_b = cls.env["res.company"].create(
            {
                "name": "Company B",
                "country_id": cls.country_us.id,
            }
        )

        # Create CRM teams
        cls.team_north = cls.env["crm.team"].create(
            {
                "name": "North Team",
                "company_id": cls.company_a.id,
                "enable_zip_auto_assignment": True,
                "zip_assignment_priority": 10,  # Higher priority
                "country_ids": [(6, 0, [cls.country_us.id])],
                "state_ids": [(6, 0, [cls.state_ny.id])],
            }
        )

        cls.team_north_lesser_priority = cls.env["crm.team"].create(
            {
                "name": "North Team Lesser Priority",
                "company_id": cls.company_a.id,
                "enable_zip_auto_assignment": True,
                "zip_assignment_priority": 4,  # Lower priority
                "country_ids": [(6, 0, [cls.country_us.id])],
                "state_ids": [(6, 0, [cls.state_ny.id])],
            }
        )

        cls.team_south = cls.env["crm.team"].create(
            {
                "name": "South Team",
                "company_id": cls.company_a.id,
                "enable_zip_auto_assignment": True,
                "zip_assignment_priority": 5,
                "country_ids": [(6, 0, [cls.country_us.id])],
                "state_ids": [(6, 0, [cls.state_ca.id])],
            }
        )

        cls.team_company_b = cls.env["crm.team"].create(
            {
                "name": "Company B Team",
                "company_id": cls.company_b.id,
                "enable_zip_auto_assignment": True,
                "zip_assignment_priority": 1,
                "country_ids": [(6, 0, [cls.country_us.id])],
                "state_ids": [(6, 0, [cls.state_ny.id])],
            }
        )

        cls.team_inactive = cls.env["crm.team"].create(
            {
                "name": "Inactive Team",
                "company_id": cls.company_a.id,
                "enable_zip_auto_assignment": False,
                "zip_assignment_priority": 20,
                "country_ids": [(6, 0, [cls.country_us.id])],
                "state_ids": [(6, 0, [cls.state_ny.id])],
            }
        )

        cls.team_company = cls.env["crm.team"].create(
            {
                "name": "Team Company",
                "company_id": cls.company_a.id,
                "enable_zip_auto_assignment": True,
                "zip_assignment_priority": 10,
                "country_ids": [(6, 0, [cls.country_us.id])],
                "state_ids": [(6, 0, [cls.state_ny.id])],
                "pre_zip_match_condition": "[('is_company', '=', True)]",
            }
        )

        cls.team_person = cls.env["crm.team"].create(
            {
                "name": "Team Person",
                "company_id": cls.company_a.id,
                "enable_zip_auto_assignment": True,
                "zip_assignment_priority": 10,
                "country_ids": [(6, 0, [cls.country_us.id])],
                "state_ids": [(6, 0, [cls.state_ny.id])],
                "pre_zip_match_condition": "[('is_company', '=', False)]",
            }
        )

        # Create ZIP patterns
        cls.env["crm.team.zip.pattern"].create(
            [
                {
                    "team_id": cls.team_north.id,
                    "pattern": r"^1[0-5].*",  # ZIP starting with 10-15
                },
                {
                    "team_id": cls.team_north_lesser_priority.id,
                    "pattern": r"^1[0-5].*",  # Same pattern to test priority
                },
                {
                    "team_id": cls.team_south.id,
                    "pattern": r"^2[0-9].*",  # ZIP starting with 20-29
                },
                {
                    "team_id": cls.team_south.id,
                    "pattern": r"^1[6-9].*",  # ZIP starting with 16-19
                },
                {
                    "team_id": cls.team_company_b.id,
                    "pattern": r"^1[0-5].*",  # Same pattern as north team
                },
                {
                    "team_id": cls.team_inactive.id,
                    "pattern": r"^3[0-9].*",  # ZIP starting with 30-39
                },
                {
                    "team_id": cls.team_company.id,
                    "pattern": r"^9[6-8].*",  # ZIP starting with 96-98
                },
                {
                    "team_id": cls.team_person.id,
                    "pattern": r"^9[6-8].*",  # ZIP starting with 96-98
                },
            ]
        )

    def test_single_match(self):
        """Test partner assignment with single team match."""
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner North",
                "zip": "12345",
                "company_id": self.company_a.id,
                "country_id": self.country_us.id,
                "state_id": self.state_ny.id,
                "is_company": False,
            }
        )
        self.assertEqual(partner.team_id, self.team_north)

    def test_multiple_matches_priority(self):
        """Test priority when multiple teams match."""
        # Both teams have patterns for ZIP starting with 10-15
        # North team has higher priority (10 vs 4)
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner Priority",
                "zip": "15789",
                "company_id": self.company_a.id,
                "country_id": self.country_us.id,
                "state_id": self.state_ny.id,
                "is_company": False,
            }
        )
        self.assertEqual(partner.team_id, self.team_north)

    def test_no_match(self):
        """Test no assignment when no team matches."""
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner No Match",
                "zip": "99999",
                "company_id": self.company_a.id,
                "country_id": self.country_us.id,
                "state_id": self.state_ny.id,
                "is_company": False,
            }
        )
        self.assertFalse(partner.team_id)

    def test_exclusion_flag(self):
        """Test that excluded partners are not assigned."""
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner Excluded",
                "zip": "12345",
                "company_id": self.company_a.id,
                "country_id": self.country_us.id,
                "state_id": self.state_ny.id,
                "exclude_from_zip_assign": True,
                "is_company": False,
            }
        )
        self.assertFalse(partner.team_id)

    def test_multi_company(self):
        """Test multi-company isolation."""
        # Partner in company A should get team_north
        partner_a = self.env["res.partner"].create(
            {
                "name": "Test Partner Company A",
                "zip": "12345",
                "company_id": self.company_a.id,
                "country_id": self.country_us.id,
                "state_id": self.state_ny.id,
                "is_company": False,
            }
        )
        self.assertEqual(partner_a.team_id, self.team_north)

        # Partner in company B should get team_company_b
        partner_b = self.env["res.partner"].create(
            {
                "name": "Test Partner Company B",
                "zip": "12345",
                "company_id": self.company_b.id,
                "country_id": self.country_us.id,
                "state_id": self.state_ny.id,
                "is_company": False,
            }
        )
        self.assertEqual(partner_b.team_id, self.team_company_b)

    def test_inactive_team_ignored(self):
        """Test that inactive teams are ignored."""
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner Inactive",
                "zip": "30123",
                "company_id": self.company_a.id,
                "country_id": self.country_us.id,
                "state_id": self.state_ny.id,
                "is_company": False,
            }
        )
        self.assertFalse(partner.team_id)

    def test_invalid_regex(self):
        """Test that invalid regex patterns are prevented by constraints."""
        # Test constraint validation prevents invalid patterns
        with self.assertRaises(ValidationError):
            self.env["crm.team.zip.pattern"].create(
                {
                    "team_id": self.team_north.id,
                    "pattern": r"[invalid(regex",  # Invalid pattern
                }
            )

    def test_repeated_pattern_in_team(self):
        """Test unique team_id pattern combination in crm team."""
        with self.assertRaises(UniqueViolation):
            self.env["crm.team.zip.pattern"].create(
                {
                    "team_id": self.team_north.id,
                    "pattern": r"^1[0-5].*",  # ZIP starting with 10-15
                }
            )

    def test_enable_zip_auto_assignment_requires_company(self):
        """
        Test that enabling zip auto assignment without company
        raises ValidationError.
        """
        with self.assertRaises(ValidationError):
            self.env["crm.team"].create(
                {
                    "name": "No Company Team",
                    "enable_zip_auto_assignment": True,
                    "company_id": None,
                }
            )

    def test_geographic_filtering(self):
        """Test that geographic filtering works correctly."""
        # Partner in wrong state should not be assigned
        partner_wrong_state = self.env["res.partner"].create(
            {
                "name": "Test Partner Wrong State",
                "zip": "12345",
                "company_id": self.company_a.id,
                "country_id": self.country_us.id,
                "state_id": self.state_ca.id,  # California, but team_north is for NY
                "is_company": False,
            }
        )
        self.assertFalse(partner_wrong_state.team_id)

        # Partner in wrong country should not be assigned
        partner_wrong_country = self.env["res.partner"].create(
            {
                "name": "Test Partner Wrong Country",
                "zip": "12345",
                "company_id": self.company_a.id,
                "country_id": self.country_ca.id,  # Canada
                "state_id": self.state_on.id,
                "is_company": False,
            }
        )
        self.assertFalse(partner_wrong_country.team_id)

    def test_no_company_no_assignment(self):
        """Test that partners without company are not assigned."""
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner No Company",
                "zip": "12345",
                "country_id": self.country_us.id,
                "state_id": self.state_ny.id,
                "is_company": False,
            }
        )
        self.assertFalse(partner.team_id)

    def test_no_zip_no_assignment(self):
        """Test that partners without ZIP are not assigned."""
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner No ZIP",
                "company_id": self.company_a.id,
                "country_id": self.country_us.id,
                "state_id": self.state_ny.id,
                "is_company": False,
            }
        )
        self.assertFalse(partner.team_id)

    def test_no_country_no_assignment(self):
        """Test that partners without country are not assigned."""
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner No Country",
                "zip": "12345",
                "company_id": self.company_a.id,
                "country_id": False,
                "is_company": False,
            }
        )
        self.assertFalse(partner.team_id)

    def test_no_state_no_assignment(self):
        """Test that partners without state are not assigned."""
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner No State",
                "zip": "12345",
                "company_id": self.company_a.id,
                "country_id": self.country_us.id,
                "is_company": False,
            }
        )
        self.assertFalse(partner.team_id)

    def test_write_zip_triggers_assignment(self):
        """Test that changing ZIP triggers reassignment."""
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner Write",
                "zip": "99999",  # No match
                "company_id": self.company_a.id,
                "country_id": self.country_us.id,
                "state_id": self.state_ny.id,
                "is_company": False,
            }
        )
        self.assertFalse(partner.team_id)

        # Change ZIP to matching pattern
        partner.write({"zip": "12345"})
        self.assertEqual(partner.team_id, self.team_north)

    def test_write_company_triggers_assignment(self):
        """Test that changing company triggers reassignment."""
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner Write Company",
                "zip": "12345",
                "company_id": self.company_b.id,
                "country_id": self.country_us.id,
                "state_id": self.state_ny.id,
                "is_company": False,
            }
        )
        self.assertEqual(partner.team_id, self.team_company_b)

        # Change company
        partner.write({"company_id": self.company_a.id})
        self.assertEqual(partner.team_id, self.team_north)

    def test_write_exclusion_flag(self):
        """Test that changing exclusion flag works correctly."""
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner Exclusion",
                "zip": "12345",
                "company_id": self.company_a.id,
                "country_id": self.country_us.id,
                "state_id": self.state_ny.id,
                "is_company": False,
            }
        )
        self.assertEqual(partner.team_id, self.team_north)

        # Exclude from assignment
        partner.write({"exclude_from_zip_assign": True})
        # Team should remain (exclusion doesn't clear existing assignment)
        self.assertEqual(partner.team_id, self.team_north)

        # Include again
        partner.write({"exclude_from_zip_assign": False})
        # Should still be assigned to same team
        self.assertEqual(partner.team_id, self.team_north)

    def test_pre_zip_match_condition(self):
        """Test that pre_zip_match_condition filters partners as expected."""
        # Setup: two teams, same country/state/zip/priority,
        # different pre_zip_match_condition
        # Partner is a company
        partner_company = self.env["res.partner"].create(
            {
                "name": "Partner Company",
                "zip": "96765",
                "company_id": self.company_a.id,
                "country_id": self.country_us.id,
                "state_id": self.state_ny.id,
                "is_company": True,
            }
        )
        self.assertEqual(partner_company.team_id, self.team_company)

        # Partner is a person
        partner_person = self.env["res.partner"].create(
            {
                "name": "Partner Person",
                "zip": "96765",
                "company_id": self.company_a.id,
                "country_id": self.country_us.id,
                "state_id": self.state_ny.id,
                "is_company": False,
            }
        )
        self.assertEqual(partner_person.team_id, self.team_person)
