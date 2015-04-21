"""
Locust tests for the profile_images API.
"""
import os
import logging
from locust import task

from ..helpers.auto_auth_tasks import AutoAuthTasks


class ProfileImagesTasks(AutoAuthTasks):

    image_file_directory = image_file_path = os.path.join(os.path.dirname(__file__), "data/")

    def on_start(self):
        """
        Setup code.
        """
        self.auto_auth()

    @task(15)
    def upload_small_jpg(self):
        """
        Uploads a small JPEG image (possibly replacing what was there previously).
        """
        self.upload("small", "jpeg")

    @task(15)
    def upload_large_jpg(self):
        """
        Uploads a large JPEG image (possibly replacing what was there previously).
        """
        self.upload("large", "jpeg")

    @task(15)
    def upload_small_png(self):
        """
        Uploads a small PNG image (possibly replacing what was there previously).
        """
        self.upload("small", "png")

    @task(15)
    def upload_large_png(self):
        """
        Uploads a large PNG image (possibly replacing what was there previously).
        """
        self.upload("large", "png")

    @task(15)
    def upload_small_gif(self):
        """
        Uploads a small GIF image (possibly replacing what was there previously).
        """
        self.upload("small", "gif")

    @task(15)
    def upload_large_gif(self):
        """
        Uploads a large GIF image (possibly replacing what was there previously).
        """
        self.upload("large", "gif")

    @task(10)
    def remove_images(self):
        """
        Deletes any stored images.
        """
        self.post(
            "/api/profile_images/v0/{}/remove".format(self._username),
            name='profile_images:remove'
        )

    def upload(self, name, extension):
        """
        Do file upload operation.
        """
        filename = name + "." + extension
        image_file_path = os.path.join(self.image_file_directory, filename)
        with open(image_file_path,'rb') as image_file:
            self.post(
                "/api/profile_images/v0/{}/upload".format(self._username),
                files=[('file', (filename, image_file, "image/"+extension))],
                name="profile_images:upload_" + name + "_" + extension
            )

    def post(self, path, *args, **kwargs):
        """
        Perform a POST.
        """
        kwargs['headers'] = {
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.locust.host,
            'format': 'multipart'
        }
        logging.debug(path)
        return getattr(self.client, "post")(path, *args, **kwargs)
