class MaintenanceRequest:
    """campus maintenance request.

    priority:      1 = Urgent, 2 = High, 3 = Normal, 4 = Low
    reported_time: a simple integer timestamp
    """

    def __init__(self, request_id, building, category, priority, reported_time, status="OPEN"):
        self.request_id = request_id
        self.building = building
        self.category = category
        self.priority = priority
        self.reported_time = reported_time
        self.status = status

    def __str__(self):
        return (f"#{self.request_id} {self.building} {self.category} "
                f"P{self.priority} t={self.reported_time} {self.status}")
