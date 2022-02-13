import multiprocessing

manager = multiprocessing.Manager()

AGENTS_LIST = manager.dict()
COLLECTORS_LIST = manager.dict()

def get_collectors_list():
    global COLLECTORS_LIST
    return COLLECTORS_LIST

def update_agents_list(agents):
    global AGENTS_LIST
    global COLLECTORS_LIST
    AGENTS_LIST = agents

    collectors = {}
    for agent in agents.values():
        for c_name, collector in agent.items():
            if not collector["enabled"]:
                continue
            collectors[c_name] = collector["allowed_input"]
    COLLECTORS_LIST = collectors
