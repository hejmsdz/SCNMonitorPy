import threading

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject

class GUIEventHandler(object):
    def __init__(self, client, builder):
        self.client = client
        self.builder = builder

    def check_transfer(self):
        usage_bar = self.builder.get_object('usageBar')
        reload_button = self.builder.get_object('reloadButton')
        download_label = self.builder.get_object('downloadLabel')
        upload_label = self.builder.get_object('uploadLabel')
        total_label = self.builder.get_object('totalLabel')
        percentage_label = self.builder.get_object('percentageLabel')

        def on_ready():
            usage_bar.set_fraction(self.client.percentage/100.0)
            percentage_label.set_text("{}%".format(self.client.percentage))
            download_label.set_text("Download: {:.2f} GB".format(self.client.download))
            upload_label.set_text("Upload: {:.2f} GB".format(self.client.upload))
            total_label.set_text("Total: {:.2f} GB".format(self.client.total))

            reload_button.set_label("Reload")
            reload_button.set_sensitive(True)

        def call_async():
            self.client.check()
            GObject.idle_add(on_ready)

        reload_button.set_sensitive(False)
        reload_button.set_label("Checking...")
        worker = threading.Thread(target=call_async)
        worker.start()

    def mainWindow_delete_event_cb(self, *args):
        Gtk.main_quit(*args)

    def reloadButton_clicked_cb(self, button):
        self.check_transfer()

    def exitButton_clicked_cb(self, button):
        Gtk.main_quit()
