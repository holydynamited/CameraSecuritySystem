import os
import threading

import requests


def send_async(url, data, files, file_to_remove=None):
    """Runs the sending task in a separate thread."""

    def run():
        try:
            res = requests.post(url, data=data, files=files, timeout=60)

            # Close only objects that have a .close() method (like file handles)
            for k in files:
                file_obj = files[k][1]
                if hasattr(file_obj, 'close'):
                    file_obj.close()

            if file_to_remove and os.path.exists(file_to_remove):
                os.remove(file_to_remove)
            print(f"[Notify] Sent. Status: {res.status_code}")
        except Exception as e:
            print(f"[Notify Error] {e}")

    threading.Thread(target=run).start()