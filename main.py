import carla
import random
import time

def spawn_vehicles_and_obstacles(client, world, num_vehicles=10, num_obstacles=5):
    blueprint_library = world.get_blueprint_library()

    # Get a random vehicle blueprint
    vehicle_bp = blueprint_library.filter('vehicle.*')[0]

    # Get a random static object blueprint
    obstacle_bp = blueprint_library.filter('static.prop.*')[0]

    spawn_points = world.get_map().get_spawn_points()

    # Spawn vehicles
    vehicles = []
    for _ in range(num_vehicles):
        try:
            spawn_point = random.choice(spawn_points)
            vehicle = world.spawn_actor(vehicle_bp, spawn_point)
            vehicles.append(vehicle)
        except IndexError:
            print("No available spawn points for vehicles.")

    # Spawn obstacles
    obstacles = []
    for _ in range(num_obstacles):
        try:
            spawn_point = random.choice(spawn_points)
            # Slightly adjust the z-coordinate to avoid collision with the ground
            spawn_point.location.z += 0.5
            obstacle = world.spawn_actor(obstacle_bp, spawn_point)
            obstacles.append(obstacle)
        except IndexError:
            print("No available spawn points for obstacles.")

    return vehicles, obstacles

def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    try:
        world = client.get_world()

        # Apply basic weather settings
        weather = carla.WeatherParameters(
            cloudiness=10.0,
            precipitation=0.0,
            sun_altitude_angle=70.0
        )
        world.set_weather(weather)

        # Spawn vehicles and obstacles
        num_vehicles = 10
        num_obstacles = 5
        vehicles, obstacles = spawn_vehicles_and_obstacles(client, world, num_vehicles, num_obstacles)

        print(f"Spawned {len(vehicles)} vehicles and {len(obstacles)} obstacles.")

        # Let the simulation run for a while
        time.sleep(10)

    finally:
        print("Cleaning up actors...")
        actors = world.get_actors()
        for actor in actors:
            if actor.type_id.startswith('vehicle.') or actor.type_id.startswith('static.prop.'):
                actor.destroy()

        print("Actors cleaned up.")

if __name__ == '__main__':
    main()