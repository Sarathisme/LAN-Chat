import multiprocessing
import socket

import nmap

from config import PORT

nm = nmap.PortScanner()


class Mapper:

    def __init__(self):
        self._ADDRESSES = self.map_network()

    def get_addresses(self):
        return self._ADDRESSES

    @staticmethod
    def ping(job_q, results_q):
        while True:

            ip = job_q.get()
            if ip is None:
                break

            try:
                output = nm.scan(ip, str(PORT))['scan'][ip]['tcp'][PORT]['state']
                if output == 'filtered' or output == 'open':
                    results_q.put(ip)
            except Exception as e:
                print(e)

    @staticmethod
    def get_my_ip():
        """
        Find my IP address
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def map_network(self, pool_size=255):
        """
        Maps the network
        :param pool_size: amount of parallel ping processes
        :return: list of valid ip addresses
        """

        ip_list = list()

        # get my IP and compose a base like 192.168.1.xxx
        ip_parts = self.get_my_ip().split('.')
        base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

        # prepare the jobs queue
        jobs = multiprocessing.Queue()
        results = multiprocessing.Queue()

        pool = [multiprocessing.Process(target=self.ping, args=(jobs, results)) for i in range(pool_size)]

        for p in pool:
            p.start()

        # cue hte ping processes
        for i in range(1, 255):
            jobs.put(base_ip + '{0}'.format(i))

        for _ in pool:
            jobs.put(None)

        for p in pool:
            p.join()

        # collect he results
        while not results.empty():
            ip = results.get()
            ip_list.append(ip)

        return ip_list


if __name__ == "__main__":
    Mapper()
