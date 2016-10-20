# -*- coding: utf-8 -*-
# © 2016 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    if version is None:
        return

    # Migrate states ['created', 'validated'] back to 'draft'
    cr.execute("""UPDATE res_letter SET state = 'draft'
                  WHERE state IN ('created', 'validated')""")

    # Migrate snd_date, rec_date
    cr.execute("""UPDATE res_letter SET snd_date = snd_rec_date
                  WHERE move = 'out'""")
    cr.execute("""UPDATE res_letter SET rec_date = snd_rec_date
                  WHERE move = 'in'""")

    # Rename column 'type' to 'type_id'
    cr.execute("""UPDATE res_letter SET type_id = type""")

    # Rename model 'letter.class' to 'letter.category'
    cr.execute("""INSERT INTO letter_category SELECT * FROM letter_class""")
    cr.execute("""UPDATE ir_model_fields SET relation = 'letter.category'
                  WHERE relation = 'letter.class'""")
    cr.execute("""UPDATE ir_model_fields SET model = 'letter.category'
                  WHERE model = 'letter.class'""")
    cr.execute("""UPDATE ir_model_data SET model = 'letter.category'
                  WHERE model = 'letter.class'""")
    cr.execute("""UPDATE ir_attachment SET res_model = 'letter.category'
                  WHERE res_model = 'letter.class'""")

    # Cleanup
    cr.execute("""ALTER TABLE res_letter DROP COLUMN snd_rec_date""")
    cr.execute("""ALTER TABLE res_letter DROP COLUMN type""")
    cr.execute("""ALTER TABLE res_letter DROP COLUMN class""")
    cr.execute("""DROP INDEX IF EXISTS res_letter_snd_rec_date_index""")
    cr.execute("""DROP INDEX IF EXISTS res_letter_type_index""")
    cr.execute("""DROP INDEX IF EXISTS res_letter_class_index""")
    cr.execute("""DROP TABLE letter_class""")
