import os
import requests

class Notifier():
    healthcheck_base_path = 'https://hc-ping.com/rGg7D8-J9ZXks41vpCNYpQ/' + os.getenv('MACHINE_NAME').lower()
    heartbeat_base_path = 'https://nixklai.heartbeat.sh/beat/' + os.getenv('MACHINE_NAME') + '?warning=15&error=25'
    
    def constructor():
        pass
    
    def _get_hc_url(self, endpoint = '/'):
        return self.healthcheck_base_path + endpoint

    def inform_success(self):
        print('>[v] Informing successful status')
        requests.get(self._get_hc_url('/'))
        requests.post(self.heartbeat_base_path)

    def inform_failure(self, code=None):
        print('>[x] Informing failed status')
        if code is None:
            requests.get(self._get_hc_url('/fail'))
        else:
           self.inform_exit_status(code)
    
    def inform_exit_status(self, code):
        print('>[i] Informing exit code:', code)
        requests.get(self._get_hc_url('/' + str(code)))

    def inform_start(self, data = None):
        print('>[i] Informing starting status')
        requests.post(
            url=self._get_hc_url('/start'),
            data=data
        )