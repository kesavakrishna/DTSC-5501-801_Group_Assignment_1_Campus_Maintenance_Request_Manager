import random

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

BUILDINGS = ["CASE", "ECNW", "ECCR", "AERO", "ATLAS", "NORLIN"]
CATEGORIES = ["HVAC", "Electrical", "Plumbing", "Equipment", "Classroom Tech", "Other"]


def generate_requests(n, seed=42, first_id=1000):
    """Return a list of n MaintenanceRequest objects.
    """
    rng = random.Random(seed)
    ids = rng.sample(range(first_id, first_id + 10 * n), n)
    requests = []
    for request_id in ids:
        request = MaintenanceRequest(
            request_id=request_id,
            building=rng.choice(BUILDINGS),
            category=rng.choice(CATEGORIES),
            priority=rng.randint(1, 4),
            reported_time=rng.randint(0, 5 * n),
        )
        requests.append(request)
    return requests