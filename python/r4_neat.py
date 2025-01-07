import os
import socket

import neat
import neat.genes
import neat.genome

from game_instance import GameCar
import proto.game_pb2 as game_pb2

pi: float = 3.1415926535897932384626433

game_car: GameCar = None


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        step = 0

        # Create neural network
        net = neat.nn.RecurrentNetwork.create(genome, config)

        genome.fitness = 0.0

        # Reset the game
        ## Send packet with Train_flags.reset = True
        reset_packet = game_pb2.ModelOutput()
        reset_packet.train_flags.reset = 1
        game_car.game_socket.sendto(reset_packet.SerializeToString(), (game_car.game_socket_address, game_car.game_socket_port+1))

        last_track_progress = 0
        initial_track_progress = 0

        last_100_speed: list[int] = []

        # Start game loop
        while step < 10000:
            # Update game state
            if not game_car.update():
                continue

            # Check if it's the first step
            if step == 0:
                last_track_progress = game_car.track_info.track_progress
                initial_track_progress = last_track_progress
                last_100_speed.append(game_car.car_info.speed)
                step += 1

            # Check if the game is over
            if game_car.track_info.track_status == 4:
                genome.fitness += 10000.0
                break

            # Fail on wall collision
            if game_car.car_info.collided:
                genome.fitness -= 500.0 * (game_car.car_info.speed/800.0)
                break


            # Check if the cars hasn't moved in the first 100 steps or became too slow
            if step >= 100:
                if initial_track_progress == game_car.track_info.track_progress or sum(last_100_speed) <= 100.0:
                    genome.fitness -= 5000.0
                    break


            # Add fitness in function of the track progress delta and the speed, punishing going the wrong way
            genome.fitness += (game_car.track_info.track_progress - last_track_progress) * (game_car.car_info.speed/6000.0) * (-2 if game_car.car_info.wrong_way else 1)

            # Preprocess game values
            speed = game_car.car_info.speed / 3000.0
            rpm = game_car.car_info.rpm / 10000.0
            gear = game_car.car_info.gear / 6.0

            gear_timeout = game_car.car_info.gear_timeout / 9.0
            accel_lifted_timer = game_car.car_info.accel_lifted_timer / 60.0

            drift_timeout = game_car.car_info.drift_timeout / 100000.0

            rays_distance = []
            for ray in game_car.car_rays.rays:
                rays_distance.append(ray.distance / 3000.0)

            # Feed the neural network
            output = net.activate((
                speed, 
                rpm, 
                gear, 
                gear_timeout, 
                accel_lifted_timer,
                game_car.car_info.traction_loss_fl,
                game_car.car_info.traction_loss_fr,
                game_car.car_info.traction_loss_rl,
                game_car.car_info.traction_loss_rr,
                game_car.car_info.wrong_way,
                game_car.car_info.free_fall,
                drift_timeout, 
                *rays_distance))
            
            # Send the output to the game
            packet = game_pb2.ModelOutput()
            packet.action.accelerate = 1 if output[0] > 0.5 else 0

            # Adjust brake threshold depending if the car will accelerate
            if packet.action.accelerate:
                if output[1] > 0.8:
                    packet.action.brake = 1
            else:
                packet.action.brake = 1 if output[1] > 0.5 else 0

            if output[2] > output[3]:
                if output[2] > 0.5:
                    packet.action.steer_left = 1
                packet.action.steer_right = 0
            else:
                if output[3] > 0.5:
                    packet.action.steer_right = 1
                packet.action.steer_left = 0
            

            packet.model_info.genome = genome_id
            packet.model_info.generation = pop.generation
            packet.model_info.species = pop.species.get_species_id(genome_id)
            packet.model_info.fitness = int(genome.fitness)
            packet.model_info.step = step
            
            packet.train_flags.reset = False

            # print("Sending processed output to game")
            game_car.game_socket.sendto(packet.SerializeToString(), (game_car.game_socket_address, game_car.game_socket_port+1))

            # Update last track progress
            last_track_progress = game_car.track_info.track_progress

            # Update last 100 speed
            last_100_speed.append(game_car.car_info.speed)
            if len(last_100_speed) > 100:
                last_100_speed.pop(0)
            
            step = step + 1

        print(f"Genome {genome_id} fitness: {genome.fitness}")

    pass

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'neat_config.ini')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

pop = neat.Population(config)
stats = neat.StatisticsReporter()
pop.add_reporter(stats)
pop.add_reporter(neat.StdOutReporter(True))

pop.add_reporter(neat.Checkpointer(10, 60*30))

# Wait until we receive a ready packet from the emulator
socket_ready = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_ready.bind(('localhost', 7650))
socket_ready.setblocking(True)
print("Waiting for ready packet from emulator")
data = socket_ready.recv(1024)
if data == b'ready':
    print('Received ready packet from emulator')
socket_ready.close()

# Initialize the game instance
game_car: GameCar = GameCar('localhost', 7652, False,
                3000, 10, 5, pi, True)

pop.run(eval_genomes, 500)