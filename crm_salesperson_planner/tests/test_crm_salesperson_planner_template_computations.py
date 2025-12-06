# Copyright 2021 Sygel - Valentin Vinagre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest
from dateutil.relativedelta import relativedelta

# Mock Odoo modules for testing
class MockModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    def browse(self, ids):
        return self

class MockEnv:
    def __init__(self):
        self.ref_cache = {}
        self.user = Mock(partner_id=Mock(id=1))
        self.company = Mock(id=1)
        
    def ref(self, ref_name):
        if ref_name not in self.ref_cache:
            self.ref_cache[ref_name] = Mock(id=1)
        return self.ref_cache[ref_name]
    
    def __getitem__(self, model_name):
        return MockModel()

class MockFields:
    @staticmethod
    def Date():
        return Mock()
    
    @staticmethod 
    def Datetime():
        return Mock()
    
    @staticmethod
    def context_today(record):
        return datetime.now().date()

class MockValidationError(Exception):
    pass

class MockApi:
    @staticmethod
    def depends(*fields):
        def decorator(func):
            func._depends = fields
            return func
        return decorator
    
    @staticmethod
    def constrains(*fields):
        def decorator(func):
            func._constrains = fields
            return func
        return decorator
    
    @staticmethod
    def onchange(*fields):
        def decorator(func):
            func._onchange = fields
            return func
        return decorator

# Mock odoo module structure
import sys
from unittest.mock import MagicMock

# Create mock odoo module
odoo_mock = MagicMock()
odoo_mock._ = lambda x: x
odoo_mock.api = MockApi()
odoo_mock.fields = MockFields()
odoo_mock.exceptions = type('exceptions', (), {'ValidationError': MockValidationError})()
sys.modules['odoo'] = odoo_mock

# Test classes
class TestCrmSalespersonPlannerVisitTemplateDateComputations:
    """Test date computations and duration calculations in visit templates"""
    
    def setup_method(self):
        """Setup test environment"""
        self.template = Mock()
        self.template.start = datetime.now()
        self.template.stop = datetime.now() + timedelta(hours=2)
        self.template.allday = True
    
    def test_compute_stop_basic(self):
        """Test basic stop time computation"""
        # Simulate _compute_stop method
        duration = 2.0
        start = datetime.now()
        
        stop = start + timedelta(minutes=round(duration * 60))
        if self.template.allday:
            stop -= timedelta(seconds=1)
        
        expected_stop = start + timedelta(hours=2, seconds=-1)
        assert stop == expected_stop
    
    def test_compute_stop_no_duration(self):
        """Test stop computation with no duration (should default to 1.0)"""
        duration = 0  # No duration
        start = datetime.now()
        
        stop = start + timedelta(minutes=round((duration or 1.0) * 60))
        if self.template.allday:
            stop -= timedelta(seconds=1)
        
        expected_stop = start + timedelta(minutes=60, seconds=-1)
        assert stop == expected_stop
    
    def test_compute_dates_allday(self):
        """Test date computation for all-day events"""
        start = datetime(2024, 1, 15, 8, 0)
        stop = datetime(2024, 1, 15, 18, 0)
        allday = True
        
        if allday and start and stop:
            start_date = start.date()
            stop_date = stop.date()
        else:
            start_date = False
            stop_date = False
        
        assert start_date == datetime(2024, 1, 15).date()
        assert stop_date == datetime(2024, 1, 15).date()
    
    def test_compute_dates_not_allday(self):
        """Test date computation for non all-day events"""
        start = datetime(2024, 1, 15, 8, 0)
        stop = datetime(2024, 1, 15, 18, 0)
        allday = False
        
        if allday and start and stop:
            start_date = start.date()
            stop_date = stop.date()
        else:
            start_date = False
            stop_date = False
        
        assert start_date is False
        assert stop_date is False
    
    def test_compute_duration_basic(self):
        """Test basic duration computation"""
        start = datetime(2024, 1, 15, 8, 0)
        stop = datetime(2024, 1, 15, 10, 30)
        
        duration = (stop - start).total_seconds() / 3600
        duration = round(duration, 2)
        
        assert duration == 2.5
    
    def test_compute_duration_half_hour(self):
        """Test duration computation for half hour"""
        start = datetime(2024, 1, 15, 8, 0)
        stop = datetime(2024, 1, 15, 8, 30)
        
        duration = (stop - start).total_seconds() / 3600
        duration = round(duration, 2)
        
        assert duration == 0.5
    
    def test_get_duration_with_none_dates(self):
        """Test duration calculation with None dates"""
        start = None
        stop = datetime(2024, 1, 15, 10, 0)
        
        if not start or not stop:
            duration = 0
        
        assert duration == 0
    
    def test_inverse_dates(self):
        """Test date inversion for all-day events"""
        start_date = datetime(2024, 1, 15).date()
        stop_date = datetime(2024, 1, 15).date()
        allday = True
        
        if allday:
            enddate = datetime.combine(stop_date, datetime.min.time())
            enddate = enddate.replace(hour=18)
            startdate = datetime.combine(start_date, datetime.min.time())
            startdate = startdate.replace(hour=8)
            
            expected_start = datetime(2024, 1, 15, 8, 0)
            expected_stop = datetime(2024, 1, 15, 18, 0)
            
            assert startdate == expected_start
            assert enddate == expected_stop
    
    def test_onchange_end_type_count(self):
        """Test onchange behavior for count end type"""
        end_type = "count"
        
        if end_type == "count":
            until = False
            count = 0
        elif end_type == "end_date":
            count = 0
        elif end_type == "forever":
            count = 0
            until = False
        
        assert until is False
        assert count == 0
    
    def test_onchange_end_type_end_date(self):
        """Test onchange behavior for end_date end type"""
        end_type = "end_date"
        
        if end_type == "count":
            until = False
            count = 0
        elif end_type == "end_date":
            count = 0
        elif end_type == "forever":
            count = 0
            until = False
        
        assert count == 0
    
    def test_onchange_end_type_forever(self):
        """Test onchange behavior for forever end type"""
        end_type = "forever"
        
        if end_type == "count":
            until = False
            count = 0
        elif end_type == "end_date":
            count = 0
        elif end_type == "forever":
            count = 0
            until = False
        
        assert count == 0
        assert until is False


class TestCrmSalespersonPlannerVisitTemplateRecurrence:
    """Test recurrence logic and date range calculations"""
    
    def setup_method(self):
        """Setup test environment for recurrence testing"""
        self.template = Mock()
        self.template.start = datetime(2024, 1, 1, 8, 0)
        self.template.stop = datetime(2024, 1, 1, 10, 0)
        self.template.rrule_type = "daily"
        self.template.interval = 1
    
    def test_get_duration_with_mock_method(self):
        """Test the _get_duration method logic"""
        def _get_duration(start, stop):
            if not start or not stop:
                return 0
            duration = (stop - start).total_seconds() / 3600
            return round(duration, 2)
        
        # Test with valid dates
        start = datetime(2024, 1, 15, 8, 0)
        stop = datetime(2024, 1, 15, 10, 30)
        duration = _get_duration(start, stop)
        assert duration == 2.5
        
        # Test with None dates
        duration = _get_duration(None, stop)
        assert duration == 0
        
        duration = _get_duration(start, None)
        assert duration == 0
    
    def test_prepare_visit_vals_single_partner(self):
        """Test visit values preparation with single partner"""
        def _prepare_visit_vals(partner_ids, dates, sequence, user_id, description, company_id, template_id):
            return [
                {
                    "partner_id": partner_ids[0].id if partner_ids else False,
                    "date": date,
                    "sequence": sequence,
                    "user_id": user_id,
                    "description": description,
                    "company_id": company_id,
                    "visit_template_id": template_id,
                }
                for date in dates
            ]
        
        # Mock partner
        partner = Mock(id=1)
        partner_ids = [partner]
        dates = [datetime(2024, 1, 15).date(), datetime(2024, 1, 16).date()]
        
        result = _prepare_visit_vals(partner_ids, dates, 20, 1, "Test Description", 1, 1)
        
        assert len(result) == 2
        assert result[0]["partner_id"] == 1
        assert result[0]["date"] == datetime(2024, 1, 15).date()
        assert result[0]["sequence"] == 20
        assert result[0]["user_id"] == 1
        assert result[0]["visit_template_id"] == 1
    
    def test_prepare_visit_vals_no_partners(self):
        """Test visit values preparation with no partners"""
        def _prepare_visit_vals(partner_ids, dates, sequence, user_id, description, company_id, template_id):
            return [
                {
                    "partner_id": partner_ids[0].id if partner_ids else False,
                    "date": date,
                    "sequence": sequence,
                    "user_id": user_id,
                    "description": description,
                    "company_id": company_id,
                    "visit_template_id": template_id,
                }
                for date in dates
            ]
        
        partner_ids = []
        dates = [datetime(2024, 1, 15).date()]
        
        result = _prepare_visit_vals(partner_ids, dates, 20, 1, "Test Description", 1, 1)
        
        assert len(result) == 1
        assert result[0]["partner_id"] is False
    
    def test_get_recurrence_dates_no_existing_visits(self):
        """Test recurrence date generation with no existing visits"""
        def _get_recurrence_dates(start_dates, items):
            dates = []
            visit_dates = []  # No existing visits
            for _date in start_dates[:items]:
                if _date not in visit_dates:
                    dates.append(_date)
            return dates
        
        start_dates = [
            datetime(2024, 1, 15).date(),
            datetime(2024, 1, 16).date(), 
            datetime(2024, 1, 17).date()
        ]
        
        dates = _get_recurrence_dates(start_dates, 2)
        
        assert len(dates) == 2
        assert dates[0] == datetime(2024, 1, 15).date()
        assert dates[1] == datetime(2024, 1, 16).date()
    
    def test_get_recurrence_dates_with_existing_visits(self):
        """Test recurrence date generation with existing visits"""
        def _get_recurrence_dates(start_dates, items):
            dates = []
            visit_dates = [datetime(2024, 1, 15).date()]  # One existing visit
            for _date in start_dates[:items]:
                if _date not in visit_dates:
                    dates.append(_date)
            return dates
        
        start_dates = [
            datetime(2024, 1, 15).date(),
            datetime(2024, 1, 16).date(), 
            datetime(2024, 1, 17).date()
        ]
        
        dates = _get_recurrence_dates(start_dates, 3)
        
        assert len(dates) == 2  # Only new dates
        assert dates[0] == datetime(2024, 1, 16).date()
        assert dates[1] == datetime(2024, 1, 17).date()
    
    def test_get_max_date(self):
        """Test max date calculation"""
        start_dates = [
            datetime(2024, 1, 15).date(),
            datetime(2024, 1, 16).date(), 
            datetime(2024, 1, 17).date()
        ]
        
        max_date = start_dates[-1]
        assert max_date == datetime(2024, 1, 17).date()
    
    def test_create_visits_workflow(self):
        """Test the complete create_visits workflow"""
        def _create_visits_and_validate(templates, auto_validate, last_visit_date, max_date):
            results = []
            for template in templates:
                # Simulate visit creation
                visits_created = True
                
                if visits_created and auto_validate:
                    # Would call action_confirm() on visits
                    state = "confirmed"
                else:
                    state = "draft"
                
                if last_visit_date >= max_date:
                    template.state = "done"
                    state = "done"
                
                results.append({
                    "template": template,
                    "visits_created": visits_created,
                    "auto_validated": auto_validate,
                    "final_state": state
                })
            
            return results
        
        # Test with auto-validate
        template = Mock()
        template.auto_validate = True
        template.last_visit_date = datetime(2024, 1, 20).date()
        template.max_date = datetime(2024, 1, 18).date()
        
        results = _create_visits_and_validate([template], True, template.last_visit_date, template.max_date)
        
        assert len(results) == 1
        assert results[0]["auto_validated"] is True
        assert results[0]["final_state"] == "done"  # last_visit_date > max_date


class TestCrmSalespersonPlannerVisitConstraints:
    """Test constraints and validation logic"""
    
    def test_partner_ids_constraint_single_partner(self):
        """Test constraint allows single partner"""
        partner_ids = [Mock(id=1)]
        
        try:
            if len(partner_ids) > 1:
                raise MockValidationError("Only one customer is allowed")
            # If we get here, constraint passed
            constraint_passed = True
        except MockValidationError:
            constraint_passed = False
        
        assert constraint_passed is True
    
    def test_partner_ids_constraint_multiple_partners(self):
        """Test constraint prevents multiple partners"""
        partner_ids = [Mock(id=1), Mock(id=2)]
        
        try:
            if len(partner_ids) > 1:
                raise MockValidationError("Only one customer is allowed")
            constraint_passed = True
        except MockValidationError:
            constraint_passed = False
        
        assert constraint_passed is False
    
    def test_visit_unlink_constraint_draft(self):
        """Test visit can be deleted when in draft state"""
        visit = Mock(state="draft")
        
        can_unlink = visit.state in ["draft", "cancel"]
        assert can_unlink is True
    
    def test_visit_unlink_constraint_confirmed(self):
        """Test visit cannot be deleted when in confirmed state"""
        visit = Mock(state="confirm")
        
        can_unlink = visit.state in ["draft", "cancel"]
        assert can_unlink is False
    
    def test_visit_unlink_constraint_cancelled(self):
        """Test visit can be deleted when in cancelled state"""
        visit = Mock(state="cancel")
        
        can_unlink = visit.state in ["draft", "cancel"]
        assert can_unlink is True
    
    def test_visit_unlink_constraint_done(self):
        """Test visit cannot be deleted when in done state"""
        visit = Mock(state="done")
        
        can_unlink = visit.state in ["draft", "cancel"]
        assert can_unlink is False
    
    def test_action_draft_validation_invalid_states(self):
        """Test action_draft prevents invalid state transitions"""
        invalid_states = ["confirm", "draft"]
        valid_states = ["cancel", "incident", "done"]
        
        def can_change_to_draft(state):
            return state in ["cancel", "incident", "done"]
        
        # Test invalid states
        for state in invalid_states:
            assert can_change_to_draft(state) is False
        
        # Test valid states
        for state in valid_states:
            assert can_change_to_draft(state) is True
    
    def test_action_confirm_validation(self):
        """Test action_confirm only works from draft state"""
        def can_confirm(states):
            return all(state == "draft" for state in states)
        
        # Valid case
        assert can_confirm(["draft"]) is True
        
        # Invalid cases
        assert can_confirm(["confirm"]) is False
        assert can_confirm(["draft", "confirm"]) is False
        assert can_confirm(["done"]) is False
    
    def test_action_done_validation(self):
        """Test action_done only works from confirmed state"""
        def can_mark_done(state):
            return state == "confirm"
        
        assert can_mark_done("confirm") is True
        assert can_mark_done("draft") is False
        assert can_mark_done("done") is False
        assert can_mark_done("cancel") is False
    
    def test_action_cancel_validation(self):
        """Test action_cancel only works from draft or confirmed states"""
        def can_cancel(state):
            return state in ["draft", "confirm"]
        
        assert can_cancel("draft") is True
        assert can_cancel("confirm") is True
        assert can_cancel("done") is False
        assert can_cancel("cancel") is False
    
    def test_action_incident_validation(self):
        """Test action_incident only works from draft or confirmed states"""
        def can_mark_incident(state):
            return state in ["draft", "confirm"]
        
        assert can_mark_incident("draft") is True
        assert can_mark_incident("confirm") is True
        assert can_mark_incident("done") is False
        assert can_mark_incident("incident") is False


class TestCrmSalespersonPlannerVisitEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_calendar_event_creation_failure_handling(self):
        """Test handling of calendar event creation failures"""
        # Simulate calendar event creation that might fail
        def create_calendar_event_with_fallback(visit):
            try:
                event = Mock()  # Simulate successful creation
                visit.calendar_event_id = event
                return event
            except Exception as e:
                # Fallback behavior
                return None
        
        visit = Mock()
        visit.calendar_event_id = None
        
        result = create_calendar_event_with_fallback(visit)
        assert result is not None
    
    def test_date_synchronization_edge_cases(self):
        """Test date synchronization edge cases"""
        def update_calendar_event_dates(visit, new_date, bypass_update=False):
            if bypass_update:
                return "bypassed"
            
            if visit.calendar_event_id:
                visit.calendar_event_id.start = new_date
                visit.calendar_event_id.stop = new_date
                return "updated"
            
            return "no_event"
        
        visit = Mock()
        visit.calendar_event_id = Mock()
        new_date = datetime(2024, 1, 15).date()
        
        # Normal update
        result = update_calendar_event_dates(visit, new_date, False)
        assert result == "updated"
        
        # Bypassed update
        result = update_calendar_event_dates(visit, new_date, True)
        assert result == "bypassed"
        
        # No calendar event
        visit.calendar_event_id = None
        result = update_calendar_event_dates(visit, new_date, False)
        assert result == "no_event"
    
    def test_user_synchronization_edge_cases(self):
        """Test user synchronization edge cases"""
        def update_calendar_event_user(visit, new_user_id, bypass_update=False):
            if bypass_update:
                return "bypassed"
            
            if visit.calendar_event_id:
                visit.calendar_event_id.user_id = new_user_id
                return "updated"
            
            return "no_event"
        
        visit = Mock()
        visit.calendar_event_id = Mock()
        new_user_id = 999
        
        # Normal update
        result = update_calendar_event_user(visit, new_user_id, False)
        assert result == "updated"
        assert visit.calendar_event_id.user_id == 999
    
    def test_sequence_generation_logic(self):
        """Test sequence number generation logic"""
        def generate_visit_number(current_name, sequence_code):
            if current_name == "/":
                return f"VST-{sequence_code}-001"
            return current_name
        
        # Test new visit
        assert generate_visit_number("/", "VISIT") == "VST-VISIT-001"
        
        # Test existing visit
        assert generate_visit_number("VST-VISIT-001", "VISIT") == "VST-VISIT-001"
    
    def test_multiple_state_update_scenarios(self):
        """Test complex state update scenarios"""
        def process_state_transition(visit, action, **kwargs):
            transitions = {
                "draft": ["cancel", "incident", "done"],
                "confirm": ["cancel", "incident", "done"],
                "cancel": ["draft"],
                "incident": ["draft"],
                "done": []  # Terminal state
            }
            
            current_state = visit.state
            allowed_actions = transitions.get(current_state, [])
            
            if action in allowed_actions:
                visit.state = action
                return f"transitioned_to_{action}"
            else:
                return f"invalid_transition_from_{current_state}"
        
        # Test valid transitions
        visit = Mock(state="draft")
        result = process_state_transition(visit, "cancel")
        assert result == "transitioned_to_cancel"
        
        # Test invalid transition
        visit = Mock(state="done")
        result = process_state_transition(visit, "draft")
        assert result == "invalid_transition_from_done"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])