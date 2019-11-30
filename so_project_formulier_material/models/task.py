# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

class ProjectFormulier(models.Model):
    _inherit = 'question.formulier'

    planned_material_ids = fields.One2many(
        'planned.material.line', 'question_frm_id', string='planned Tasks')
    consumed_material_ids = fields.One2many(
        'consumed.material.line', 'question_frm_id', string='consumed Tasks')
    screw_piles_ids = fields.One2many('screw.piles', 'question_frm_id', string='Screw Piles')

    # De oplevering verliep => Delivery was completed
    according_to_plan = fields.Selection([('Ja', 'Ja'),
                                ('Nee', 'Nee')],
                                string='According to plan', track_visibility='always')
    garden_left_tidy = fields.Selection([('Ja', 'Ja'),
                                ('Nee', 'Nee')],
                                string='The garden has been left tidy', track_visibility='always')
    walls_left_tidy = fields.Selection([('Ja', 'Ja'),
                                ('Nee', 'Nee')],
                                string='The walls have been left tidy', track_visibility='always')
    damage_property_caused = fields.Selection([('Ja', 'Ja'),
                                ('Nee', 'Nee')],
                                string='Damage to your property caused by us', track_visibility='always')
    satisfied_progress_work = fields.Selection([('Ja', 'Ja'),
                                ('Nee', 'Nee')],
                                string='Are you satisfied with the progress of the work?', track_visibility='always')
    comments = fields.Text(string='Comments')

    signature = fields.Binary('Signature', help='Signature received through the portal.', copy=False, attachment=True)
    signed_by = fields.Char('Signed by', help='Name of the person that signed the SO.', copy=False)

class PlannedMaterialLine(models.Model):
    _inherit = 'planned.material.line'

    question_frm_id = fields.Many2one(related='sale_line_id.question_frm_id',
        string='Project Formulier')

class ConsumedMaterialLine(models.Model):
    _inherit = 'consumed.material.line'

    question_frm_id = fields.Many2one(related='sale_id.question_frm_id',
        string='Project formulier')

# class ProjectTask(models.Model):
#     _inherit = 'project.task'

#     @api.model
#     def create(self, vals):
#         res = super(ProjectTask, self).create(vals)
#         if res.question_frm_id:
#             res.name = res.question_frm_id.name
#         return res