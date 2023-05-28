import subprocess, re
import sys
import http.client
import socket
import urllib.parse as url

import time

# Main 서버에 대한 위치
loginInfo = [
    {'system_name': socket.gethostname(),
     'ip': '172.0.0.1',
     'port': '80'}
]

def main():
    #cpu 사용량
    output = subprocess.check_output(['top', '-bn1', '-o', '%MEM'])
    match = re.match(r'^[\w\W]*?\n( +PID.*COMMAND)\n([\w\W]*)', output.decode())
    matchs = match[0].split('\n')
    cpu_use = matchs[2].split(',')

    # 디스크 전체 사용량
    # df -P | grep -v ^Filesystem | awk \'{sum += $2} END {print sum/1024}\'
    disk_process = subprocess.Popen(["df"], stdout=subprocess.PIPE)
    awk_process = subprocess.Popen(["awk", '{sum += $2} END {print sum/1024/1024}'], stdin=disk_process.stdout, stdout=subprocess.PIPE)
    total_disk_use = awk_process.communicate()[0]

    # 디스크 현재 사용량
    # df -P | grep -v ^Filesystem | awk '{sum += $3} END {print sum/1024}'
    disk_process = subprocess.Popen(["df"], stdout=subprocess.PIPE)
    awk_process = subprocess.Popen(["awk", '{sum += $3} END {print sum/1024/1024}'], stdin=disk_process.stdout, stdout=subprocess.PIPE)
    realtime_disk_use = awk_process.communicate()[0]

    total_disk = float(total_disk_use.decode().strip())
    use_disk = float(realtime_disk_use.decode().strip())
    disk_use_percent = useDisk / totalDisk * 100

    # 전체 메모리 용량
    # cat /proc/meminfo | grep MemTotal | awk '{print $2/1024}'
    mem_process = subprocess.Popen(["cat", "/proc/meminfo"], stdout=subprocess.PIPE)
    grep_process = subprocess.Popen(["grep", "MemTotal"], stdin=mem_process.stdout, stdout=subprocess.PIPE)
    awk_process = subprocess.Popen(["awk", '{print $2/1024}'], stdin=grep_process.stdout, stdout=subprocess.PIPE)
    total_mem_use = awk_process.communicate()[0]

    # 사용 메모리 용량
    # cat /proc/meminfo | grep MemAvailable | awk '{print $2/1024 " GB"}'
    mem_process = subprocess.Popen(["cat", "/proc/meminfo"], stdout=subprocess.PIPE)
    grep_process = subprocess.Popen(["grep", "MemAvailable"], stdin=mem_process.stdout, stdout=subprocess.PIPE)
    awk_process = subprocess.Popen(["awk", '{print $2/1024}'], stdin=grep_process.stdout, stdout=subprocess.PIPE)
    realtime_mem_use = awk_process.communicate()[0]

    total_mem = float(total_mem_use.decode().strip())
    use_mem = (total_mem - float(realtime_mem_use.decode().strip()))
    use_mem_percent = use_mem / total_mem * 100

    system_name = loginInfo[0]['system_name']
    total_disk = total_disk
    use_disk = use_disk
    percent_disk = disk_use_percent
    use_cpu = re.findall('\d.\d+', cpu_use[0])[0]
    total_mem = total_mem
    use_mem = use_mem
    percent_mem = use_mem_percent

    # create get query param
    param = 'system_name=' + system_name + \
            '&total_disk=' + str(total_disk) + \
            '&use_disk=' + str(use_disk) + \
            '&percent_disk=' + str(percent_disk) + \
            '&use_cpu=' + str(use_cpu) + \
            '&total_mem=' + str(total_mem) + \
            '&use_mem=' + str(use_mem) + \
            '&percent_mem=' + str(percent_mem)
    param = '/monitoring/regist?' + param

    print(param)
    print(loginInfo[0]['ip'])
    conn = http.client.HTTPConnection(loginInfo[0]['ip'])
    conn.request("GET", param)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    sys.exit()

main()