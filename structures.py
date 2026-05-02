# structures.py

class Node:
    def __init__(self, name, seat_no, status):
        self.name = name
        self.seat_no = seat_no
        self.status = status
        self.next = None


class BookingHistory:
    def __init__(self):
        self.head = None

    def add_record(self, name, seat_no, status):
        new_node = Node(name, seat_no, status)

        if not self.head:
            self.head = new_node
            return

        temp = self.head
        while temp.next:
            temp = temp.next

        temp.next = new_node

    def display(self):
        temp = self.head
        result = []

        while temp:
            result.append(f"{temp.name} | Seat {temp.seat_no} | {temp.status}")
            temp = temp.next

        return result if result else ["No history"]
