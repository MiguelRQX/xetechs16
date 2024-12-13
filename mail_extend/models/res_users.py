# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import _, api, fields, models, modules, tools
from odoo.addons.base.models.res_users import is_selection_groups


class Users(models.Model):
    """ Update of res.users class
        - add a preference about sending emails about notifications
        - make a new user follow itself
        - add a welcome message
        - add suggestion preference
        - if adding groups to a user, check mail.channels linked to this user
          group, and the user. This is done by overriding the write method.
    """
    _inherit = 'res.users'

    @api.model
    def systray_get_activities(self):
        activities = self.env["mail.activity"].search([("user_id", "=", self.env.uid)])
        activities_by_record_by_model_name = defaultdict(lambda: defaultdict(lambda: self.env["mail.activity"]))
        for activity in activities:
            record = self.env[activity.res_model].browse(activity.res_id)
            activities_by_record_by_model_name[activity.res_model][record] += activity
        model_ids = list({self.env["ir.model"]._get(name).id for name in activities_by_record_by_model_name.keys()})
        user_activities = {}
        for model_name, activities_by_record in activities_by_record_by_model_name.items():
            domain = [("id", "in", list({r.id for r in activities_by_record.keys()}))]
            allowed_records = self.env[model_name].search(domain)
            if not allowed_records:
                continue
            module = self.env[model_name]._original_module
            icon = module and modules.module.get_module_icon(module)
            model = self.env["ir.model"]._get(model_name).with_prefetch(model_ids)
            user_activities[model_name] = {
                "id": model.id,
                "name": model.name,
                "model": model_name,
                "type": "activity",
                "icon": icon,
                "total_count": 0,
                "today_count": 0,
                "overdue_count": 0,
                "planned_count": 0,
                "done_count": 0,
                "actions": [
                    {
                        "icon": "fa-clock-o",
                        "name": "Summary",
                    }
                ],
            }
            for record, activities in activities_by_record.items():
                if record not in allowed_records:
                    continue
                for activity in activities:
                    user_activities[model_name]["%s_count" % activity.state] += 1
                    if activity.state in ("today", "overdue"):
                        user_activities[model_name]["total_count"] += 1
        return list(user_activities.values())

