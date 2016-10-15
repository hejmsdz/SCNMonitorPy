import html.parser
import logging

class HTMLParser(html.parser.HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = logging.getLogger('scnmonitor.HTMLParser')
        self.num_table = 0
        self.num_cell = 0
        self.current_field = None
        self.output = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.num_table += 1
            self.log.debug("Found a table (%d)", self.num_table)
        elif tag == 'td' and ('class', 'form_values') in attrs:
            self.num_cell += 1
            self.log.debug("Found a td.form_values (%d)", self.num_cell)
        elif tag == 'span':
            self.log.debug("Found a span")
        else:
            return

        fields = [None, 'download', 'upload', 'total']
        if self.num_table == 1 and self.num_cell <= 3:
            self.current_field = fields[self.num_cell]
            if self.num_cell == 3 and tag == 'span':
                self.current_field = 'percentage'

        self.log.debug("The current field is %s", self.current_field)

    def handle_data(self, data):
        if self.current_field is None:
            return

        self.log.debug("Found data for %s: %s", self.current_field, data)
        self.output[self.current_field] = data

        self.current_field = None
