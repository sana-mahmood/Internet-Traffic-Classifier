import statistics, math
from datetime import datetime
import datetime
from tkinter import *
import subprocess
from tkinter import messagebox
from tkinter import ttk
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import numpy as ny
import ipaddress
from sklearn import tree
from sklearn import svm
from sklearn.neural_network import MLPClassifier
import tkinter
from tkinter import *
from sklearn.metrics import confusion_matrix


class Burst:
    def __init__(self, st, et):
        self.Packets = list()
        self.start_time = st
        self.end_time = et
        self.s2d_packets = 0
        self.d2s_packets = 0
        self.s2d_bytes = 0
        self.d2s_bytes = 0
        self.s2d_bps = 0
        self.d2s_bps = 0
        self.s2d_pps = 0
        self.d2s_pps = 0
        self.s2d_bpp = 0
        self.d2s_bpp = 0

    def calculations(self):
        for i in range(0, len(self.Packets)):
            if self.Packets[i].type == 1:
                self.s2d_packets = self.s2d_packets + 1
                self.s2d_bytes = self.s2d_bytes + self.Packets[i].length
            if self.Packets[i].type == 2:
                self.d2s_packets = self.d2s_packets + 1
                self.d2s_bytes = self.d2s_bytes + self.Packets[i].length

        self.s2d_bps = self.s2d_bytes * 8 / 3
        self.d2s_bps = self.d2s_bytes * 8 / 3
        self.s2d_pps = self.s2d_packets / 3
        self.d2s_pps = self.d2s_packets / 3
        if self.s2d_packets != 0:
            self.s2d_bpp = self.s2d_bytes / self.s2d_packets
        if self.d2s_packets != 0:
            self.d2s_bpp = self.d2s_bytes / self.d2s_packets


class Packet:
    def __init__(self, time_stamp, length, type):
        h, m, s = str(time_stamp).split(':')
        inSec = float(h) * 3600 + float(m) * 60 + float(s)
        self.time_stamp = inSec
        self.length = length
        self.type = type  # send one two receive


class FlowInfo:
    def __init__(self, ip1, ip2, time_stamp, length):
        self.ip1 = ip1
        self.ip2 = ip2
        self.send = 1
        self.received = 0
        self.countPackets = 1
        self.PacketList = list()
        self.maxPacketLength = 0
        self.minPacketLength = 0
        self.AverageInterArrivalTime = 0
        self.average_packet_length = 0
        self.flow_duration = "00:00:00.000000"
        self.flow_duration = datetime.datetime.strptime(self.flow_duration, "%H:%M:%S.%f")
        self.port1 = get_port(ip1)
        self.port2 = get_port(ip2)
        self.transmitted_data = 0
        self.received_data = 0
        self.first_window_size = -1
        self.transmitted_data_rate = 0
        self.received_data_rate = 0
        self.standard_deviation_of_packet_length = 0
        self.received_to_transmitted_pkts = 0
        self.received_to_transmitted_data = 0
        self.received_to_transmitted_data_rate = 0
        pkt = Packet(time_stamp, length, 1)
        self.PacketList.append(pkt)
        self.start_time = 0
        self.burst_list = list()
        self.min_s2d_packets = 0
        self.max_s2d_packets = 0
        self.avg_s2d_packets = 0
        self.avg_d2s_packets = 0
        self.min_d2s_packets = 0
        self.max_d2s_packets = 0
        self.min_s2d_bytes = 0
        self.max_s2d_bytes = 0
        self.avg_s2d_bytes = 0
        self.avg_d2s_bytes = 0
        self.min_d2s_bytes = 0
        self.max_d2s_bytes = 0
        self.min_s2d_bps = 0
        self.max_s2d_bps = 0
        self.avg_s2d_bps = 0
        self.avg_d2s_bps = 0
        self.min_d2s_bps = 0
        self.max_d2s_bps = 0

        self.min_s2d_pps = 0
        self.max_s2d_pps = 0
        self.avg_s2d_pps = 0
        self.avg_d2s_pps = 0
        self.min_d2s_pps = 0
        self.max_d2s_pps = 0

        self.min_s2d_bpp = 0
        self.max_s2d_bpp = 0
        self.avg_s2d_bpp = 0
        self.avg_d2s_bpp = 0
        self.min_d2s_bpp = 0
        self.max_d2s_bpp = 0

    def calculation(self):
        length_list = list()
        for i in range(0, len(self.PacketList)):
            length_list.append(self.PacketList[i].length)
        if len(self.PacketList) == 1:
            self.standard_deviation_of_packet_length = -1
        else:
            self.standard_deviation_of_packet_length = statistics.stdev(length_list)
        self.flow_duration = 0
        if len(self.PacketList) > 1:
            thelist = list()
            for i in range(0, len(self.PacketList)):
                thelist.append(self.PacketList[i].time_stamp)
            self.AverageInterArrivalTime = average_inter_arrival_time_in_seconds(thelist)
            self.flow_duration = flow_duration_in_sec(thelist)
            send_packet_time_list = list()
            received_packet_time_list = list()
            for i in range(0, len(self.PacketList)):
                if self.PacketList[i].type == 1:
                    send_packet_time_list.append(self.PacketList[i].time_stamp)
                else:
                    received_packet_time_list.append(self.PacketList[i].time_stamp)

            transmitted_flow_duration = flow_duration_in_sec(send_packet_time_list)
            received_flow_duration = flow_duration_in_sec(received_packet_time_list)

        total_data = 0
        for i in range(0, len(self.PacketList)):
            total_data = total_data + self.PacketList[i].length
        self.minPacketLength = min(length_list)
        self.maxPacketLength = max(length_list)
        self.average_packet_length = total_data / len(length_list)
        for i in range(0, len(self.PacketList)):
            if self.PacketList[i].type == 1:
                self.transmitted_data = self.transmitted_data + self.PacketList[i].length
            else:
                self.received_data = self.received_data + self.PacketList[i].length

        if self.send > 1:
            self.transmitted_data_rate = self.transmitted_data / transmitted_flow_duration
            self.received_to_transmitted_pkts = self.received / self.send
        if self.average_packet_length != -1 and self.transmitted_data > 0:
            self.received_to_transmitted_data = self.received_data / self.transmitted_data
        if self.average_packet_length != -1 and self.transmitted_data_rate > 0:
            self.received_to_transmitted_data_rate = self.received_data_rate / self.transmitted_data_rate
        if self.received > 1:
            self.received_data_rate = self.received_data / received_flow_duration

    def print_features(self, file):
        t = self.AverageInterArrivalTime
        one_line = "Flows b/w " + self.ip1 + " & " + self.ip2
        file.write("%s\n" % one_line)
        one_line = "Total Packets: " + str(self.countPackets)
        file.write("%s\n" % one_line)
        one_line = "Minimum Packet length: " + str(self.minPacketLength) + " bytes."
        file.write("%s\n" % one_line)
        one_line = "Maximum Packet length: " + str(self.maxPacketLength) + " bytes."
        file.write("%s\n" % one_line)
        one_line = "Ports are " + str(self.port1) + " and " + str(self.port2)
        file.write("%s\n" % one_line)
        one_line = "Transmitted Packets: " + str(self.send)
        file.write("%s\n" % one_line)
        one_line = "Received Packets: " + str(self.received)
        file.write("%s\n" % one_line)
        one_line = "Total data transmitted: " + str(self.transmitted_data) + " bytes"
        file.write("%s\n" % one_line)
        one_line = "Total data received: " + str(self.received_data) + " bytes"
        file.write("%s\n" % one_line)
        if self.send > 1:
            one_line = "Transmitted data rate: " + str(self.transmitted_data_rate) + " bytes/sec"
            file.write("%s\n" % one_line)
        else:
            one_line = "Only one packet transmitted, therefore no data rate"
            file.write("%s\n" % one_line)

        if self.received > 1:
            one_line = "Received data rate: " + str(self.received_data_rate) + " bytes/sec"
            file.write("%s\n" % one_line)
        else:
            one_line = "Only one packet received, therefore no data rate"
            file.write("%s\n" % one_line)
        if self.send > 0 and self.received > 0:
            one_line = "Received to transmitted packets (ratio): " + str(self.received_to_transmitted_pkts)
            file.write("%s\n" % one_line)
        else:
            one_line = "Received to transmitted packets (ratio): " + str(0)
            file.write("%s\n" % one_line)
        if self.average_packet_length == -1:
            one_line = "Received to transmitted data ratio cannot be determined. Length not mentioned "
            file.write("%s\n" % one_line)
        else:
            one_line = "Received to transmitted data (ratio): " + str(self.received_to_transmitted_data)
            file.write("%s\n" % one_line)
        if self.received_to_transmitted_data_rate > 0:
            one_line = "Received to transmitted data rate (ratio): " + str(self.received_to_transmitted_data_rate)
            file.write("%s\n" % one_line)
        else:
            one_line = "Received to transmitted data rate cannot be determined. Length not mentioned "
            file.write("%s\n" % one_line)
        if self.first_window_size > 0:
            one_line = "Window size of first packet in flow: " + str(self.first_window_size) + " bytes"
            file.write("%s\n" % one_line)
        else:
            one_line = "Window size not mentioned in the packet"
            file.write("%s\n" % one_line)

        if self.countPackets == 1:
            one_line = "Receive only one packet. So, no Flow duration."
            file.write("%s\n" % one_line)
            one_line = "Receive only one packet. So, no Inter-Arrival time "
            file.write("%s\n" % one_line)
        else:
            one_line = "Flow duration: " + str(self.flow_duration) + " sec "
            file.write("%s\n" % one_line)
            one_line = "Average-Inter Arrival Time: " + str(t) + " sec "
            file.write("%s\n" % one_line)
        if self.average_packet_length == -1:
            one_line = "Packet Length not mentioned"
            file.write("%s\n" % one_line)
        else:
            one_line = "Average Packet Length: " + str(self.average_packet_length) + " bytes."
            file.write("%s\n" % one_line)
        one_line = "Standard Deviation of Packet lengths: " + str(self.standard_deviation_of_packet_length)
        file.write("%s\n" % one_line)

    def print_features_for_Classification(self, file):
        t = self.AverageInterArrivalTime

        '''
        one_line = self.ip1
        file.write("%s\n" % one_line)
        one_line = self.ip2
        file.write("%s\n" % one_line)
        '''
        one_line = str(self.port1)
        file.write("%s\n" % one_line)
        one_line = str(self.port2)
        file.write("%s\n" % one_line)
        one_line = str(self.countPackets)
        file.write("%s\n" % one_line)
        one_line = str(self.minPacketLength)
        file.write("%s\n" % one_line)
        one_line = str(self.maxPacketLength)
        file.write("%s\n" % one_line)
        one_line = str(self.send)
        file.write("%s\n" % one_line)
        one_line = str(self.received)
        file.write("%s\n" % one_line)
        one_line = str(self.transmitted_data)
        file.write("%s\n" % one_line)
        one_line = str(self.received_data)
        file.write("%s\n" % one_line)
        if self.send > 1:
            one_line = str(self.transmitted_data_rate)
            file.write("%s\n" % one_line)
        else:
            one_line = str("-2")
            file.write("%s\n" % one_line)

        if self.received > 1:
            one_line = str(self.received_data_rate)
            file.write("%s\n" % one_line)
        else:
            one_line = "-2"
            file.write("%s\n" % one_line)
        if self.send > 0 and self.received > 0:
            one_line = str(self.received_to_transmitted_pkts)
            file.write("%s\n" % one_line)
        else:
            one_line = str(0)
            file.write("%s\n" % one_line)
        if self.average_packet_length == -1:
            one_line = "-1"
            file.write("%s\n" % one_line)
        else:
            one_line = str(self.received_to_transmitted_data)
            file.write("%s\n" % one_line)
        if self.received_to_transmitted_data_rate > 0:
            one_line = str(self.received_to_transmitted_data_rate)
            file.write("%s\n" % one_line)
        else:
            one_line = "-1"
            file.write("%s\n" % one_line)

        if self.first_window_size > 0:
            one_line = str(self.first_window_size)
            file.write("%s\n" % one_line)
        else:
            one_line = "-1"
            file.write("%s\n" % one_line)

        if self.countPackets == 1:
            one_line = "-2"
            file.write("%s\n" % one_line)
            one_line = "-2"
            file.write("%s\n" % one_line)
        else:
            one_line = str(self.flow_duration)
            file.write("%s\n" % one_line)
            one_line = str(t)
            file.write("%s\n" % one_line)
        if self.average_packet_length == -1:
            one_line = "-1"
            file.write("%s\n" % one_line)
        else:
            one_line = str(self.average_packet_length)
            file.write("%s\n" % one_line)
        one_line = str(self.standard_deviation_of_packet_length)
        file.write("%s\n" % one_line)

    def set_lists(self, time_stamp, pack_length, type):
        pkt = Packet(time_stamp, int(pack_length), type)
        self.PacketList.append(pkt)
        self.countPackets = self.countPackets + 1

    def new_feature_set_extraction(self):

        t = 0
        if self.flow_duration > 3:
            curr = self.PacketList[0].time_stamp
            start = curr
            while (curr + 3) < (start + self.flow_duration):
                obj = Burst(curr, curr + 3)
                curr = curr + 3
                while self.PacketList[t].time_stamp < curr:
                    obj.Packets.append(self.PacketList[t])
                    t = t + 1

                self.burst_list.append(obj)

    def print_bursts(self, file):
        if self.flow_duration > 3:

            one_line = "Max_s2d_packets : " + str(self.max_s2d_packets)
            file.write("%s\n" % one_line)
            one_line = "Min_s2d_packets : " + str(self.min_s2d_packets)
            file.write("%s\n" % one_line)
            one_line = "Avg_s2d_packets : " + str(self.avg_s2d_packets)
            file.write("%s\n" % one_line)
            one_line = "Max_d2s_packets : " + str(self.max_d2s_packets)
            file.write("%s\n" % one_line)
            one_line = "Min_d2s_packets : " + str(self.min_d2s_packets)
            file.write("%s\n" % one_line)
            one_line = "Avg_d2s_packets : " + str(self.avg_d2s_packets)
            file.write("%s\n" % one_line)

            one_line = "Max_s2d_bytes : " + str(self.max_s2d_bytes)
            file.write("%s\n" % one_line)
            one_line = "Min_s2d_bytes : " + str(self.min_s2d_bytes)
            file.write("%s\n" % one_line)
            one_line = "Avg_s2d_bytes : " + str(self.avg_s2d_bytes)
            file.write("%s\n" % one_line)
            one_line = "Max_d2s_bytes : " + str(self.max_d2s_bytes)
            file.write("%s\n" % one_line)
            one_line = "Min_d2s_bytes : " + str(self.min_d2s_bytes)
            file.write("%s\n" % one_line)
            one_line = "Avg_d2s_bytes : " + str(self.avg_d2s_bytes)
            file.write("%s\n" % one_line)

            one_line = "Max_s2d_bps : " + str(self.max_s2d_bps)
            file.write("%s\n" % one_line)
            one_line = "Min_s2d_bps : " + str(self.min_s2d_bps)
            file.write("%s\n" % one_line)
            one_line = "Avg_s2d_bps : " + str(self.avg_s2d_bps)
            file.write("%s\n" % one_line)
            one_line = "Max_d2s_bps : " + str(self.max_d2s_bps)
            file.write("%s\n" % one_line)
            one_line = "Min_d2s_bps : " + str(self.min_d2s_bps)
            file.write("%s\n" % one_line)
            one_line = "Avg_d2s_bps : " + str(self.avg_d2s_bps)
            file.write("%s\n" % one_line)

            one_line = "Max_s2d_pps : " + str(self.max_s2d_pps)
            file.write("%s\n" % one_line)
            one_line = "Min_s2d_pps : " + str(self.min_s2d_pps)
            file.write("%s\n" % one_line)
            one_line = "Avg_s2d_pps : " + str(self.avg_s2d_pps)
            file.write("%s\n" % one_line)
            one_line = "Max_d2s_pps : " + str(self.max_d2s_pps)
            file.write("%s\n" % one_line)
            one_line = "Min_d2s_pps : " + str(self.min_d2s_pps)
            file.write("%s\n" % one_line)
            one_line = "Avg_d2s_pps : " + str(self.avg_d2s_pps)
            file.write("%s\n" % one_line)

            one_line = "Max_s2d_bpp : " + str(self.max_s2d_bpp)
            file.write("%s\n" % one_line)
            one_line = "Min_s2d_bpp : " + str(self.min_s2d_bpp)
            file.write("%s\n" % one_line)
            one_line = "Avg_s2d_bpp : " + str(self.avg_s2d_bpp)
            file.write("%s\n" % one_line)
            one_line = "Max_d2s_bpp : " + str(self.max_d2s_bpp)
            file.write("%s\n" % one_line)
            one_line = "Min_d2s_bpp : " + str(self.min_d2s_bpp)
            file.write("%s\n" % one_line)
            one_line = "Avg_d2s_bpp : " + str(self.avg_d2s_bpp)
            file.write("%s\n" % one_line)


        else:
            one_line = " flow duration was less than 3 seconds, so no burst would be considered"
            file.write("%s\n" % one_line)

    def print_bursts_for_Classification(self, file):
        one_line = str(self.max_s2d_packets)
        file.write("%s\n" % one_line)
        one_line = str(self.min_s2d_packets)
        file.write("%s\n" % one_line)
        one_line = str(self.avg_s2d_packets)
        file.write("%s\n" % one_line)
        one_line = str(self.max_d2s_packets)
        file.write("%s\n" % one_line)
        one_line = str(self.min_d2s_packets)
        file.write("%s\n" % one_line)
        one_line = str(self.avg_d2s_packets)
        file.write("%s\n" % one_line)

        one_line = str(self.max_s2d_bytes)
        file.write("%s\n" % one_line)
        one_line = str(self.min_s2d_bytes)
        file.write("%s\n" % one_line)
        one_line = str(self.avg_s2d_bytes)
        file.write("%s\n" % one_line)
        one_line = str(self.max_d2s_bytes)
        file.write("%s\n" % one_line)
        one_line = str(self.min_d2s_bytes)
        file.write("%s\n" % one_line)
        one_line = str(self.avg_d2s_bytes)
        file.write("%s\n" % one_line)

        one_line = str(self.max_s2d_bps)
        file.write("%s\n" % one_line)
        one_line = str(self.min_s2d_bps)
        file.write("%s\n" % one_line)
        one_line = str(self.avg_s2d_bps)
        file.write("%s\n" % one_line)
        one_line = str(self.max_d2s_bps)
        file.write("%s\n" % one_line)
        one_line = str(self.min_d2s_bps)
        file.write("%s\n" % one_line)
        one_line = str(self.avg_d2s_bps)
        file.write("%s\n" % one_line)

        one_line = str(self.max_s2d_pps)
        file.write("%s\n" % one_line)
        one_line = str(self.min_s2d_pps)
        file.write("%s\n" % one_line)
        one_line = str(self.avg_s2d_pps)
        file.write("%s\n" % one_line)
        one_line = str(self.max_d2s_pps)
        file.write("%s\n" % one_line)
        one_line = str(self.min_d2s_pps)
        file.write("%s\n" % one_line)
        one_line = str(self.avg_d2s_pps)
        file.write("%s\n" % one_line)

        one_line = str(self.max_s2d_bpp)
        file.write("%s\n" % one_line)
        one_line = str(self.min_s2d_bpp)
        file.write("%s\n" % one_line)
        one_line = str(self.avg_s2d_bpp)
        file.write("%s\n" % one_line)
        one_line = str(self.max_d2s_bpp)
        file.write("%s\n" % one_line)
        one_line = str(self.min_d2s_bpp)
        file.write("%s\n" % one_line)
        one_line = str(self.avg_d2s_bpp)
        file.write("%s\n" % one_line)
        one_line = str(self.start_time)
        file.write("%s\n" % one_line)

    def burst_calculation(self):

        if self.flow_duration > 3:
            self.min_s2d_packets = math.inf
            self.min_d2s_packets = math.inf
            self.min_s2d_bytes = math.inf
            self.min_d2s_bytes = math.inf
            self.min_s2d_bps = math.inf
            self.min_d2s_bps = math.inf
            self.min_s2d_pps = math.inf
            self.min_d2s_pps = math.inf
            self.min_s2d_bpp = math.inf
            self.min_d2s_bpp = math.inf

            sum_s2d_packets = 0
            sum_d2s_packets = 0
            sum_s2d_bytes = 0
            sum_d2s_bytes = 0
            sum_s2d_bps = 0
            sum_d2s_bps = 0
            sum_s2d_pps = 0
            sum_d2s_pps = 0
            sum_s2d_bpp = 0
            sum_d2s_bpp = 0

            for i in range(0, len(self.burst_list)):
                self.burst_list[i].calculations()

                sum_s2d_packets = sum_s2d_packets + self.burst_list[i].s2d_packets
                sum_d2s_packets = sum_d2s_packets + self.burst_list[i].d2s_packets
                sum_s2d_bytes = sum_s2d_bytes + self.burst_list[i].s2d_bytes
                sum_d2s_bytes = sum_d2s_bytes + self.burst_list[i].d2s_bytes
                sum_s2d_bps = sum_s2d_bps + self.burst_list[i].s2d_bps
                sum_d2s_bps = sum_d2s_bps + self.burst_list[i].d2s_bps
                sum_s2d_pps = sum_s2d_pps + self.burst_list[i].s2d_pps
                sum_d2s_pps = sum_d2s_pps + self.burst_list[i].d2s_pps
                sum_s2d_bpp = sum_s2d_bpp + self.burst_list[i].s2d_bpp
                sum_d2s_bpp = sum_d2s_bpp + self.burst_list[i].d2s_bpp

                if self.min_s2d_packets > self.burst_list[i].s2d_packets:
                    self.min_s2d_packets = self.burst_list[i].s2d_packets
                if self.max_s2d_packets < self.burst_list[i].s2d_packets:
                    self.max_s2d_packets = self.burst_list[i].s2d_packets
                if self.min_d2s_packets > self.burst_list[i].d2s_packets:
                    self.min_d2s_packets = self.burst_list[i].d2s_packets
                if self.max_d2s_packets < self.burst_list[i].d2s_packets:
                    self.max_d2s_packets = self.burst_list[i].d2s_packets

                if self.min_s2d_bytes > self.burst_list[i].s2d_bytes:
                    self.min_s2d_bytes = self.burst_list[i].s2d_bytes
                if self.max_s2d_bytes < self.burst_list[i].s2d_bytes:
                    self.max_s2d_bytes = self.burst_list[i].s2d_bytes
                if self.min_d2s_bytes > self.burst_list[i].d2s_bytes:
                    self.min_d2s_bytes = self.burst_list[i].d2s_bytes
                if self.max_d2s_bytes < self.burst_list[i].d2s_bytes:
                    self.max_d2s_bytes = self.burst_list[i].d2s_bytes

                if self.min_s2d_bps > self.burst_list[i].s2d_bps:
                    self.min_s2d_bps = self.burst_list[i].s2d_bps
                if self.max_s2d_bps < self.burst_list[i].s2d_bps:
                    self.max_s2d_bps = self.burst_list[i].s2d_bps
                if self.min_d2s_bps > self.burst_list[i].d2s_bps:
                    self.min_d2s_bps = self.burst_list[i].d2s_bps
                if self.max_d2s_bps < self.burst_list[i].d2s_bps:
                    self.max_d2s_bps = self.burst_list[i].d2s_bps

                if self.min_s2d_bpp > self.burst_list[i].s2d_bpp:
                    self.min_s2d_bpp = self.burst_list[i].s2d_bpp
                if self.max_s2d_bpp < self.burst_list[i].s2d_bpp:
                    self.max_s2d_bpp = self.burst_list[i].s2d_bpp
                if self.min_d2s_bpp > self.burst_list[i].d2s_bpp:
                    self.min_d2s_bpp = self.burst_list[i].d2s_bpp
                if self.max_d2s_bpp < self.burst_list[i].d2s_bpp:
                    self.max_d2s_bpp = self.burst_list[i].d2s_bpp

                if self.min_s2d_pps > self.burst_list[i].s2d_pps:
                    self.min_s2d_pps = self.burst_list[i].s2d_pps
                if self.max_s2d_pps < self.burst_list[i].s2d_pps:
                    self.max_s2d_pps = self.burst_list[i].s2d_pps
                if self.min_d2s_pps > self.burst_list[i].d2s_pps:
                    self.min_d2s_pps = self.burst_list[i].d2s_pps
                if self.max_d2s_pps < self.burst_list[i].d2s_pps:
                    self.max_d2s_pps = self.burst_list[i].d2s_pps

            self.avg_s2d_packets = sum_s2d_packets / len(self.burst_list)
            self.avg_d2s_packets = sum_d2s_packets / len(self.burst_list)
            self.avg_s2d_bytes = sum_s2d_bytes / len(self.burst_list)
            self.avg_d2s_bytes = sum_d2s_bytes / len(self.burst_list)
            self.avg_s2d_bps = sum_s2d_bps / len(self.burst_list)
            self.avg_d2s_bps = sum_d2s_bps / len(self.burst_list)
            self.avg_s2d_pps = sum_s2d_pps / len(self.burst_list)
            self.avg_d2s_pps = sum_d2s_pps / len(self.burst_list)
            self.avg_s2d_bpp = sum_s2d_bpp / len(self.burst_list)
            self.avg_d2s_bpp = sum_d2s_bpp / len(self.burst_list)

    '''
    def print(self):
        if self.flow_duration > 3:
            print("Duration : "+str(self.flow_duration))
            print("Total bursts : " + str(len(self.burst_list)))
    '''

    def test(self):
        if self.flow_duration == 9.041398999994271:
            for i in range(0, len(self.burst_list)):
                for j in range(0, len(self.burst_list[i].Packets)):
                    print("Packet : " + str(j + 1)
                          + " ts : " + str(self.burst_list[i].Packets[j].time_stamp)
                          + " length : " + str(self.burst_list[i].Packets[j].length) + "  t: " + str(
                        self.burst_list[i].Packets[j].type))
                print("-------------------------------------")
            return 1
        return 0


def flow_duration_in_sec(thelist):
    # print(len(thelist))
    if (len(thelist) > 1):
        start = thelist[0]
        end = thelist[len(thelist) - 1]

        diff = end - start
        return diff
    else:
        return 0


def average_inter_arrival_time_in_seconds(time_stamp_list):
    thelist = time_stamp_list
    sum = 0
    for i in range(len(thelist) - 1):
        if thelist[i] > thelist[i + 1]:
            sum = (thelist[i] - thelist[i + 1])
        else:
            sum = sum + (thelist[i + 1] - thelist[i])

    inSec = sum / len(thelist)
    return inSec


def get_port(address):
    parts = address.split(".")
    port_str = parts[len(parts) - 1].replace(":", "")
    if port_str.isdigit():
        port = int(port_str)
    else:
        port = 0
    return port


def time_in_sec(time_st):
    h, m, s = str(time_st).split(':')
    inSec = float(h) * 3600 + float(m) * 60 + float(s)
    return inSec


def extract(string, start='(', stop=')'):
    a = string[string.find(start) + 1:string.find(stop)]
    return a


def removeport(address):
    # print(address)
    list_dot_sep = address.split(".")
    ip = list_dot_sep[0] + "." + list_dot_sep[1] + "." + list_dot_sep[2] + "." + list_dot_sep[3]
    return ip


# from datetime import datetime
def start_func():
    global startButton
    startButton.config(state="disabled")
    global sp
    sp = subprocess.Popen(['tcpdump', '-w', 'test.pcap'], shell=False)


def back_from_features_extractor_func():
    global window
    global route
    window.destroy()
    if route == 1:
        main1_function(1)
    else:
        main2_function(1)


def details_func():
    global np
    a = np.get()
    a = int(a)

    if os.path.isfile('text.txt'):
        os.remove('text.txt')

        a = np.get()
        a = int(a)

    flow_list = maintain_stats(a)

    if (len(flow_list) > 0):

        global window
        global root
        root.destroy()
        window = Tk()
        window.title("Features Extracted from Collected Flows")
        w = 1090
        h = 400
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        window.geometry('%dx%d+%d+%d' % (w, h, x, y))

        top = Frame(window)
        top.pack(side=BOTTOM)

        back = Frame(master=window)
        back.pack()
        canvas = Canvas(back)
        canvas.pack(side=LEFT)

        table = Frame(canvas, width=100, height=100, )
        canvas.create_window((0, 0), window=table, anchor='nw')
        table.pack(side=BOTTOM)

        tree = ttk.Treeview(table, selectmode="extended", columns=("A", "B", "C", "D", "E", "F", "G"))

        tree.pack(expand=YES, fill=BOTH)
        tree.heading("#0", text="")
        tree.column("#0", minwidth=0, width=10, stretch=NO)
        tree.heading("A", text="Source IP")
        tree.column("A", minwidth=0, width=170, stretch=NO)
        tree.heading("B", text="Destination IP")
        tree.column("B", minwidth=0, width=170, stretch=NO)
        tree.heading("C", text="Src. Port")
        tree.column("C", minwidth=0, width=130, stretch=NO)
        tree.heading("D", text="Dest. Port")
        tree.column("D", minwidth=0, width=130, stretch=NO)
        tree.heading("E", text="Flow Duration")
        tree.column("E", minwidth=0, width=130, stretch=NO)
        tree.heading("F", text="Total Packets")
        tree.column("F", minwidth=0, width=130, stretch=NO)
        tree.heading("G", text="Avg. Pkt Length")
        tree.column("G", minwidth=0, width=130, stretch=NO)

        tree.pack()

        total_pkts = 0
        for i in range(0, len(flow_list)):
            temp = float(flow_list[i].flow_duration)

            temp1 = round(temp, 3)

            temp2 = float(flow_list[i].average_packet_length)
            temp3 = round(temp2, 3)

            total_pkts = total_pkts + flow_list[i].countPackets

            tree.insert("", i, iid=None, values=(
            removeport(flow_list[i].ip1), removeport(flow_list[i].ip2), flow_list[i].port1, flow_list[i].port2,
            str(temp1),
            flow_list[i].countPackets, temp3))

        var = StringVar()
        label = Label(window, textvariable=var, relief=FLAT)
        var.set("Total flows : " + str(len(flow_list)))
        label.config(height=2, width=60)
        label.place(x=320, y=240)

        var = StringVar()
        label = Label(window, textvariable=var, relief=FLAT)
        var.set("Total packets : " + str(total_pkts))
        label.config(height=2, width=60)
        label.place(x=320, y=280)

        backButton = Button(window, text="Back", font=("Arial", 11), command=back_from_features_extractor_func,
                            fg="#f2f2f2", bg="#333333")
        backButton.place(x=500, y=320)
        backButton.config(height=1, width=13)

    else:
        global startButton
        global stopButton
        startButton.config(state=NORMAL)
        stopButton.config(state=NORMAL)

        messagebox.showinfo("Alert", "No packet Captured yet!")


def stop_func():
    global sp
    global stopButton
    sp.terminate()
    stopButton.config(state="disabled")
    result = subprocess.run(['bash', 'demo.sh'])
    global checkCap
    checkCap = 1
    global fname
    fname = "test.pcap"


def maintain_stats(a):
    global ch
    ch = 1
    uniquemap = dict()
    flow_list = list()
    Total_packets = 0
    Total_bytes = 0
    first_check = 0
    count = 0
    with open('stats', encoding="Latin-1") as f:
        for line in f:
            list_space_separated = line.split(" ")
            start_t = list_space_separated[0]
            if len(list_space_separated) > 3:
                t = 1
                packet_length = -1
                list_comma_seperated = line.split(",")
                last_element = list_comma_seperated[len(list_comma_seperated) - 1]

                if "length" in last_element:
                    arr = re.findall(r'\d+', last_element)
                    packet_length = arr[0]
                else:
                    if last_element.find("(") and last_element.find(")"):
                        list_space_sep = line.split(" ")
                        last = list_space_sep[len(list_space_sep) - 1]
                        if last.find("(") and last.find(")"):
                            packet_length = extract(last)
                            if packet_length != int:
                                count = count + 1
                                packet_length = 0
                        else:
                            packet_length = 0
                substr = "win"
                index = line.find(substr)
                win_size = -1
                if index > 0:
                    new_Str = line[index:index + 13]
                    temp = re.findall('\d+', new_Str)
                    win_size = int(temp[0])

                if first_check == 0:
                    first_check = 1
                    starting_time = list_space_separated[0]
                if "Request who-has" in line:
                    print(list_space_separated[4])
                    print(list_space_separated[6])

                    source = str(list_space_separated[4])
                    destination = str(list_space_separated[6]).replace(",", "")
                    if destination == "tell":
                        destination = destination = str(list_space_separated[7]).replace(":", "")
                    removeport(source)
                    removeport(destination)

                else:

                    if ("Reply" not in list_space_separated[2]) and "IP6" != list_space_separated[1]:
                        # print(list_space_separated[2])
                        # print(list_space_separated[4])
                        # print("-------")
                        source = str(list_space_separated[2]).replace(":", "")
                        destination = str(list_space_separated[4]).replace(":", "")
                        if destination == "tell":
                            destination = destination = str(list_space_separated[4]).replace(":", "")
                        removeport(source)
                        removeport(destination)
                    else:
                        t = -1

                ending_time = list_space_separated[0]
                pair1 = (source, destination)
                pair2 = (destination, source)
                new_list = list()
                if t == -1:
                    t = 1
                else:
                    if not pair1 in uniquemap:
                        if not pair2 in uniquemap:

                            new_list.append(list_space_separated[0])
                            uniquemap.update({pair1: new_list})
                            if packet_length != -1:
                                Total_bytes = Total_bytes + int(packet_length)
                            Flow = FlowInfo(source, destination, list_space_separated[0], int(packet_length))
                            Flow.start_time = start_t
                            Total_packets = Total_packets + 1
                            if win_size > 0:
                                Flow.first_window_size = win_size

                            flow_list.append(Flow)
                        else:
                            temp_lists = list()
                            temp_lists = uniquemap.get(pair2)
                            L=len(temp_lists)

                            if a==1 and L>=5 or a==2 and L>=10 or a==3 and L>=15:
                                print("s")
                            else:
                                temp_lists.append(list_space_separated[0])
                                uniquemap.update({pair2: temp_lists})
                                index = 0
                                for k in range(0, len(flow_list)):
                                    if flow_list[k].ip2 == source and flow_list[k].ip1 == destination:
                                        index = k
                                if packet_length != -1:
                                    Total_packets = Total_packets + 1

                                Total_bytes = Total_bytes + int(packet_length)
                                flow_list[index].set_lists(list_space_separated[0], packet_length, 2)
                                flow_list[index].received = flow_list[index].received + 1


                    else:
                        temp_lists = list()
                        temp_lists = uniquemap.get(pair1)
                        L = len(temp_lists)
                        if a == 1 and L >=5 or a == 2 and L >=10 or a == 3 and L >=15:
                            print("q")
                        else:
                            temp_lists.append(list_space_separated[0])
                            uniquemap.update({pair1: temp_lists})
                            index = 0
                            for k in range(0, len(flow_list)):
                                if flow_list[k].ip1 == source and flow_list[k].ip2 == destination:
                                    index = k
                            flow_list[index].set_lists(list_space_separated[0], packet_length, 1)
                            flow_list[index].send = flow_list[index].send + 1
                            Total_bytes = Total_bytes + int(packet_length)
                            if packet_length != -1:
                                Total_packets = Total_packets + 1


    if len(uniquemap) > 0:
        starting_time_in_seconds = time_in_sec(starting_time)
        ending_time_in_seconds = time_in_sec(ending_time)

        duration_of_session = ending_time_in_seconds - starting_time_in_seconds

        Avg_bps = Total_bytes * 8 / duration_of_session
        Avg_pps = Total_packets / duration_of_session
        if Total_packets != 0:
            Avg_bpp = Total_bytes / Total_packets

        file = open('text.txt', 'w')
        Total_flows = len(uniquemap)

        for j in range(len(flow_list)):
            flow_list[j].calculation()
            flow_list[j].new_feature_set_extraction()
            flow_list[j].burst_calculation()
            flow_list[j].print_features_for_Classification(file)
            flow_list[j].print_bursts_for_Classification(file)
            one_line = "--------------------------------------------- "
            file.write("%s\n" % one_line)

        return flow_list

    else:
        global startButton
        global stopButton
        startButton.config(state=NORMAL)
        stopButton.config(state=NORMAL)

        messagebox.showinfo("Alert", "No packet Captured yet!")

        return flow_list


def back_func1():
    global win
    win.destroy()


def classify_func():
    global ch
    global checkCap
    if ch == 0:
        if checkCap == 1:
            global np
            a=np.get()
            a=int(a)
            flow_lists = maintain_stats(a)
        else:
            messagebox.showinfo("Alert", "No packet Captured yet!")
            return

    # -----------------------READING LIVE PACKET CAPTURE FILE-----------------------
    npc = np.get()
    npc = int(npc)
    flow_lists = maintain_stats(npc)

    f = open('text.txt', 'r')
    temp = f.read()
    tempt = temp.split('---------------------------------------------')
    f.close()
    tempt.pop()
    s = len(tempt)
    l = list()
    other = 0

    for n in range(0, s):
        t = tempt[n].splitlines()

        if (t[1] == '53' or t[2] == '53' or t[1] == '25' or t[2] == '25' or t[1] == '143' or t[2] == '143' or t[
            1] == '110' or t[2] == '110' or t[1] == '993' or t[2] == '993' or t[1] == '995' or t[2] == '995' or t[
            1] == '465' or t[2] == '465' or t[1] == '67' or t[2] == '68' or t[1] == '25' or t[2] == '25'):
            l.append(n)
            other = other + 1

    for n in range(0, len(l)):
        tempt.pop((l[n] - n))

    labelcounter[8] = other
    if len(tempt)==0:
        p=[]
        t=[]
        predictcounter(p,1,t)
        return

    test_size = len(tempt) - 1
    test_sets = ny.empty([test_size, 48], dtype=ny.float64)
    time = list()

    temp3 = ''
    c = 0
    for i in range(0, test_size):
        temp3 = tempt[c].splitlines()
        c = c + 1

        if (i == 0):
            time.append(temp3[49])
        else:
            time.append(temp3[50])

        for k in range(0, 48):
            test_sets[i][k] = float(temp3[k + 1])

    global v
    a = v.get()
    train1, test1, train_labels1, test_labels1 = train_test_split(feature_set1,
                                                                  labelT1,
                                                                  test_size=0.70,
                                                                  random_state=2)

    train, test, train_labels, test_labels = train_test_split(feature_set,
                                                             labelT,
                                                             test_size=0.50,
                                                             random_state=10)




    if a is '':
        a = 0
    a = int(a)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(train, train_labels)
    p = clf.predict(test)
    print("Decision tree accuracy")
    print(p)
    print(accuracy_score(test_labels, p))
    confusion = confusion_matrix(test_labels, p, labels=[0, 1, 2, 3, 4, 5, 6, 7])
    print("Decision tree")
    print(confusion)












    clf = clf.fit(train1, train_labels1)
    p = clf.predict(test1)
    print("Decision tree accuracy for 5 packets")
    print(p)
    print(accuracy_score(test_labels1, p))

    print(len(feature_set2))
    print(len(labelT2))
    print(len(feature_set3))
    print(len(labelT3))




    if a is 1:
        if npc==4:
            clf = tree.DecisionTreeClassifier()
            clf = clf.fit(feature_set, labelT)
            p = clf.predict(test_sets)

            predictcounter(p, 1, time)

        elif npc==3:
            clf = tree.DecisionTreeClassifier()
            clf = clf.fit(feature_set3, labelT3)
            p = clf.predict(test_sets)
            predictcounter(p, 1, time)
        elif npc==2:
            clf = tree.DecisionTreeClassifier()
            clf = clf.fit(feature_set2, labelT2)
            p = clf.predict(test_sets)
            predictcounter(p, 1, time)
        elif npc==1:
            clf = tree.DecisionTreeClassifier()
            clf = clf.fit(feature_set1, labelT1)
            p = clf.predict(test_sets)
            predictcounter(p, 1, time)





    elif a is 2:
        if npc == 4:
            gnb = GaussianNB()
            model = gnb.fit(feature_set, labelT)
            preds = gnb.predict(test_sets)
            predictcounter(preds, 2, time)
        elif npc==3:
            gnb = GaussianNB()
            model = gnb.fit(feature_set3, labelT3)
            preds = gnb.predict(test_sets)
            predictcounter(preds, 2, time)
        elif npc==2:
            gnb = GaussianNB()
            model = gnb.fit(feature_set2, labelT2)
            preds = gnb.predict(test_sets)
            predictcounter(preds, 2, time)
        elif npc==1:
            gnb = GaussianNB()
            model = gnb.fit(feature_set1, labelT1)
            preds = gnb.predict(test_sets)
            predictcounter(preds, 2, time)




    elif a is 3:
        if npc == 4:
            neral = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(6, 3), random_state=1)
            neral.fit(feature_set, labelT)
            neralp = neral.predict(test_sets)
            predictcounter(neralp, 3, time)
        elif npc==3:
            neral = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(6, 3), random_state=1)
            neral.fit(feature_set3, labelT3)
            neralp = neral.predict(test_sets)
            predictcounter(neralp, 3, time)
        elif npc==2:
            neral = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(6, 3), random_state=1)
            neral.fit(feature_set2, labelT2)
            neralp = neral.predict(test_sets)
            predictcounter(neralp, 3, time)
        elif npc==1:
            neral = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(6, 3), random_state=1)
            neral.fit(feature_set1, labelT1)
            neralp = neral.predict(test_sets)
            predictcounter(neralp, 3, time)


    elif a is 4:
        if npc == 4:
            svm1 = svm.SVC()
            svm1.fit(feature_set, labelT)
            svmp = svm1.predict(test_sets)
            predictcounter(svmp, 4, time)
        elif npc==3:
            svm1 = svm.SVC()
            svm1.fit(feature_set3, labelT3)
            svmp = svm1.predict(test_sets)
            predictcounter(svmp, 4, time)
        elif npc==2:
            svm1 = svm.SVC()
            svm1.fit(feature_set2, labelT2)
            svmp = svm1.predict(test_sets)
            predictcounter(svmp, 4, time)
        elif npc==1:
            svm1 = svm.SVC()
            svm1.fit(feature_set1, labelT1)
            svmp = svm1.predict(test_sets)
            predictcounter(svmp, 4, time)




    '''
    global startButton
    global stopButton
    startButton.config(state=NORMAL)
    stopButton.config(state=NORMAL)
    '''


import os


def selectfile_func():
    global fname
    path = askopenfilename()
    var = StringVar()

    fname = os.path.basename(path)
    os.rename(fname, 'test.pcap')
    result = subprocess.run(['bash', 'demo.sh'])
    os.rename('test.pcap', fname)
    global checkCap
    checkCap = 1


global checkCap
checkCap = 0

from tkinter.filedialog import askopenfilename


def main_function():
    global root
    global startButton
    global stopButton
    global SelectFileButton
    root = Tk()
    root.title("Internet Traffic Classification Tool")
    w = 360
    h = 320
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    startButton = Button(root, text="Live Packet Captures", font=("Arial", 10), command=main1_func, fg="#f2f2f2",
                         bg="#333333")
    startButton.place(x=100, y=90)
    startButton.config(height=1, width=18)

    SelectFileButton = Button(root, text="Select .pcap File", font=("Arial", 10), command=main2_func, fg="#f2f2f2",
                              bg="#333333")
    SelectFileButton.place(x=100, y=140)
    SelectFileButton.config(height=1, width=18)
    root.mainloop()


import datetime


# THIS IS THE FUNCTION TO CALCULATE THE PERCENTAGE
def predictcounter(predict, a, t):
    flow_time = list()

    for i in range(0, 8):
        max = 0
        min = 0

        for n in range(0, len(predict)):
            if (predict[n] == i and min == 0):
                min = t[n]

            if (predict[n] == i):
                max = t[n]

        flow_time.append(min)
        flow_time.append(max)

    for i in range(0, len(predict)):
        labelcounter[predict[i]] = labelcounter[predict[i]] + 1

    for i in range(0, 9):
        max = len(predict) + labelcounter[8]
        labelpercentage[i] = (labelcounter[i] / max) * 100

    if a is 1:
        ti = "Decision Tree Classification"
    elif a is 2:
        ti = "Naive Bayes Classification"
    elif a is 3:
        ti = "SVM Classification"
    elif a is 4:
        ti = "Neural Network Classification"
    global win
    win = Tk()
    win.title(ti)
    w = 900
    h = 400
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))

    backB = Button(win, text="Close", font=("Arial", 10), command=back_func1, fg="#f2f2f2", bg="#333333")
    backB.place(x=340, y=300)
    backB.config(height=1, width=18)

    top = Frame(win)
    top.pack(side=BOTTOM)

    back = Frame(master=win)
    back.pack()
    canvas = Canvas(back)
    canvas.pack(side=LEFT)

    table = Frame(canvas, width=100, height=120, )
    canvas.create_window((0, 0), window=table, anchor='nw')
    table.pack(side=BOTTOM)

    tree = ttk.Treeview(table, selectmode="extended", columns=("A", "B", "C", "D", "E"))

    tree.pack(expand=YES, fill=BOTH)
    tree.heading("#0", text="")
    tree.column("#0", minwidth=0, width=10, stretch=NO)
    tree.heading("A", text=" Application ")
    tree.column("A", minwidth=0, width=170, stretch=NO)
    tree.heading("B", text="Percentage")
    tree.column("B", minwidth=0, width=170, stretch=NO)
    tree.heading("C", text=" Starting time ")
    tree.column("C", minwidth=0, width=170, stretch=NO)
    tree.heading("D", text="Ending time")
    tree.column("D", minwidth=0, width=170, stretch=NO)

    tree.heading("E", text="Duration")
    tree.column("E", minwidth=0, width=170, stretch=NO)

    tree.pack()

    j = 0
    for k in range(0, 8):
        k = k + 1
    for i in range(0, 9):

        temp2 = float(labelpercentage[i])
        temp3 = round(temp2, 3)
        if (i == 8):
            tree.insert("", i, iid=None, values=(label_name[i], temp3, 0, 0, 0))

        else:
            if flow_time[j] == 0:
                flow_time[j] = "00:00:00.000000"
            if flow_time[j + 1] == 0:
                flow_time[j + 1] = "00:00:00.000000"

            print (flow_time[j+1])
            print (flow_time[j])
            diff = 0;
            if flow_time[j]!=0 or flow_time[j + 1]!=0:
                h, m, s = str(flow_time[j]).split(':')
                start = float(h) * 3600 + float(m) * 60 + float(s)
                h, m, s = str(flow_time[j + 1]).split(':')
                end = float(h) * 3600 + float(m) * 60 + float(s)
                diff = end - start



            tree.insert("", i, iid=None, values=(label_name[i], temp3, flow_time[j], flow_time[j + 1], diff))
        j = j + 2

    global fname
    outp = "123" + " Result"
    filee = open(outp, 'w')
    for i in range(0, len(label_name)):
        temp2 = float(labelpercentage[i])
        temp3 = round(temp2, 3)
        one_line = label_name[i] + " : " + str(temp3)  # bidirectional flows
        filee.write("%s\n" % one_line)

    for i in range(0, 8):
        labelcounter[i] = 0

    for i in range(0, 8):
        labelcounter[i] = 0


        # ------------- end -------------------------------


def file_reading(filename, file_data):
    for i in range(0, 8):
        temp1 = ''
        temp = ''
        f = open(filename[i], 'r')
        temp = f.read()
        temp1 = temp.split('--------------------------------')
        f.close()
        temp1.pop()

        s = len(temp1)
        l = list()

        for n in range(0, s):
            t = temp1[n].splitlines()

            if (t[1] == '53' or t[2] == '53' or t[1] == '25' or t[2] == '25' or t[1] == '143' or t[2] == '143' or t[
                1] == '110' or t[2] == '110' or t[1] == '993' or t[2] == '993' or t[1] == '995' or t[2] == '995' or t[
                1] == '465' or t[2] == '465' or t[1] == '67' or t[2] == '68' or t[1] == '25' or t[2] == '25'):
                l.append(n)

        for n in range(0, len(l)):
            temp1.pop((l[n] - n))

        file_data.append(temp1)


def label_data(file_data,label):
    max = 0

    for i in range(0, 8):

        sum = max + len(file_data[i])
        for k in range(max, sum):
            label[k] = i
        max = sum


def label_feature(feature_set, file_data):
    c = 0
    max = 0
    for n in range(0, 8):
        c = 0
        sum = max + len(file_data[n])
        for i in range(max, sum):
            temp3 = ''

            temp3 = file_data[n][c].splitlines()

            c = c + 1

            for k in range(0, 48):
                feature_set[i][k] = float(temp3[k + 1])
        max = sum


global ch
ch = 0

labelcounter = list(range(9))
for i in range(0, 9):
    labelcounter[i] = 0

labelpercentage = list(range(9))
for i in range(0, 9):
    labelcounter[i] = 0


def main1_func():
    global route
    route = 1
    main1_function(0)


def main1_function(choice):
    global root
    global startButton
    global stopButton
    global SelectFileButton
    if choice == 0:
        root.destroy()
    root = Tk()
    root.title("Internet Traffic Classification Tool")
    w = 480
    h = 600
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    startButton = Button(root, text="Start Packet Capturing", font=("Arial", 10), command=start_func, fg="#f2f2f2",
                         bg="#333333")
    startButton.place(x=160, y=70)
    startButton.config(height=1, width=18)

    stopButton = Button(root, text="Stop Packet Capturing", font=("Arial", 10), command=stop_func, fg="#f2f2f2",
                        bg="#333333")
    stopButton.place(x=160, y=100)
    stopButton.config(height=1, width=18)

    detailsButton = Button(root, text="Show Statistics", font=("Arial", 10), command=details_func, fg="#f2f2f2",
                           bg="#333333")
    detailsButton.place(x=180, y=150)
    detailsButton.config(height=1, width=13)

    var = StringVar()
    label = Label(root, textvariable=var, relief=FLAT)
    var.set("Select the required classifier")
    label.config(font=("Arial", 14))
    label.config(height=2, width=24)
    label.place(x=100, y=320)

    global np
    np = StringVar()

    n1 = Radiobutton(root, text="5 packet classification", font=("Arial", 11), variable=np, value=1)
    n1.place(x=30, y=210)
    n1.select()
    n2 = Radiobutton(root, text="10 packet classification", font=("Arial", 11), variable=np, value=2)
    n2.place(x=30, y=240)
    n3 = Radiobutton(root, text="15 packet classification", font=("Arial", 11), variable=np, value=3)
    n3.place(x=30, y=270)
    n4 = Radiobutton(root, text="Complete packet classification", font=("Arial", 11), variable=np, value=4)
    n4.place(x=30, y=290)


    global v
    v = StringVar()

    R1 = Radiobutton(root, text="Decision Tree", font=("Arial", 11), variable=v, value=1)
    R1.place(x=30, y=350)
    R1.select()
    R2 = Radiobutton(root, text="Naive Bayes", font=("Arial", 11), variable=v, value=2)
    R2.place(x=30, y=380)
    R3 = Radiobutton(root, text="Neural Network", font=("Arial", 11), variable=v, value=3)
    R3.place(x=30, y=410)
    R4 = Radiobutton(root, text="SVM Classification", font=("Arial", 11), variable=v, value=4)
    R4.place(x=30, y=440)

    ClassifyButton = Button(root, text="Classify", font=("Arial", 10), command=classify_func, fg="#f2f2f2",
                            bg="#333333")
    ClassifyButton.place(x=180, y=470)
    ClassifyButton.config(height=1, width=13)

    BacktoMainButton = Button(root, text="Back", font=("Arial", 10), command=BackToMain_function, fg="#f2f2f2",
                              bg="#333333")
    BacktoMainButton.place(x=180, y=510)
    BacktoMainButton.config(height=1, width=13)
    root.mainloop()


def BackToMain_function():
    global root
    root.destroy()
    main_function()


def main2_func():
    global route
    route = 2
    main2_function(0)


def main2_function(choice):
    global root
    global startButton
    global stopButton
    global SelectFileButton
    if choice == 0:
        root.destroy()
    root = Tk()
    root.title("Internet Traffic Classification Tool")
    w = 480
    h = 550
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    SelectFileButton = Button(root, text="Select File", font=("Arial", 10), command=selectfile_func, fg="#f2f2f2",
                              bg="#333333")
    SelectFileButton.place(x=180, y=70)
    SelectFileButton.config(height=1, width=13)

    detailsButton = Button(root, text="Show Statistics", font=("Arial", 10), command=details_func, fg="#f2f2f2",
                           bg="#333333")
    detailsButton.place(x=180, y=100)
    detailsButton.config(height=1, width=13)

    var = StringVar()
    label = Label(root, textvariable=var, relief=FLAT)
    var.set("Select the required classifier")
    label.config(font=("Arial", 14))
    label.config(height=2, width=24)
    label.place(x=100, y=310)

    global np
    np = StringVar()

    n1 = Radiobutton(root, text="5 packet classification", font=("Arial", 11), variable=np, value=1)
    n1.place(x=30, y=210)
    n1.select()
    n2 = Radiobutton(root, text="10 packet classification", font=("Arial", 11), variable=np, value=2)
    n2.place(x=30, y=240)
    n3 = Radiobutton(root, text="15 packet classification", font=("Arial", 11), variable=np, value=3)
    n3.place(x=30, y=270)
    n4 = Radiobutton(root, text="Complete packet classification", font=("Arial", 11), variable=np, value=4)
    n4.place(x=30, y=290)



    global v
    v = StringVar()

    R1 = Radiobutton(root, text="Decision Tree", font=("Arial", 11), variable=v, value=1)
    R1.place(x=30, y=350)
    R1.select()
    R2 = Radiobutton(root, text="Naive Bayes", font=("Arial", 11), variable=v, value=2)
    R2.place(x=30, y=380)
    R3 = Radiobutton(root, text="Neural Network", font=("Arial", 11), variable=v, value=3)
    R3.place(x=30, y=410)
    R4 = Radiobutton(root, text="SVM Classification", font=("Arial", 11), variable=v, value=4)
    R4.place(x=30, y=440)

    ClassifyButton = Button(root, text="Classify", font=("Arial", 10), command=classify_func, fg="#f2f2f2",
                            bg="#333333")
    ClassifyButton.place(x=180, y=470)
    ClassifyButton.config(height=1, width=13)

    BacktoMainButton = Button(root, text="Back", font=("Arial", 10), command=BackToMain_function, fg="#f2f2f2",
                              bg="#333333")
    BacktoMainButton.place(x=180, y=510)
    BacktoMainButton.config(height=1, width=13)

    root.mainloop()


file_data = []

label_name = ['Gmail', 'Instagram', 'Netflix', 'Torrent', 'Dropbox', 'Facebook', 'Youtube',
              'Skype', 'DNS/DHCP/SMTP/POP3/IMAP']

FFilename = [ 'GmailForClassification.txt', 'InstagramForClassification.txt',
             'NetflixForClassification.txt', 'TorrentForClassification.txt',
             'DropboxForClassification.txt', 'FacebookForClassification.txt', 'YoutubeForClassification.txt',
             'SkypeForClassification.txt']

file_reading(FFilename, file_data)

Total_lenght = len(file_data[0]) + len(file_data[1]) + len(file_data[2]) + len(file_data[3]) + len(file_data[4]) + len(
    file_data[5]) + len(file_data[6]) + len(file_data[7])

labelT = ny.empty([Total_lenght], dtype=int)

label_data(file_data,labelT)

feature_set = ny.empty([Total_lenght, 48], dtype=ny.float64)

label_feature(feature_set, file_data)

file_data1 = []

FFilename1 = [ 'GmailForClassification5.txt', 'InstagramForClassification5.txt',
             'NetflixForClassification5.txt', 'TorrentForClassification5.txt',
             'DropboxForClassification5.txt', 'FacebookForClassification5.txt', 'YoutubeForClassification5.txt',
             'SkypeForClassification5.txt']

file_reading(FFilename1, file_data1)

Total_lenght1 = len(file_data1[0]) + len(file_data1[1]) + len(file_data1[2]) + len(file_data1[3]) + len(file_data1[4]) + len(
    file_data1[5]) + len(file_data1[6]) + len(file_data1[7])

labelT1 = ny.empty([Total_lenght1], dtype=int)

label_data(file_data1,labelT1)

feature_set1 = ny.empty([Total_lenght1, 48], dtype=ny.float64)

label_feature(feature_set1, file_data1)

file_data2 = []

FFilename2 = [ 'GmailForClassification10.txt', 'InstagramForClassification10.txt',
             'NetflixForClassification10.txt', 'TorrentForClassification10.txt',
             'DropboxForClassification10.txt', 'FacebookForClassification10.txt', 'YoutubeForClassification10.txt',
             'SkypeForClassification10.txt']

file_reading(FFilename2, file_data2)

Total_lenght2 = len(file_data2[0]) + len(file_data2[1]) + len(file_data2[2]) + len(file_data2[3]) + len(file_data2[4]) + len(
    file_data2[5]) + len(file_data2[6]) + len(file_data2[7])

labelT2 = ny.empty([Total_lenght2], dtype=int)

label_data(file_data2,labelT2)

feature_set2 = ny.empty([Total_lenght2, 48], dtype=ny.float64)

label_feature(feature_set2, file_data2)

file_data3 = []

FFilename3 = [ 'GmailForClassification15.txt', 'InstagramForClassification15.txt',
             'NetflixForClassification15.txt', 'TorrentForClassification15.txt',
             'DropboxForClassification15.txt', 'FacebookForClassification15.txt', 'YoutubeForClassification15.txt',
             'SkypeForClassification15.txt']

file_reading(FFilename3, file_data3)

Total_lenght3 = len(file_data3[0]) + len(file_data3[1]) + len(file_data3[2]) + len(file_data3[3]) + len(file_data3[4]) + len(
    file_data3[5]) + len(file_data3[6]) + len(file_data3[7])

labelT3 = ny.empty([Total_lenght3], dtype=int)

label_data(file_data3,labelT3)

feature_set3 = ny.empty([Total_lenght3, 48], dtype=ny.float64)

label_feature(feature_set3, file_data3)

other = 0
global route
main_function()






