#!/usr/bin/env python
from nexnest import createApp

app = createApp(os.getenv('FLASK_CONFIG') or 'default')

app.run(host='0.0.0.0',
        port=8080,
        debug=True)
