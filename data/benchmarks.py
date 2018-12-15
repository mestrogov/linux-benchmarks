# -*- coding: utf-8 -*-

from subprocess import check_output, STDOUT
from psutil import virtual_memory
from time import sleep


class Benchmarks:
    @staticmethod
    def execute():
        for a in range(2):
            print("### Executing benchmarks ...\n\n\n")

            Benchmarks.Sysbench.cpu()
            Benchmarks.Sysbench.memory()
            Benchmarks.Sysbench.fileio()

            Benchmarks.Fio.write()
            Benchmarks.Fio.read()

            Benchmarks.Network.cachefly()
            Benchmarks.Network.speedtest()

            print("### Executing benchmarks again in 30 seconds ...")
            sleep(30)

    class Sysbench:

        @staticmethod
        def cpu():
            print("### Executing Sysbench CPU benchmark ...\n\n")

            s_events = str(str(check_output("sysbench cpu --threads=1 run", shell=True)).split(
                "total number of events:")[1].split("\\")[0].strip())
            m_events = str(str(check_output("sysbench cpu run", shell=True)).split(
                "total number of events:")[1].split("\\")[0].strip())

            print("### Sysbench CPU benchmark results: Single Thread - {0} events; Multi Thread - {1} events".
                  format(s_events, m_events))
            return s_events, m_events

        @staticmethod
        def memory():
            print("### Executing Sysbench Memory benchmark ...\n\n")

            events = str(str(check_output("sysbench memory run", shell=True)).split(
                "total number of events:")[1].split("\\")[0].strip())

            print("### Sysbench Memory benchmark result: {0} events".format(events))
            return events

        @staticmethod
        def fileio():
            print("### Executing Sysbench FileIO benchmark ...\n\n")

            events = str(str(check_output("sysbench fileio --file-test-mode=seqwr run", shell=True)).split(
                "total number of events:")[1].split("\\")[0].strip())

            print("### Sysbench FileIO benchmark result: {0} events".format(events))
            return events

    class Fio:

        @staticmethod
        def write():
            print("### Executing Fio benchmark WRITE ...\n\n")

            jobs = str(round(round(virtual_memory()[0] / 1024 / 1024) / 512))
            raw_result = str(check_output("fio --name=randwrite --ioengine=libaio --iodepth=16 --rw=randwrite "
                                          "--bs=4k --direct=1 --size=512M --numjobs={0} --runtime=240 "
                                          "--group_reporting".format(jobs), shell=True))
            speed = str(raw_result.split("BW=")[1].split(" ")[0].strip())
            iops = str(raw_result.split("IOPS=")[1].split(",")[0].replace("k", "K").strip())

            print("### Fio benchmark WRITE results: Speed - {0}; IOPS - {1}".format(speed, iops))
            return speed, iops

        @staticmethod
        def read():
            print("### Executing Fio benchmark READ ...\n\n")

            jobs = str(round(round(virtual_memory()[0] / 1024 / 1024) / 512))
            raw_result = str(check_output("fio --name=randread --ioengine=libaio --iodepth=16 --rw=randread "
                                          "--bs=4k --direct=1 --size=512M --numjobs={0} --runtime=240 "
                                          "--group_reporting".format(jobs), shell=True))

            speed = str(raw_result.split("BW=")[1].split(" ")[0].strip())
            iops = str(raw_result.split("IOPS=")[1].split(",")[0].replace("k", "K").strip())

            print("### Fio benchmark READ results: Speed - {0}; IOPS - {1}".format(speed, iops))
            return speed, iops

    class Network:

        @staticmethod
        def cachefly():
            print("### Executing Speedtest benchmark ...\n\n")

            download = str(str(check_output("wget -O /dev/null http://cachefly.cachefly.net/100mb.test", stderr=STDOUT,
                                            shell=True)).split("Downloaded:")[1].split("(")[1].split(")")[0].strip())

            print("### Cachefly network download performance: {0}".format(download))
            return download

        @staticmethod
        def speedtest():
            print("### Executing Speedtest benchmark ...\n\n")

            raw_result = str(check_output("speedtest-cli --bytes", shell=True))
            download = str(raw_result.split("Download:")[1].split("/s")[0].replace("Mbyte", "MB/s").strip())
            upload = str(raw_result.split("Upload:")[1].split("/s")[0].replace("Mbyte", "MB/s").strip())

            print("### Speedtest network performance: Download - {0}; Upload - {1}".format(download, upload))
            return download, upload


Benchmarks.execute()
