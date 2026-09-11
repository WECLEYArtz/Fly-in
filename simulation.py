from components import Graph, Drone, Path, HubTypes


class Simulation:
    def __init__(self, nb_drones:int, graph: Graph):
        self.nb_drones:int = nb_drones
        self.graph: Graph = graph
        self.path_tiers: list[Path] = []

    def id_gen(self):
        for i in range(1,self.nb_drones+1):
            yield i

    def init_drone_paths(self):
        bottleneck_1 = min([e.max_capacity for e in self.path_tiers[0]])
        bottleneck_2 = min([e.max_capacity for e in self.path_tiers[1]])
        second_path_turns = len(self.path_tiers[1]) -1
        bottlenecks = [bottleneck_2, bottleneck_1]

        drone_id_gen = Simulation.id_gen(self)
        paths_ids = [1,0] # try to use bit shifting later, or something cleaner

        turns = 0
        nb_drones = self.nb_drones
        drones_start_hub = self.graph.start_hub.users

        while (nb_drones):
            if turns == 0:
                turns = second_path_turns -1
                bottlenecks.reverse()
                paths_ids.reverse()

            for _ in range(int(bottlenecks[0])): #[ init every drone for the current turn]
                drones_start_hub.append(Drone(next(drone_id_gen), paths_ids[0]))
                nb_drones -= 1
                if not turns:
                    break
            turns -= 1


    def run_simulation(self):
        drones_end_hub = self.graph.end_hub.users
        line_logs: list[str] = []
        while(len(drones_end_hub) < self.nb_drones):
            for path_id, path in enumerate(self.path_tiers):
                # if (not path_id):
                #     print("\n[Debug]: << NEW LOOP >>")
                # print("[Debug]: switching to Path", path_id)
                for hub_id in range(len(path)-2 , -1, -1):
                    # print("[Debug]:    switching to", path[hub_id].name_colored, "in path", path_id, f"{len(path[hub_id].users)}/{path[hub_id].max_capacity}")
                    to_remove:list[Drone] = []
                    for drone in path[hub_id].users:
                        if drone.fly_path_id != path_id:
                            continue
                        # print("[Debug]:      checking drone", drone.id)
                        if hub_id and drone in path[hub_id-1].users:
                            path[hub_id-1].users.remove(drone)
                            path[hub_id-1].max_capacity -= 1
                            line_logs.append(f'D{drone.id}-{path[hub_id].name_colored}')
                        elif len(path[hub_id+1].users) < path[hub_id+1].max_capacity:
                            path[hub_id+1].users.append(drone)
                            if path[hub_id+1].type == HubTypes.RESTRICTED:
                                line_logs.append(f'D{drone.id}-{path[hub_id].name_colored}-{path[hub_id+1].name_colored}')
                                path[hub_id].max_capacity += 1
                            else:
                                line_logs.append(f'D{drone.id}-{path[hub_id+1].name_colored}')
                                to_remove.append(drone)

                    path[hub_id].users = [drone for drone in path[hub_id].users
                                                  if not drone in to_remove]
            if line_logs:
                print(' '.join(line_logs))
                line_logs = []
