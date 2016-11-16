#!/usr/bin/env python

import os, sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# from flask.ext.script import Manager, Server
from flask_script import Manager, Server

# from OctBlog import create_app
# app = create_app(os.getenv('config') or 'default')

from OctBlog import app


manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0',
    port = 5000)
)

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    manager.run()
