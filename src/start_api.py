from common.utils.debugtool import DebugTool
# from common.data_cache import DataCache

from app import config, create_app

# from gevent import monkey

# monkey.patch_all()

app = create_app()
DebugTool.start_logging(entry_point=__file__)

# DataCache.flush_transaction()

env = config['ENVIRONMENT']
debug = env == 'develop'

if __name__ == '__main__':
    app.run(debug=debug, host='0.0.0.0', port=5000)
