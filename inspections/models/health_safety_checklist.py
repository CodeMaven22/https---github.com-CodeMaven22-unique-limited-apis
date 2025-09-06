from django.db import models
from inspections.models.base import BaseInspection

class HealthSafetyChecklist(models.Model):
    inspection = models.ForeignKey(BaseInspection, on_delete=models.CASCADE, related_name='health_safety_checklists' )
    
    # Policy and Training Section
    previous_concerns_addressed = models.BooleanField(
        default=False,
        help_text="Have previous health and safety concerns been addressed?"
    )
    policy_up_to_date_local_health_safety = models.BooleanField(
        default=False,
        help_text="Is the local health and safety policy up to date?"
    )
    staff_issued_personal_copy_policy_told_text = models.BooleanField(
        default=False,
        help_text="Have staff been issued with personal copies of the policy?"
    )
    health_safety_standing_item_agenda_previous_staff_meeting = models.BooleanField(
        default=False,
        verbose_name="Health & Safety on Staff Meeting Agenda",
        help_text="Has health & safety been a standing item on staff meeting agendas?"
    )
    all_staff_received_training_health_safety_procedures = models.BooleanField(
        default=False,
        help_text="Have all staff received training on health & safety procedures?"
    )
    new_staff_receive_training_beginning_employment = models.BooleanField(
        default=False,
        help_text="Do new staff receive training at the beginning of employment?"
    )
    temporary_staff_receive_necessary_training = models.BooleanField(
        default=False,
        help_text="Do temporary staff receive necessary health & safety training?"
    )

    # Risk Assessments Section
    staff_carry_out_manual_handling_risk_assessment = models.BooleanField(
        default=False,
        help_text="Do staff carry out manual handling risk assessments?"
    )
    equipment_used_mobility_risk_assessment = models.BooleanField(
        default=False,
        help_text="Is there a risk assessment for equipment used for mobility?"
    )
    computer_workstation_assessments_carried_out_recorded = models.BooleanField(
        default=False,
        help_text="Have computer workstation assessments been carried out and recorded?"
    )

    # Physical Environment Section
    working_conditions_suitable_noise_lighting_ventilation_temperature = models.BooleanField(
        default=False,
        verbose_name="Suitable Working Conditions",
        help_text="Are working conditions suitable (noise, lighting, ventilation, temperature)?"
    )
    furniture_furnishings_good_condition_suitable_stable = models.BooleanField(
        default=False,
        verbose_name="Furniture Condition",
        help_text="Is furniture in good condition, suitable and stable?"
    )
    equipment_suitable_maintained_good_condition = models.BooleanField(
        default=False,
        verbose_name="Equipment Condition",
        help_text="Is equipment suitable and maintained in good condition?"
    )
    floor_surfaces_acceptable_condition = models.BooleanField(
        default=False,
        help_text="Are floor surfaces in acceptable condition?"
    )

    # Fire Safety Section
    fire_doors_kept_closed = models.BooleanField(
        default=False,
        help_text="Are fire doors kept closed?"
    )
    notices_informing_staff_what_to_do_fire = models.BooleanField(
        default=False,
        verbose_name="Fire Procedure Notices",
        help_text="Are there notices informing staff what to do in case of fire?"
    )
    staff_know_what_to_do_event_fire = models.BooleanField(
        default=False,
        verbose_name="Staff Fire Procedure Knowledge",
        help_text="Do staff know what to do in the event of a fire?"
    )

    # First Aid Section
    adequate_first_aiders_available = models.BooleanField(
        default=False,
        help_text="Are there adequate first aiders available?"
    )
    easy_to_find_first_aiders = models.BooleanField(
        default=False,
        help_text="Is it easy to identify/find first aiders?"
    )

    # Electrical Safety Section
    electricity_obvious_defects_electrical_equipment = models.BooleanField(
        default=False,
        verbose_name="Electrical Equipment Defects",
        help_text="Are there any obvious defects in electrical equipment?"
    )
    sockets_overloaded = models.BooleanField(
        default=False,
        help_text="Are any electrical sockets overloaded?"
    )
    all_electrical_equipment_inspected = models.BooleanField(
        default=False,
        help_text="Has all electrical equipment been inspected?"
    )

    # General Safety
    circulation_routes_kept_clear_obstructions_wires_cables_boxes = models.BooleanField(
        default=False,
        verbose_name="Clear Circulation Routes",
        help_text="Are circulation routes kept clear of obstructions?"
    )
    harmful_substances_in_use_precautions_agreed = models.TextField(
        blank=True,
        null=True,
        help_text="Details about harmful substances in use and precautions"
    )
    comments = models.TextField(
        blank=True,
        null=True,
        help_text="Any additional comments about the health and safety inspection"
    )
    is_active = models.BooleanField(default=True, help_text="Is this checklist active?")

    def __str__(self):
        return f"Health & Safety Checklist - {self.inspection.location or 'Unknown Location'}"

    class Meta:
        verbose_name = "Health & Safety Checklist"
        verbose_name_plural = "Health & Safety Checklists"