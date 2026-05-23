import unittest
from mirror import get_depth, get_relative_prefix, rewrite_url, rewrite_html

class TestMirror(unittest.TestCase):
    
    def test_get_depth(self):
        self.assertEqual(get_depth('/'), 0)
        self.assertEqual(get_depth('/publications'), 1)
        self.assertEqual(get_depth('/students'), 1)
        self.assertEqual(get_depth('/talks'), 1)
        self.assertEqual(get_depth('/group'), 1)
        self.assertEqual(get_depth('/some/deep/page'), 3)
        self.assertEqual(get_depth(''), 0)

    def test_get_relative_prefix(self):
        self.assertEqual(get_relative_prefix(0), "")
        self.assertEqual(get_relative_prefix(1), "../")
        self.assertEqual(get_relative_prefix(2), "../../")

    def test_rewrite_url_local_pages(self):
        # From root (depth 0)
        self.assertEqual(rewrite_url('/', '/'), './')
        self.assertEqual(rewrite_url('/', '/publications'), 'publications/')
        self.assertEqual(rewrite_url('/', '/students'), 'students/')
        self.assertEqual(rewrite_url('/', '/talks'), 'talks/')
        self.assertEqual(rewrite_url('/', '/group'), 'group/')

        # From depth 1 (e.g. /publications)
        self.assertEqual(rewrite_url('/publications', '/'), '../')
        self.assertEqual(rewrite_url('/publications', '/publications'), '../publications/')
        self.assertEqual(rewrite_url('/publications', '/students'), '../students/')
        self.assertEqual(rewrite_url('/publications', '/talks'), '../talks/')
        self.assertEqual(rewrite_url('/publications', '/group'), '../group/')
        
        # Test homepage mapping
        self.assertEqual(rewrite_url('/publications', '/homepage'), '../')
        self.assertEqual(rewrite_url('/', '/homepage'), './')
        
        # Test caslogin mapping
        self.assertEqual(rewrite_url('/publications', '/caslogin'), 'https://klusowski.princeton.edu/caslogin')
        
        # Test anchors
        self.assertEqual(rewrite_url('/publications', '/students#anchor'), '../students/#anchor')
        self.assertEqual(rewrite_url('/', '/publications#anchor'), 'publications/#anchor')

    def test_rewrite_url_assets(self):
        # From root
        self.assertEqual(
            rewrite_url('/', '/core/assets/vendor/jquery/jquery.min.js?v=4.0.0'),
            'core/assets/vendor/jquery/jquery.min.js'
        )
        self.assertEqual(
            rewrite_url('/', '/sites/g/files/toruqf5901/files/documents/Klusowski_cv.pdf'),
            'sites/g/files/toruqf5901/files/documents/Klusowski_cv.pdf'
        )

        # From depth 1
        self.assertEqual(
            rewrite_url('/publications', '/core/assets/vendor/jquery/jquery.min.js?v=4.0.0'),
            '../core/assets/vendor/jquery/jquery.min.js'
        )
        self.assertEqual(
            rewrite_url('/publications', '/sites/g/files/toruqf5901/files/documents/Klusowski_cv.pdf'),
            '../sites/g/files/toruqf5901/files/documents/Klusowski_cv.pdf'
        )

    def test_rewrite_url_external_and_special(self):
        self.assertEqual(rewrite_url('/publications', 'https://orfe.princeton.edu'), 'https://orfe.princeton.edu')
        self.assertEqual(rewrite_url('/publications', 'mailto:example@princeton.edu'), 'mailto:example@princeton.edu')
        self.assertEqual(rewrite_url('/publications', '#main-content'), '#main-content')

    def test_rewrite_url_typekit(self):
        self.assertEqual(rewrite_url('/', '//use.typekit.net/bok5fgz.css'), '__TYPEKIT__')
        self.assertEqual(rewrite_url('/publications', 'https://use.typekit.net/ozr7oya.css'), '__TYPEKIT__')

    def test_rewrite_html(self):
        html = """
        <html>
            <head>
                <link rel="stylesheet" href="//use.typekit.net/bok5fgz.css">
                <link rel="stylesheet" href="/profiles/ps/themes/ps_base/css/styles.css?v=1">
                <script src="/core/assets/vendor/jquery/jquery.min.js"></script>
            </head>
            <body>
                <a href="#edit-search-keys" class="sr-only sr-only-focusable">Skip to search</a>
                <a href="/publications">Publications</a>
                <a href="https://orfe.princeton.edu">ORFE</a>
                <div class="utility-menu">
                    <ul class="nav navbar-nav utility-nav">
                        <li class="nav-item">
                            <a class="ps-login-link ps-login-logout-link" data-drupal-link-system-path="caslogin" href="https://klusowski.princeton.edu/caslogin">Log in</a>
                        </li>
                    </ul>
                </div>
                <div class="search-bar" id="search-bar">
                    <form id="search-block-form"></form>
                </div>
                <img src="/sites/g/files/toruqf5901/files/styles/1x1_750w_750h/public/2026-04/profile.png" srcset="/sites/g/files/toruqf5901/files/styles/1x1_750w_750h/public/2026-04/profile.png 1x, /sites/g/files/toruqf5901/files/styles/1x1_750w_750h/public/2026-04/profile.png 2x">
            </body>
        </html>
        """
        discovered = set()
        rewritten = rewrite_html(html, '/publications', discovered)
        
        # Verify typekit URL is set in head and the old one is gone
        self.assertIn('https://use.typekit.net/oym8vwq.css', rewritten)
        self.assertNotIn('bok5fgz.css', rewritten)
        
        # Verify relative asset references
        self.assertIn('../profiles/ps/themes/ps_base/css/styles.css', rewritten)
        self.assertIn('../core/assets/vendor/jquery/jquery.min.js', rewritten)
        
        # Verify relative links
        self.assertIn('../publications/', rewritten)
        self.assertIn('https://orfe.princeton.edu', rewritten)
        
        # Verify search bar and skip search links are removed
        self.assertNotIn('search-bar', rewritten)
        self.assertNotIn('#edit-search-keys', rewritten)
        
        # Verify login link and utility menu are removed
        self.assertNotIn('ps-login-link', rewritten)
        self.assertNotIn('utility-menu', rewritten)
        self.assertNotIn('Log in', rewritten)
        
        # Verify img src and srcset
        self.assertIn('../sites/g/files/toruqf5901/files/styles/1x1_750w_750h/public/2026-04/profile.png', rewritten)
        
        # Verify discovered assets contains key local paths
        self.assertIn('/profiles/ps/themes/ps_base/css/styles.css', discovered)
        self.assertIn('/core/assets/vendor/jquery/jquery.min.js', discovered)
        self.assertIn('/sites/g/files/toruqf5901/files/styles/1x1_750w_750h/public/2026-04/profile.png', discovered)

if __name__ == '__main__':
    unittest.main()
