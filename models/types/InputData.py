from typing import dict, Sequence

class AgentPosition():
    posX : int
    posY : int


class InputData():

    def __init__(self,frame_id: int,agent_ids: Sequence[int],agent_positions: dict[int, AgentPosition]) -> None:
        self.frame_id = frame_id
        self.agent_ids = agent_ids
        self.agent_positions = agent_positions

    frame_id: int
    agent_ids : Sequence[int]
    agent_positions: dict[int, AgentPosition]
