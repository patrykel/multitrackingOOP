
class MultiTrackRecord:

    def __init__(self, event_id, group_id, combination, hit_lines, solution, method, exec_time_in_s, fishing_distance=None):
        self.event_id = event_id
        self.group_id = group_id
        self.combination = combination
        self.hit_lines = hit_lines
        self.solution = solution
        self.method = method
        self.exec_time_in_s = exec_time_in_s
        self.fishing_distance = fishing_distance
