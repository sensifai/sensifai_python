from string import ascii_letters
import random
import http.client
import mimetypes


def random_string(length):
    return ''.join([random.choice(ascii_letters) for i in range(length)])


def encode_multipart_data(file):
    boundary = random_string(30)

    def get_content_type (filename):
        return mimetypes.guess_type (filename)[0] or 'application/octet-stream'

    def encode_file (filename):
        return ('--' + boundary,
                'Content-Disposition: form-data; name="file"; filename="%s"' % filename,
                'Content-Type: %s' % get_content_type(filename),
                '', open(filename, 'rb').read().decode('ISO-8859-1')
                )

    lines = []
    lines.extend(encode_file(file))
    lines.extend(('--%s--' % boundary, ''))
    body = '\r\n'.join(lines)

    content_type = 'multipart/form-data; boundary=' + boundary
    content_length = str(len(body))

    return body, content_type, content_length
