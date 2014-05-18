

from .control import Control

def main(**settings):
    app = Control(**settings)
    app.run()
