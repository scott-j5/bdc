================
Django Bootstrap 5 Modal
================

|PyPi_Version| |PyPi_Status| |Format| |python_versions| |django_versions| |License|

Django Bootstrap 5 Modal is a simple Django plugin that aims to simplify the process of using bootstrap 5 modals in your templates

Key features
============

* Create a new modal and modal button/link using a single template tag.
* Turn any existing html block into a modal link using a single template tag.
* Dynamically load content to your bootstrap modals.
* Included ajax submission/validation recipe for in-modal forms.
* Works with forward/back browser navigation.


Usage
============
* Install django-imageit using pip
    .. code-block:: shell

        pip install django-bootstrap5-modal


* Add 'bootstrap5-modal' to INSTALLED_APPS in your settings.py
    .. code-block:: python

        INSTALLED_APPS = [
            ...
            'bootstrap5-modal',
            ...
        ]

* Use bootstrap 5 Modal in your templates using the following tags
	.. code-block:: python

        ...
		{% modal_btn %}
		...
		{% modal_link %}
		...
		{% modal_link_wrapper %}
			# html code block to be wrapped in a modal link
		{% end_modal_Link_wrapper %}
		...

* If the target_modal key word argument is provided

* Available key word arguments
	All arguments are optional, however: 'url' and 'target_modal' arguments must not be absent together!
	* **url (str)/(template_var)**: The url of the page to be loaded into the modal on click. If blank or missing, the content of 'target_modal' will be shown.
    * **target_modal (str)**: ID selector for desired target_modal. If blank or missing, a new modal will be created and inserted into the DOM immediately after the triggering button.
    * **class_list (str)**: Class list applied to the created modal button/link
    * **btn_text (str)**: (Only avaiable on '{% modal_btn %}' tag) Specifies the text to be shown within the gereated modal button
    * **link_text (str)**: (Only avaiable on '{% modal_link %}' tag) Specifies the text to be shown within the generated modal link

    .. note:: Imageit fields inherit from the existing Django `FileField <https://docs.djangoproject.com/en/3.2/ref/models/fields/#filefield>`_. Therefore FileField arguments are also accepted (such as upload_to).


Template Tags & Options
============
Imageit provides many options to tailor functionality specifically for your use case. While specific dimensions for scaling can be set as arguments on a field-by-field basis, Imageit also allows for project wide defaults to be set if no value is provided at the field level.

Imageit will default to 100dpi quality at maximum dimensions of 1000x1000, If you wish to use your own custom defaults, you can do so in your settings.py as follows.

**Settings overrides**
.. code-block:: python

    IMAGEIT_MAX_UPLOAD_SIZE_MB = 5
    IMAGEIT_MAX_SAVE_SIZE_MB = 5
    IMAGEIT_DEFAULT_IMAGE_PROPS = {"max_width": 1000, "max_height": 1000, "quality": 100, "upscale": False}
    IMAGEIT_ACCEPTED_CONTENT_TYPES = 'image/jpeg', 'image/png', 'image/svg+xml'
    IMAGEIT_SVG_CONTENT_TYPE = 'image/svg+xml'

* **IMAGEIT_MAX_UPLOAD_SIZE_MB** is provided in MB, and is validated on the client side as well as on the server before cropping/scaling.

* **IMAGEIT_MAX_SAVE_SIZE_MB** is provided in MB, and is validated on the server after and scaling/cropping/resampling is completed.

* **IMAGEIT_DEFAULT_IMAGE_PROPS** Default properties used to scale/resample images

* **IMAGEIT_ACCEPTED_CONTENT_TYPES** Content types accepted by imageit. (File mimes are validated by 3rd party FileTypes package)

.. warning:: It is not reccomended to allow svg file uploads to untrusted users. Imageit will allow upload of svg images if specified in your accepted content types. It must be noted that while Imageit completes checks for scripts in svg files, no guarantee of security from XSS attacks is provided. 



.. _Django: https://www.djangoproject.com

.. |PyPi_Version| image:: https://img.shields.io/pypi/v/django-imageit.svg
.. |PyPi_Status| image:: https://img.shields.io/pypi/status/django-imageit.svg
.. |Format| image:: https://img.shields.io/pypi/format/django-imageit.svg
.. |python_versions| image:: https://img.shields.io/pypi/pyversions/django-imageit.svg
.. |django_versions| image:: https://img.shields.io/badge/Django-3.0,%203.1,%203.2-green.svg
.. |License| image:: https://img.shields.io/pypi/l/django-imageit.svg