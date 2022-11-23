# -*- coding: utf-8 -*-

from collections import defaultdict
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
import pytz

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import format_date
'''
NOTES:
1-


TODO:
1-


LEARNED THAT:
1-

READ ABOUT:
1-why does he have the active employee check without the domain in the get finction it doesnt not make sense

'''

class HrAppraisalReportEmployees(models.TransientModel):
    _name = 'hr.appraisal.report.employees'
    _description = 'Generate appraisal reports for all selected employees'

    #this is needed as it creates a search domain however not for the contracts in this case but for employees whom this is valid
    #commented for now but needs modification
    '''
    def _get_available_contracts_domain(self):
        return [('contract_ids.state', 'in', ('open', 'close')), ('company_id', '=', self.env.company.id)]
    '''
    #current contraint is only the company as appraisal is applicabkle for everyone
    def _get_available_constraints_domain(self):
        return [('company_id', '=', self.env.company.id)]
    #this is needed as it retrieves a list of all active employees with the domain in mind
    #for now I will deactivate the domain requirements
    '''
    def _get_employees(self):
        active_employee_ids = self.env.context.get('active_employee_ids', False)
        if active_employee_ids:
            return self.env['hr.employee'].browse(active_employee_ids)
        # YTI check dates too
        return self.env['hr.employee'].search(self._get_available_contracts_domain())
    '''
    def _get_employees(self):
        active_employee_ids = self.env.context.get('active_employee_ids', False)
        if active_employee_ids:
            return self.env['hr.employee'].browse(active_employee_ids)
        # YTI check dates too
        return self.env['hr.employee'].search(self._get_available_constraints_domain())
    #this is needed but requires some change, change is right underneath it
    '''
    employee_ids = fields.Many2many('hr.employee', 'hr_employee_group_rel', 'payslip_id', 'employee_id', 'Employees',
                                    default=lambda self: self._get_employees(), required=True,
                                    compute='_compute_employee_ids', store=True, readonly=False)
    '''
    employee_ids = fields.Many2many('hr.employee', 'hr_employee_group_rel', 'appraisal_report', 'employee_id', 'Employees',
                                    default=lambda self: self._get_employees(), required=True,
                                    compute='_compute_employee_ids', store=True, readonly=False)
    
    #I dont think this is needed for now
    #structure_id = fields.Many2one('hr.payroll.structure', string='Salary Structure')
    
    #this is needed
    department_id = fields.Many2one('hr.department')
    
    #this is needed but will require some change, teh change is right underneath it
    '''
    @api.depends('department_id')
    def _compute_employee_ids(self):
        for wizard in self:
            domain = wizard._get_available_contracts_domain()
            if wizard.department_id:
                domain = expression.AND([
                    domain,
                    [('department_id', 'child_of', self.department_id.id)]
                ])
            wizard.employee_ids = self.env['hr.employee'].search(domain)
    '''
    #this is very useful for applying domains
    @api.depends('department_id')
    def _compute_employee_ids(self):
        for wizard in self:
            domain = wizard._get_available_constraints_domain()
            if wizard.department_id:
                domain = expression.AND([domain, [('department_id', 'child_of', self.department_id.id)]])
            wizard.employee_ids = self.env['hr.employee'].search(domain)
    
    
    #i dont think this is needed for now
    '''
    def _check_undefined_slots(self, work_entries, payslip_run):
        """
        Check if a time slot in the contract's calendar is not covered by a work entry
        """
        work_entries_by_contract = defaultdict(lambda: self.env['hr.work.entry'])
        for work_entry in work_entries:
            work_entries_by_contract[work_entry.contract_id] |= work_entry

        for contract, work_entries in work_entries_by_contract.items():
            calendar_start = pytz.utc.localize(datetime.combine(max(contract.date_start, payslip_run.date_start), time.min))
            calendar_end = pytz.utc.localize(datetime.combine(min(contract.date_end or date.max, payslip_run.date_end), time.max))
            outside = contract.resource_calendar_id._attendance_intervals_batch(calendar_start, calendar_end)[False] - work_entries._to_intervals()
            if outside:
                time_intervals_str = "\n - ".join(['', *["%s -> %s" % (s[0], s[1]) for s in outside._items]])
                raise UserError(_("Some part of %s's calendar is not covered by any work entry. Please complete the schedule. Time intervals to look for:%s") % (contract.employee_id.name, time_intervals_str))
    '''
    #I dont think this is needed
    '''
    def _filter_contracts(self, contracts):
        # Could be overriden to avoid having 2 'end of the year bonus' payslips, etc.
        return contracts
    '''
    
    #This is needed but requires a lot of change, change is right underneath it
    '''
    def compute_sheet(self):
        self.ensure_one()
        if not self.env.context.get('active_id'):
            from_date = fields.Date.to_date(self.env.context.get('default_date_start'))
            end_date = fields.Date.to_date(self.env.context.get('default_date_end'))
            today = fields.date.today()
            first_day = today + relativedelta(day=1)
            last_day = today + relativedelta(day=31)
            if from_date == first_day and end_date == last_day:
                batch_name = from_date.strftime('%B %Y')
            else:
                batch_name = _('From %s to %s', format_date(self.env, from_date), format_date(self.env, end_date))
            payslip_run = self.env['hr.payslip.run'].create({
                'name': batch_name,
                'date_start': from_date,
                'date_end': end_date,
            })
        else:
            payslip_run = self.env['hr.payslip.run'].browse(self.env.context.get('active_id'))

        employees = self.with_context(active_test=False).employee_ids
        if not employees:
            raise UserError(_("You must select employee(s) to generate payslip(s)."))

        #Prevent a payslip_run from having multiple payslips for the same employee
        employees -= payslip_run.slip_ids.employee_id
        success_result = {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.payslip.run',
            'views': [[False, 'form']],
            'res_id': payslip_run.id,
        }
        if not employees:
            return success_result

        payslips = self.env['hr.payslip']
        Payslip = self.env['hr.payslip']

        contracts = employees._get_contracts(
            payslip_run.date_start, payslip_run.date_end, states=['open', 'close']
        ).filtered(lambda c: c.active)
        contracts._generate_work_entries(payslip_run.date_start, payslip_run.date_end)
        work_entries = self.env['hr.work.entry'].search([
            ('date_start', '<=', payslip_run.date_end),
            ('date_stop', '>=', payslip_run.date_start),
            ('employee_id', 'in', employees.ids),
        ])
        self._check_undefined_slots(work_entries, payslip_run)

        if(self.structure_id.type_id.default_struct_id == self.structure_id):
            work_entries = work_entries.filtered(lambda work_entry: work_entry.state != 'validated')
            if work_entries._check_if_error():
                work_entries_by_contract = defaultdict(lambda: self.env['hr.work.entry'])

                for work_entry in work_entries.filtered(lambda w: w.state == 'conflict'):
                    work_entries_by_contract[work_entry.contract_id] |= work_entry

                for contract, work_entries in work_entries_by_contract.items():
                    conflicts = work_entries._to_intervals()
                    time_intervals_str = "\n - ".join(['', *["%s -> %s" % (s[0], s[1]) for s in conflicts._items]])
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Some work entries could not be validated.'),
                        'message': _('Time intervals to look for:%s', time_intervals_str),
                        'sticky': False,
                    }
                }


        default_values = Payslip.default_get(Payslip.fields_get())
        payslips_vals = []
        for contract in self._filter_contracts(contracts):
            values = dict(default_values, **{
                'name': _('New Payslip'),
                'employee_id': contract.employee_id.id,
                'credit_note': payslip_run.credit_note,
                'payslip_run_id': payslip_run.id,
                'date_from': payslip_run.date_start,
                'date_to': payslip_run.date_end,
                'contract_id': contract.id,
                'struct_id': self.structure_id.id or contract.structure_type_id.default_struct_id.id,
            })
            payslips_vals.append(values)
        payslips = Payslip.with_context(tracking_disable=True).create(payslips_vals)
        payslips._compute_name()
        payslips.compute_sheet()
        payslip_run.state = 'verify'

        return success_result
    '''
    def compute_sheet(self):
        self.ensure_one()
        if not self.env.context.get('active_id'):
            from_date = fields.Date.to_date(self.env.context.get('default_date_start'))
            end_date = fields.Date.to_date(self.env.context.get('default_date_end'))
            today = fields.date.today()
            #this is a one month interval should be changed to a 1 year interval
            first_day = today + relativedelta(day=1)
            last_day = today + relativedelta(day=31)
            #the batch name calculation should change
            if from_date == first_day and end_date == last_day:
                batch_name = from_date.strftime('%B %Y')
            else:
                batch_name = _('From %s to %s', format_date(self.env, from_date), format_date(self.env, end_date))
            appraisal_report_run = self.env['hr.appraisal.report.run'].create({
                'name': batch_name,
                'date_start': from_date,
                'date_end': end_date,
            })
        else:
            appraisal_report_run = self.env['hr.appraisal.report.run'].browse(self.env.context.get('active_id'))

        employees = self.with_context(active_test=False).employee_ids
        if not employees:
            raise UserError(_("You must select employee(s) to generate appraisal_report(s)."))

        #Prevent an appraisal_run from having multiple appraisal reports for the same employee
        employees -= appraisal_report_run.appraisal_report_ids.employee_id
        success_result = {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.appraisal.report.run',
            'views': [[False, 'form']],
            'res_id': appraisal_report_run.id,
        }
        if not employees:
            return success_result
        
        appraisal_reports = self.env['hr.appraisal.report']
        Appraisal_report = self.env['hr.appraisal.report']
        
        #this part of the method cross checks it is needed later to guarantee noi other reports have been made
        '''
        contracts = employees._get_contracts(
            payslip_run.date_start, payslip_run.date_end, states=['open', 'close']
        ).filtered(lambda c: c.active)
        contracts._generate_work_entries(payslip_run.date_start, payslip_run.date_end)
        work_entries = self.env['hr.work.entry'].search([
            ('date_start', '<=', payslip_run.date_end),
            ('date_stop', '>=', payslip_run.date_start),
            ('employee_id', 'in', employees.ids),
        ])
        self._check_undefined_slots(work_entries, payslip_run)

        if(self.structure_id.type_id.default_struct_id == self.structure_id):
            work_entries = work_entries.filtered(lambda work_entry: work_entry.state != 'validated')
            if work_entries._check_if_error():
                work_entries_by_contract = defaultdict(lambda: self.env['hr.work.entry'])

                for work_entry in work_entries.filtered(lambda w: w.state == 'conflict'):
                    work_entries_by_contract[work_entry.contract_id] |= work_entry

                for contract, work_entries in work_entries_by_contract.items():
                    conflicts = work_entries._to_intervals()
                    time_intervals_str = "\n - ".join(['', *["%s -> %s" % (s[0], s[1]) for s in conflicts._items]])
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Some work entries could not be validated.'),
                        'message': _('Time intervals to look for:%s', time_intervals_str),
                        'sticky': False,
                    }
                }

        '''
        default_values = Appraisal_report.default_get(Appraisal_report.fields_get())
        appraisal_reports_vals = []
        #payslips_vals = []
        #this part populates the rewquired data for the model
        #currently this is used for the contracts, we dont use contracts instead we use kpiitems
        '''
        for contract in self._filter_contracts(contracts):
            values = dict(default_values, **{
                'name': _('New Payslip'),
                'employee_id': contract.employee_id.id,
                'credit_note': payslip_run.credit_note,
                'payslip_run_id': payslip_run.id,
                'date_from': payslip_run.date_start,
                'date_to': payslip_run.date_end,
                'contract_id': contract.id,
                'struct_id': self.structure_id.id or contract.structure_type_id.default_struct_id.id,
            })
            payslips_vals.append(values)
        '''
        for employee in self._get_employees():
            values = dict(default_values, **{
                'name': _('New Appraisal Report'),
                'employee_id': employee.id,
                'appraisal_report_run_id': appraisal_report_run.id,
                'date_from': appraisal_report_run.date_start,
                'date_to': appraisal_report_run.date_end,
            })
            appraisal_reports_vals.append(values)
        appraisal_reports = Appraisal_report.with_context(tracking_disable=True).create(appraisal_reports_vals)
        appraisal_reports._compute_name()
        appraisal_reports.compute_sheet()
        appraisal_reports.state = 'verify'

        return success_result
