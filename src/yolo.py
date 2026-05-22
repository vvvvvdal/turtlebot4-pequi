import cv2
import rclpy
from ultralytics import YOLO
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist

DISTANCIA_MINIMA = 1.5

class Visao_YOLO:
    def __init__(self):
        self.modelo_yolo = YOLO('yolov8n.pt')

    def processar_imagem(self, imagem_cv2):
        # 2. Inferencia da IA do modelo YOLO
        resultados = self.modelo_yolo(imagem_cv2)
        imagem_desenhada = resultados[0].plot()

        pessoa = False
        x_centro = 0
        y_centro = 0

        # 3. Processamento de coordenadas
        for caixa in resultados[0].boxes:
            classe = int(caixa.cls[0].item())

            if classe == 0: # Pessoa (person) tem id de classe 0 
                x_centro = int(caixa.xywh[0][0].item())
                y_centro = int(caixa.xywh[0][1].item())
                pessoa = True
                break

        return pessoa, x_centro, y_centro, imagem_desenhada


class Olho_Do_Robo(Node):
    def __init__(self) -> None:
        super().__init__('Olho_Do_Robo')

        self.bridge = CvBridge()
        self.visao = VisaoYOLO()

        # Ouvinte da camera rgb (visão)
        self.subscription_velocidade = self.create_subscription(
            Image,
            '/turtlebot1/oakd/rgb/preview/image_raw',
            self.ouvinte_callback,
            10)
        self.subscription_velocidade # Previne aviso de variável não utilizada

        # Variaveis de memoria do robo
        self.mapa_profundidade = None
        self.fugindo = False # Memória de estado do robô

        # Ouvinte da camera de profundidade (distancia)
        self.subscription_profundidade = self.create_subscription(
            Image,
            '/turtlebot1/oakd/rgb/preview/depth',
            self.profundidade_callback,
            10)
        self.subscription_profundidade # Previne aviso de variável não utilizada

        # Falante do robo (controle de rodas)
        self.publisher_velocidade = self.create_publisher(Twist, '/turtlebot1/cmd_vel', 10)
        
    def ouvinte_callback(self, img):
        # 1. Traducao da imagem
        imagem_cv2 = self.bridge.imgmsg_to_cv2(img, "bgr8")

        pessoa, x_centro, y_centro, imagem_desenhada = self.visao.processar_imagem(imagem_cv2)

        # 4. Controle de seguranca ao detectar pessoa proxima
        if pessoa and self.mapa_profundidade is not None:
            distancia_atual = self.calcular_distancia(y_centro, x_centro)

            # Trava de segurança: 0.0 geralmente significa erro de leitura do sensor (camera cega)
            if distancia_atual <= 0.0:
                self.get_logger().info("Leitura do sensor falhou (0.0m). Ignorando acao para evitar travamentos.")

            # 1: Robo muito perto da pessoa
            elif distancia_atual <= DISTANCIA_MINIMA: 
                self.get_logger().info(f"[ALERTA] Pessoa muito perto. Distancia de {distancia_atual:.2f}m. Dando re.")
                msg_movimento = Twist()
                msg_movimento.linear.x = -0.3 # Robo anda 0.3m/s para tras
                msg_movimento.angular.z = 0.0
                self.publisher_velocidade.publish(msg_movimento)

                self.fugindo = True # Robo anota na memoria que esta fugindo

            # 2: Robo esta alem da distancia minima
            else: 
                # Se o robo estava fugindo, ele freia e fica parado na distancia segura
                if self.fugindo: 
                    self.get_logger().info(f"Robo esta na distancia segura. Distancia de {distancia_atual:.2f}m.")
                    msg_movimento = Twist()
                    msg_movimento.linear.x = 0.0
                    msg_movimento.angular.z = 0.0
                    self.publisher_velocidade.publish(msg_movimento)

                    self.fugindo = False # Desativa o modo de fuga, liberando o movimento do robo pro Nav2/Teclado

        # 5. Exibicao na Tela
        cv2.imshow("Camera do robo", imagem_desenhada)
        cv2.waitKey(1)
    
    def profundidade_callback(self, img_profundidade):
        # Salva o mapa de distancia na memoria do robo sem alterar os dados puros (passthrough)
        self.mapa_profundidade = self.bridge.imgmsg_to_cv2(img_profundidade, "passthrough")

    def calcular_distancia(self, y: int, x: int) -> float:
        # Extrai o valor do pixel central do elemento. No Gazebo, a camera de profundidade ja manda em metros.
        return float(self.mapa_profundidade[y, x])


def main(args=None):
    rclpy.init(args=args)
    olho_do_robo = Olho_Do_Robo()
    
    try:
        rclpy.spin(olho_do_robo)
    except KeyboardInterrupt:
        pass # Fecha quando aperta CTRL+C no terminal
    finally:
        olho_do_robo.destroy_node()
        cv2.destroyAllWindows()
        rclpy.shutdown()

if __name__ == "__main__":
    main()