import os

from .api.app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.cli.command()
def test():
    """Run Unit Test"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
  app.run()
