from subprocess import Popen
from tenacity import *
import sys, time, os, signal, psutil

home_directory = os.environ.get("HOME")
signal_file_path = os.path.join(home_directory, "alive.signal")
nonce_file_path = os.path.join(home_directory, "nonce.txt")
current_try_count = 0


@retry(stop=stop_after_attempt(5))
def run_brownie(args):
    global current_try_count

    # Kill processes to make sure we start clean
    kill_process_by_cmdline("ganache-cli")
    kill_process_by_name("brownie")

    if os.path.exists(signal_file_path) and current_try_count == 0:
        os.remove(signal_file_path)
        print("cleaning up signal from last run")

    if os.path.exists(nonce_file_path):
        if current_try_count == 0:
            os.remove(nonce_file_path)
        else:
            print("nonce found, aborting before we trigger another tx")
            exit(1)

    p = Popen(args)

    # sleep 10, 20, 30, 40, 50, or 60 seconds based on retries
    sleep_time = 10 + min(current_try_count * 10, 50)
    print(f"waiting for alive signal, sleeping for {sleep_time} seconds")
    time.sleep(sleep_time)

    current_try_count += 1

    if not os.path.exists(signal_file_path):
        print(f"alive signal not found, killing brownie and ganache. queuing try #{current_try_count}")
        p.terminate()
        kill_process_by_cmdline("ganache-cli")
        raise Exception()

    print("found alive signal, waiting for process to complete")
    exit_code = p.wait()
    os.remove(signal_file_path)
    exit(exit_code)


def kill_process_by_cmdline(cmdline_arg_find):
    for proc in psutil.process_iter():
        for cmdline_arg in proc.cmdline():
            if cmdline_arg_find in cmdline_arg:
                pid = proc.pid
                os.kill(int(pid), signal.SIGKILL)


def kill_process_by_name(proc_name):
    for proc in psutil.process_iter():
        if proc_name == proc.name():
            pid = proc.pid
            os.kill(int(pid), signal.SIGKILL)


if __name__ == "__main__":
    run_brownie(sys.argv[1:])
