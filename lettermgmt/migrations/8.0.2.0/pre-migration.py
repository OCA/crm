# -*- coding: utf-8 -*-
# © 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    if version is None:
        return

    # Rename model 'letter.class' to 'letter.category'
    cr.execute("""ALTER TABLE letter_class RENAME TO letter_category""")
    cr.execute("""UPDATE ir_model_fields SET relation = 'letter.category'
                  WHERE relation = 'letter.class'""")
    cr.execute("""UPDATE ir_model_fields SET model = 'letter.category'
                  WHERE model = 'letter.class'""")
    cr.execute("""UPDATE ir_model_data SET model = 'letter.category'
                  WHERE model = 'letter.class'""")
    cr.execute("""UPDATE ir_attachment SET res_model = 'letter.category'
                  WHERE res_model = 'letter.class'""")
