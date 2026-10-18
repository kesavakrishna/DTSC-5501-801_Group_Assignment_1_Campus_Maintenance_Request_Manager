import random

from maintenance_request import MaintenanceRequest

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