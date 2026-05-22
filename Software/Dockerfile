FROM osrf/ros:humble-desktop

ARG user_id=1000
ARG ros_ws=/home/dockeruser/turtlebot4_ws

ENV DEBIAN_FRONTEND=noninteractive

# Pacotes do sistema
RUN apt-get update && apt-get install -y \
    # Ignition Gazebo Fortress (versão compatível com Humble)
    ignition-fortress \
    # Bridge ROS 2 <-> Ignition
    ros-humble-ros-gz \
    ros-humble-gz-ros2-control \
    # Middleware CycloneDDS (obrigatório)
    ros-humble-rmw-cyclonedds-cpp \
    # TurtleBot4 simulator
    ros-humble-turtlebot4-simulator \
    ros-humble-irobot-create-nodes \
    ros-humble-turtlebot4-navigation \
    ros-humble-turtlebot4-description \
    # Navegação autônoma (Nav2)
    ros-humble-nav2-bringup \
    ros-humble-nav2-msgs \
    # SLAM Toolbox (mapeamento)
    ros-humble-slam-toolbox \
    # Visualização
    ros-humble-rviz2 \
    # Utilitários
    python-is-python3 \
    python3-pip \
    nano \
    less \
    xterm \
    git \
    # Dependências do YOLO (OpenCV, etc)
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# YOLOv8 (Ultralytics): instalado como root antes de trocar de usuário
RUN pip3 install ultralytics "numpy<2"

# Uso de GPU NVIDIA (caso você tenha): Gráficos para Gazebo/RViz e Compute para YOLO
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=all

# Usuário não-root
RUN useradd -m --uid ${user_id} dockeruser
USER dockeruser
WORKDIR /home/dockeruser
ENV HOME=/home/dockeruser
ENV PATH="/home/dockeruser/.local/bin:${PATH}"

# Força saída Python sem buffer
ENV PYTHONUNBUFFERED=1

# Workspace do TurtleBot4
RUN mkdir -p ${ros_ws}/src

# .bashrc
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc \
    && echo "export TURTLEBOT4_MODEL=standard" >> ~/.bashrc \
    && echo "export ROS_DOMAIN_ID=0" >> ~/.bashrc \
    && echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc \
    && echo "export IGN_VERSION=fortress" >> ~/.bashrc \
    && echo "export IGNITION_VERSION=fortress" >> ~/.bashrc

# Entrypoint
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]