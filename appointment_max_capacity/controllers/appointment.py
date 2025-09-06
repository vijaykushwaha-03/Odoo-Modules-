# -*- coding: utf-8 -*-
# Copyright (C) Odoo custom Technologies.

import json
from odoo.http import request
from odoo.addons.appointment.controllers.appointment import AppointmentController

class CustomAppointmentController(AppointmentController):

    def _prepare_appointment_type_page_values(self, appointment_type, staff_user_id=False, resource_selected_id=False, **kwargs):
        result= super(CustomAppointmentController,self)._prepare_appointment_type_page_values(appointment_type, staff_user_id, resource_selected_id, **kwargs)
        
        filter_resource_ids = json.loads(kwargs.get('filter_resource_ids') or '[]')
        resources_possible = self._get_possible_resources(appointment_type, filter_resource_ids)
        resource_default = resource_selected = request.env['appointment.resource']

        if resources_possible:
            if resource_selected_id and resource_selected_id in resources_possible.ids and appointment_type.assign_method != 'time_resource':
                resource_selected = request.env['appointment.resource'].sudo().browse(resource_selected_id)
            elif appointment_type.assign_method == 'resource_time':
                resource_default = resources_possible[0]
        possible_combinations = (resource_selected or resource_default or resources_possible)._get_filtered_possible_capacity_combinations(1, {})
        max_capacity_possible = possible_combinations[-1][1] if possible_combinations else 1
        
        result['max_capacity'] = max_capacity_possible        
        return result    
        