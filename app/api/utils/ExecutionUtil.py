class ExecutionUtil:
    
    @staticmethod
    def get_state_string(state):
        if state == 0:
            return "waiting"
        elif state == 1:
            return "running"
        elif state == 3:
            return "success"
        else:
            return "error"
