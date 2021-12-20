from fe.bench.workload import Workload
from fe.bench.workload import NewOrder
from fe.bench.workload import Payment
import matplotlib.pyplot as plt
import time
import threading
import logging
import requests

def testThroughPut():
    wl = Workload()
    wl.gen_database()
    new_order_request = []
    for i in range(0, wl.procedure_per_session):
        new_order = wl.get_new_order()
        new_order_request.append(new_order)
    # logging.info('order loaded.')
    tot_order_count = 0
    ok_order_count = 0
    time_order = 0
    tot_payment_count = 0
    ok_payment_count = 0
    time_payment = 0

    payment_request = []
    for new_order in new_order_request:
        before = time.time()
        ok, order_id = new_order.run()
        after = time.time()
        time_order += after - before
        tot_order_count += 1
        if ok:
            ok_order_count += 1
            payment = Payment(new_order.buyer, order_id)
            payment_request.append(payment)

    for payment in payment_request:
        before = time.time()
        ok = payment.run()
        after = time.time()
        time_payment += after - before
        tot_payment_count += 1
        if ok:
            ok_payment_count += 1

    global s_tot_order_count, s_ok_order_count, s_time_order, s_tot_payment_count, s_ok_payment_count, s_time_payment, lock
    lock.acquire()
    s_tot_order_count += tot_order_count
    s_ok_order_count += ok_order_count
    s_time_order += time_order
    s_tot_payment_count += tot_payment_count
    s_ok_payment_count += ok_payment_count
    s_time_payment += time_payment
    lock.release()


lock = threading.Lock()

def draw_plot(threadsNum, tps_order, latency_order, tps_payment, latency_payment):
    plt.style.use('seaborn')
    fig, ax = plt.subplots(1,2, figsize=(14, 7))
    ax[0].plot(threadsNum, tps_order, marker = 'o', label='tps_order')
    ax[1].plot(threadsNum, latency_order, marker = 'o', label='latency_order')
    ax[0].plot(threadsNum, tps_payment, marker = '^', label='tps_payment')
    ax[1].plot(threadsNum, latency_payment, marker = '^', label='latency_payment')
    ax[0].set_xlabel('Concurrency requests number')
    ax[0].set_ylabel('Throughput(requests/s)')
    ax[1].set_xlabel('Concurrency requests number')
    ax[1].set_ylabel('latency(s)')
    ax[0].legend()
    ax[1].legend()
    plt.savefig('fe/tps/tps_latency_pic.png')
    
if __name__ == '__main__':
    threadsNumList = [1, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
    repeatTime = 3
    tps_order = []
    latency_order = []
    tps_payment = []
    latency_payment = []
    logging.basicConfig(level=logging.INFO, filename='fe/tps/testTps.log')
    print('Test started.')
    for threadsNum in threadsNumList:
        print('Testing threads: %d' % threadsNum)
        m_tps_order = 0
        m_latency_order = 0
        m_tps_payment = 0
        m_latency_payment = 0
        for _ in range(repeatTime):
            s_tot_order_count = 0
            s_ok_order_count = 0
            s_time_order = 0
            s_tot_payment_count = 0
            s_ok_payment_count = 0
            s_time_payment = 0
            logging.info("ThreadsNum: %d" % threadsNum)
            threads = []
            for jk in range(threadsNum):
                s = threading.Thread(target=testThroughPut) 
                threads.append(s)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            logging.info("ok_rate_order:{:.2f}%, tps_order:{:.2f}, latency_order:{:.6f}, ok_rate_payment:{:.2f}%, tps_payment:{:.2f}, latency_payment:{:.6f}".format(
                s_ok_order_count / s_tot_order_count * 100, s_ok_order_count / (s_time_order / threadsNum), s_time_order / s_tot_order_count,
                s_ok_payment_count / s_tot_payment_count * 100, s_ok_payment_count / (s_time_payment / threadsNum), s_time_payment / s_tot_payment_count))
            m_tps_order += s_ok_order_count / (s_time_order / threadsNum)
            m_latency_order += s_time_order / s_tot_order_count
            m_tps_payment += s_ok_payment_count / (s_time_payment / threadsNum)
            m_latency_payment += s_time_payment / s_tot_payment_count
        
        tps_order.append(m_tps_order / repeatTime)
        latency_order.append(m_latency_order / repeatTime)
        tps_payment.append(m_tps_payment / repeatTime)
        latency_payment.append(m_latency_payment / repeatTime)

    draw_plot(threadsNumList, tps_order, latency_order, tps_payment, latency_payment)
    print('Test finished. Result: fe/tps/tps_latency_pic.png')
    