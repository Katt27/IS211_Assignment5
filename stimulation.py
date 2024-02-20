import csv
from argparse import ArgumentParser

class Request:
    def __init__(self, timestamp, file_name, process_time):
        self.timestamp = timestamp
        self.file_name = file_name
        self.process_time = process_time

class Server:
    def __init__(self):
        self.request_queue = []
        self.current_time = 0
        self.total_wait_time = 0
        self.completed_requests = 0

    def add_request(self, request):
        self.request_queue.append(request)

    def process_next_request(self):
        if self.request_queue:
            next_request = self.request_queue.pop(0)
            wait_time = max(0, self.current_time - next_request.timestamp)
            self.total_wait_time += wait_time
            self.current_time = max(self.current_time, next_request.timestamp) + next_request.process_time
            self.completed_requests += 1

    def calculate_average_wait_time(self):
        if self.completed_requests == 0:
            return 0
        return self.total_wait_time / self.completed_requests

def simulateOneServer(filename):
    server = Server()
    requests = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:
                timestamp, file_name, process_time = int(row[0]), row[1], int(row[2])
                requests.append(Request(timestamp, file_name, process_time))
    
    requests.sort(key=lambda x: x.timestamp)

    for request in requests:
        if server.current_time < request.timestamp:
            server.current_time = request.timestamp
        server.add_request(request)
        server.process_next_request()

    return server.calculate_average_wait_time()

def simulateManyServers(filename, number_of_servers):
    servers = [Server() for _ in range(number_of_servers)]
    requests = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:
                timestamp, file_name, process_time = int(row[0]), row[1], int(row[2])
                requests.append(Request(timestamp, file_name, process_time))
    
    requests.sort(key=lambda x: x.timestamp)

    for i, request in enumerate(requests):
        server = servers[i % number_of_servers]
        if server.current_time < request.timestamp:
            server.current_time = request.timestamp
        server.add_request(request)
        server.process_next_request()

    total_wait_time = sum(server.calculate_average_wait_time() for server in servers) / number_of_servers
    return total_wait_time

def main():
    parser = ArgumentParser(description="Network Request Simulation")
    parser.add_argument("--file", type=str, required=True, help="Path to the CSV file containing network requests")
    parser.add_argument("--servers", type=int, help="Number of servers to simulate. Defaults to 1 if not specified.")

    args = parser.parse_args()

    if args.servers and args.servers > 1:
        average_wait_time = simulateManyServers(args.file, args.servers)
        print(f"Average Wait Time with {args.servers} Servers: {average_wait_time} seconds")
    else:
        average_wait_time = simulateOneServer(args.file)
        print(f"Average Wait Time with One Server: {average_wait_time} seconds")

if __name__ == "__main__":
    main()
