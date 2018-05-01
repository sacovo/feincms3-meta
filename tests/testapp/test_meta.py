from django import test
from django.utils.functional import lazy

from feincms3_meta.utils import meta_tags


class MetaTest(test.TestCase):
    def test_meta(self):
        request = test.RequestFactory().get('/')
        self.assertEqual(
            str(meta_tags(request=request)),
            '''\
<meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/">
  <meta name="description" content="">''')

        lazy_url = lazy(lambda: '/', str)()
        self.assertEqual(
            str(meta_tags(url=lazy_url, request=request)),
            '''\
<meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/">
  <meta name="description" content="">''')

        self.assertEqual(
            str(meta_tags(
                request=request,
                defaults={'title': 'stuff'},
                title=None,
            )),
            '''\
<meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/">
  <meta name="description" content="">''')