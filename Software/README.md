# Turtlebot4 (Pequi Mecânico)

## Config para GPU NVIDIA
```bash
# Adicionar chave do repositório da NVIDIA
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Instalar Toolkit (caso falte algo)
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Configurar o Docker para usar a runtime da NVIDIA
sudo nvidia-ctk runtime configure --runtime=docker

# Gerar o arquivo CDI
sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml

# Reiniciar o Docker
sudo systemctl restart docker
```

## Como rodar
```bash
# Dar permissão para uso de interface gráfica
xhost +local:docker

# Buildar container
docker build -t tb4_simulador .

# Rodar container
docker run --rm -it \
  --gpus all \
  --name turtlebot4_simulador \
  --env="DISPLAY=$DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  --volume="$(pwd):/home/dockeruser/ws" \
  --network=host \
  tb4_simulador

# Terminal 1: Turtlebot4 no Gazebo no mapa Warehouse
ros2 launch turtlebot4_ignition_bringup turtlebot4_ignition.launch.py world:=warehouse namespace:=turtlebot1 \
  gui_config:=/home/dockeruser/ws/config_turtlebot1.config

# Terminal 2: SLAM
docker exec -it turtlebot4_simulador bash
ros2 launch turtlebot4_navigation slam.launch.py sync:=true namespace:=turtlebot1

# Terminal 3: Nav2
docker exec -it turtlebot4_simulador bash
ros2 launch turtlebot4_navigation nav2.launch.py namespace:=turtlebot1

# Terminal 4: RViz2
docker exec -it turtlebot4_simulador bash
ros2 launch turtlebot4_viz view_robot.launch.py namespace:=turtlebot1
# Alteração no Fixed Frame: "map" -> "turtlebot1/map"

# Terminal 5: YOLOv8
docker exec -it turtlebot4_simulador bash
#python3 src/yolo.py
``` 