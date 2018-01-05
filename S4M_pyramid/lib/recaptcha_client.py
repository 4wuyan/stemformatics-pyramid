from webhelpers2.html import literal
class Recaptcha(object):
    """Recaptcha functionality for Pylons applications.

1. Install recaptcha-client from http://pypi.python.org/pypi/recaptcha-clientpackage

2. Sign up for keys at http://recaptcha.net

3. Add the following items to development.ini:

::

    recaptcha.public_key = yourpublickey
    recaptcha.private_key = yourprivatekey

    #optional list of known proxies
    #recaptcha.local_proxies = 127.0.0.1, 192.168.0.42

4. Example usage:

::

    #in myproject/lib/helpers.py
    recaptcha = Recaptcha()

    #in the controller that renders the recaptcha-proected form::
    c.recaptcha = h.recaptcha.displayhtml() #insert c.recaptcha into the form

    #in the controller that handles the form POST::
    recaptcha_response = h.recaptcha.submit()
    if not recaptcha_response.is_valid:
        #render the form and try again
        c.recaptcha = h.recaptcha.displayhtml(error=recaptcha_response.error_code)

"""

    def __init__(self):
        """Recaptcha might be called before config is parsed, e.g. in project.lib.helpers, so defer config lookup"""

        import recaptcha.client.captcha
        recaptcha.client.captcha.RecaptchaResponse

    def _deferred_lookup(self, **kws):
        from pylons import config
        self._public_key = config['recaptcha.public_key']
        self._private_key = config['recaptcha.private_key']
        local_proxies = config.get('recaptcha.local_proxies', '127.0.0.1')
        self._local_proxies = list(i.strip() for i in local_proxies.split(','))
        self.displayhtml = self._displayhtml
        return self.displayhtml(**kws)
    displayhtml = _deferred_lookup

    def _displayhtml(self, use_ssl=False, error=None):
        """Return HTML string for inserting recaptcha into a form."""
        from recaptcha.client.captcha import displayhtml
        return literal(displayhtml(self._public_key, use_ssl = use_ssl, error = error))

    def submit(self):
        """Return an instance of recaptcha.client.captcha.RecaptchaResponse."""
        from pylons import request
        if request.environ.get('paste.testing', False):
            from recaptcha.client.captcha import RecaptchaResponse
            return RecaptchaResponse(False, 'paste.testing')
        from recaptcha.client.captcha import submit
        recaptcha_challenge_field = request.POST.get('recaptcha_challenge_field', None)
        recaptcha_response_field = request.POST.get('recaptcha_response_field', None)
        remoteip = request.environ.get('REMOTE_ADDR', None)
        if remoteip in self._local_proxies:
            remoteip = request.environ.get('HTTP_X_FORWARDED_FOR', remoteip)

        return submit(recaptcha_challenge_field, recaptcha_response_field, self._private_key, remoteip)
