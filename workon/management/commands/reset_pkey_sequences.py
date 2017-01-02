# encoding: utf-8

import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):


    help = "Little help to describe the command" \
        "\n  usage:   ./manage.py reset_pkey_sequences [options]"


    # def add_arguments(self, parser):
    #     parser.add_argument('table')

    def handle(self, *args, **options):

        import os
        from StringIO import StringIO

        os.environ['DJANGO_COLORS'] = 'nocolor'

        from django.core.management import call_command
        from django.apps import apps
        from django.db import connection

        commands = StringIO()
        cursor = connection.cursor()

        for app in apps.get_app_configs():
            label = app.label
            call_command('sqlsequencereset', label, stdout=commands)

        cursor.execute(commands.getvalue())

        # # Login to psql and run the following
        # # What is the result?
        # cursor = connection.cursor()
        # cursor.execute('''SELECT MAX(id) FROM %s''' % table)
        # max_id = cursor.fetchone()[0]
        # print 'Max ID is %s' % max_id

        # # Then run...
        # # This should be higher than the last result.
        # cursor.execute('''SELECT nextval('%s_id_seq')''' % table)
        # next_val = cursor.fetchone()[0]
        # print 'Next val is %s' % next_val

        # if next_val <= max_id:
        #     print "ID seq is corrupted... reset sequence"
        #     cursor.execute('''SELECT setval('%s_id_seq', (SELECT MAX(id) FROM %s))''' % (table, table))
        #     print "ID seq recovery done."


        # cursor.execute('''SELECT MAX(id) FROM %s''' % table)
        # max_id = cursor.fetchone()[0]
        # print 'Max ID is %s' % max_id
        # cursor.execute('''SELECT nextval('%s_id_seq')''' % table)
        # current_next_val = cursor.fetchone()[0]
        # print 'Next val is %s' % current_next_val

        # SELECT nextval('your_table_id_seq');

        # # If it's not higher... run this set the sequence last to your highest pid it.
        # # (wise to run a quick pg_dump first...)
        # SELECT setval('your_table_id_seq', (SELECT MAX(id) FROM your_table));
        # # if your tables might have no rows
        # # false means the set value will be returned by the next nextval() call
        # SELECT setval('your_table_id_seq', COALESCE((SELECT MAX(id)+1 FROM your_table), 1), false);