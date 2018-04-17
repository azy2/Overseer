"""uWSGI entry point."""
import os

from ovs import create_app

config_path = 'config/config-local-dev.json'
if not os.path.exists(config_path):
    config_path = None
app = create_app(config_path)

if __name__ == '__main__':
    app.run()
