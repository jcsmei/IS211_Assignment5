#!/usr/bin/env python
#! -*- coding: utf-8 -*-
"""IS211_Assignment05. A simple assingment to demostrate the queue structure."""

import argparse
import csv
import urllib2


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help="Enter a valid URL to a CSV file.")
parser.add_argument('-s', '--servers', help="Enter the number of servers.")
args =  parser.parse_args()


def downloadData(url):
        """A function to read CSV file from URL.

        Args:
                url (string): A web URL that links to a CSV file.

        Returns:
                csv_file (various): A CSV data set.

        Example:
                >>> url = downloadData('http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv')
                >>> csv_data = urllib2.urlopen(url)
                >>> df = csv.reader(csv_data)
                >>> for row in df:
                                print row
                ['8', '/external/background.PNG', '1']
                ['9', '/css/main.css', '3']
                ['9', '/images/circle.gif', '1']
                ['9', '/images/main.jpg', '1']
                ...
                ['10005', '/images/main.jpg', '3']
                ['10005', '/css/profile.CSS', '3']
                ['10006', '/html/profile.html', '1']
        """
        csv_file = urllib2.urlopen(url)
        return csv_file


class Queue:
        """A Queue class for sorting according to First In First Out rule.
        """
        def __init__(self):
                self.items = []

        def is_empty(self):
                return self.items == []

        def enqueue(self, item):
                self.items.insert(0, item)

        def dequeue(self):
                return self.items.pop()

        def size(self):
                return len(self.items)


class Server(object):
        """A Server class to for the simulateOneServer function.
        """
        def __init__(self):
                self.current_task =  None
                self.time_remaining = 0

        def tick(self):
                if self.current_task != None:
                        self.time_remaining = self.time_remaining - 1
                        if self.time_remaining <= 0:
                                self.current_task = None

        def busy(self):
                if self.current_task != None:
                        return True
                else:
                        return False

        def start_next(self, new_task):
                self.current_task = new_task
                self.time_remaining = new_task.get_time()


class Request(object):
        """A Request class to simulate server requests.
        """
        def __init__(self, req_sec, process_time):
                self.timestamp = req_sec
                self.process_time = process_time

        def get_stamp(self):
                return self.timestamp

        def get_time(self):
                return self.process_time

        def wait_time(self, current_time):
                return current_time - self.timestamp
                
def simulateOneServer(csv_data):
        """A function to simulate one server request.

        Args:
                csv_data (object): CSV data from the URL as an object.

        Returns:
                (string): A string that prints the average wait time and the tasks in the queue.

        Examples:
        >>> df = downloadData('http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv')
        >>> simulateOneServer(df)
        Average wait time is 2502.00 seconds; 5006 tasks remaining.
        """
        readfile = csv.reader(csv_data)
        lab_server = Server()
        server_queue = Queue()
        waiting_times = []

        for line in readfile:
                req_sec = int(line[0])
                process_time = int(line[2])
                task = Request(req_sec, process_time)
                server_queue.enqueue(task)

                if (not lab_server.busy()) and (not server_queue.is_empty()):
                        next_task = server_queue.dequeue()
                        waiting_times.append(next_task.wait_time(req_sec))
                        lab_server.start_next(next_task)

                lab_server.tick()

        average_wait =  sum(waiting_times) / len(waiting_times)
        print ('Average wait time is %6.2f seconds; %3d tasks remaining.'
               % (average_wait, server_queue.size()))


def simulateManyServers(csv_data, servers):
        """Do something.
        """
        readfile = csv.reader(csv_data)
        lab_server = Server(servers)
        server_queue = Queue()
        waiting_times = []

        for line in readfile:
                req_sec = int(line[0])
                process_time = int(line[2])
                task = Request(req_sec, process_time)
                server_queue.enqueue(task)

                if Request(csv_data):
                        task = Task(line)
                        server_queue.enqueue(task)

                if (not lab_server.busy()) and (not server_queue.is_empty()):
                        next_task = server_queue.dequeue()
                        waiting_times.append(next_task.wait_time(req_sec))
                        lab_server.start_next(next_task)

                lab_server.tick()

        average_wait =  sum(waiting_times) / len(waiting_times)
        print ('Average wait time is %6.2f seconds; %3d tasks remaining.'
               % (average_wait, server_queue.size()))


def main():
        """A function to simulate printing tasks with queue.
        """
        if not args.url:
                print (
                        '''Hi Professor, there are errors in the code.
Not sure how to iterate through the CSV list in new tasks for many servers.
All i found on Google were on multithreading, which is not what we need here.

But the simulateOneServer() function works.
                       ''')
                raise
        try:
                csv_data = downloadData(args.url)
        except urllibs2.URLError:
                print 'Please enter URL for a CSV file.'
                raise
        else:
                if not args.servers:
                        simulateOneServer(csv_data)
                else:
                        simulateManyServers(csv_data, args.servers)

if __name__ ==  '__main__':
        main()
