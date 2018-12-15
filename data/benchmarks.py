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

            print("\n\n### Executing benchmarks again in 30 seconds ...")
            sleep(30)

    class Sysbench:

        @staticmethod
        def cpu():
            print("\n\n### Executing Sysbench CPU benchmark ...")

            s_events = str(str(check_output("sysbench cpu --threads=1 run", shell=True)).split(
                "total number of events:")[1].split("\\")[0].strip())
            m_events = str(str(check_output("sysbench cpu run", shell=True)).split(
                "total number of events:")[1].split("\\")[0].strip())

            print("### Sysbench CPU benchmark results: Single thread - {0} events; Multi thread - {1} events".
                  format(s_events, m_events))
            return s_events, m_events

        @staticmethod
        def memory():
            print("\n\n### Executing Sysbench Memory benchmark ...")

            events = str(str(check_output("sysbench memory run", shell=True)).split(
                "total number of events:")[1].split("\\")[0].strip())

            print("### Sysbench Memory benchmark result: {0} events".format(events))
            return events

        @staticmethod
        def fileio():
            print("\n\n### Executing Sysbench FileIO benchmark ...")

            events = str(str(check_output("sysbench fileio --file-test-mode=seqwr run", shell=True)).split(
                "total number of events:")[1].split("\\")[0].strip())

            print("### Sysbench FileIO benchmark result: {0} events".format(events))
            return events

    class Fio:

        @staticmethod
        def write():
            print("\n\n### Executing Fio benchmark WRITE ...")

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
            print("\n\n### Executing Fio benchmark READ ...")

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
            print("\n\n### Executing Cachefly network performance benchmark  ...")

            download = str(str(check_output("wget -i /dev/null http://cachefly.cachefly.net/100mb.test", stderr=STDOUT,
                                            shell=True)).split("Downloaded:")[1].split("(")[1].split(")")[0].strip())

            print("### Cachefly network download performance: {0}".format(download))
            return download

        @staticmethod
        def speedtest():
            print("\n\n### Executing Speedtest network performance benchmark ...")

            raw_result = str(check_output("speedtest-cli --bytes", shell=True))
            download = str(raw_result.split("Download:")[1].split("/s")[0].replace("Mbyte", "MB/s").strip())
            upload = str(raw_result.split("Upload:")[1].split("/s")[0].replace("Mbyte", "MB/s").strip())

            print("### Speedtest network performance benchmark: Download - {0}; Upload - {1}".format(download, upload))
            return download, upload


Benchmarks.execute()
