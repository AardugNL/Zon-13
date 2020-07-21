# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, api


class Resource(models.Model):
    _inherit = 'resource.resource'

    @api.model
    def create(self, vals):
        '''Create task resource'''
        res = super(Resource, self).create(vals)
        self.env['task.resource'].create({
            'obj_type': 'resource',
            'category_ids': vals.get('category_ids', None),
            'resource_img': vals.get('resource_image', None),
            'resource_id': res.id
        })
        return res

    def unlink(self):
        '''Delete task resource'''
        resource = self.env['task.resource'].search([('resource_id', '=', self.id)])
        resource.unlink()
        return super(Resource, self).unlink()
