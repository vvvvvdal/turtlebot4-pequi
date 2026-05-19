# Turtlebot4 (Pequi Mecânico)

## Docker
```bash
# Buildar container
docker build -t tb4_simulador .

# Rodar container
docker run --rm -it \
  --name turtlebot4_simulador \
  --env="DISPLAY=$DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  --network=host \
  tb4_simulador

# Testar Gazebo
ign gazebo
``` 