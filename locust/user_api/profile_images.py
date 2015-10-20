"""
Locust tests for the profile_images API.
"""
import os
import sys
import logging
from locust import task

# Work around the fact that this code doesn't live in a proper Python package.
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'helpers'))
from auto_auth_tasks import AutoAuthTasks


class ProfileImagesTasks(AutoAuthTasks):

    image_file_directory = image_file_path = os.path.join(os.path.dirname(__file__), "data/")
    api_endpoint = '/api/user/v1/accounts/{}/image'

    def on_start(self):
        """
        Setup code.
        """
        self.auto_auth()

    @task(15)
    def upload_small_jpg_multipart(self):
        """
        Uploads a small JPEG image (possibly replacing what was there
        previously) submitting data as multipart/form-data.
        """
        self.upload_multipart("small", "jpeg")

    @task(15)
    def upload_small_jpg_raw(self):
        """
        Uploads a small JPEG image (possibly replacing what was there
        previously) submitting data as image/jpeg.
        """
        self.upload_raw("small", "jpeg")

    @task(15)
    def upload_large_jpg_multipart(self):
        """
        Uploads a large JPEG image (possibly replacing what was there previously).
        """
        self.upload_multipart("large", "jpeg")

    @task(15)
    def upload_large_jpg_raw(self):
        """
        Uploads a large JPEG image (possibly replacing what was there previously).
        """
        self.upload_raw("large", "jpeg")

    @task(15)
    def upload_small_png_multipart(self):
        """
        Uploads a small PNG image (possibly replacing what was there previously).
        """
        self.upload_multipart("small", "png")

    @task(15)
    def upload_small_png_raw(self):
        """
        Uploads a small PNG image (possibly replacing what was there previously).
        """
        self.upload_raw("small", "png")

    @task(15)
    def upload_large_png_multipart(self):
        """
        Uploads a large PNG image (possibly replacing what was there previously).
        """
        self.upload_multipart("large", "png")

    @task(15)
    def upload_large_png_raw(self):
        """
        Uploads a large PNG image (possibly replacing what was there previously).
        """
        self.upload_raw("large", "png")

    @task(15)
    def upload_small_gif_multipart(self):
        """
        Uploads a small GIF image (possibly replacing what was there previously).
        """
        self.upload_multipart("small", "gif")

    @task(15)
    def upload_small_gif_raw(self):
        """
        Uploads a small GIF image (possibly replacing what was there previously).
        """
        self.upload_raw("small", "gif")

    @task(15)
    def upload_large_gif_multipart(self):
        """
        Uploads a large GIF image (possibly replacing what was there previously).
        """
        self.upload_multipart("large", "gif")

    @task(15)
    def upload_large_gif_raw(self):
        """
        Uploads a large GIF image (possibly replacing what was there previously).
        """
        self.upload_raw("large", "gif")

    @task(20)
    def remove_images(self):
        """
        Deletes any stored images.
        """
        self.delete()

    def upload_raw(self, name, extension):
        filename = '.'.join([name, extension])
        image_file_path = os.path.join(self.image_file_directory, filename)
        headers = {
            'Content-type': 'image/{}'.format(extension),
            'Content-disposition': 'attachment; filename={}'.format(filename),
        }
        with open(image_file_path, 'rb') as image_file:
            self.post_raw(
                headers=headers,
                data=image_file,
                name='profile_images:{}_{}_raw'.format(extension, name)
            )

    def upload_multipart(self, name, extension):
        """
        Do file upload operation.
        """
        filename = name + "." + extension
        image_file_path = os.path.join(self.image_file_directory, filename)
        with open(image_file_path, 'rb') as image_file:
            self.post_multipart(
                files=[('file', (filename, image_file, "image/"+extension))],
                name="profile_images:{}_{}_multipart".format(extension, name)
            )

    def post_multipart(self, *args, **kwargs):
        kwargs['headers'] = kwargs.get('headers', {})
        kwargs['headers'].update({
            'format': 'multipart',
        })
        self.submit('POST', *args, **kwargs)

    def post_raw(self, *args, **kwargs):
        """
        Perform a POST.
        """
        self.submit('POST', *args, **kwargs)

    def delete(self, *args, **kwargs):
        self.submit('DELETE',
            name='profile_images:remove',
            *args, **kwargs
        )

    def submit(self, method, *args, **kwargs):
        kwargs['headers'] = kwargs.get('headers', {})
        kwargs['headers'].update({
            'X-CSRFToken': self.client.cookies.get('csrftoken', ''),
            'Referer': self.locust.host,
        })
        endpoint = self.api_endpoint.format(self._username)
        return getattr(self.client, method.lower())(endpoint, *args, **kwargs)
