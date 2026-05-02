import heapq

class BookingQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def add_customer(self, customer_name, priority):
        # Min-heap uses the first element (priority) to sort
        heapq.heappush(self._queue, (priority, self._index, customer_name))
        self._index += 1

    def serve_next(self):
        if not self._queue:
            return "No customers in queue."
        priority, index, name = heapq.heappop(self._queue)
        status = "Prime" if priority == 1 else "Regular"
        return f"Serving {status} Customer: {name}"
