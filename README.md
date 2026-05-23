# TurtleBot4: Pequi Mecânico

O objetivo deste projeto foi pegar o TurtleBot4 (base iRobot Create 3) e fazer um upgrade real na arquitetura de software e hardware dele. A ideia foi resolver gargalos de processamento substituindo a placa original e implementar um sistema de navegação autônoma onde o robô não apenas desvia de paredes cegas, mas usa visão computacional (YOLOv8) para identificar objetos e tomar decisões de segurança em tempo real.

---
Documentos no Drive
[![Google Drive](https://img.shields.io/badge/Google%20Drive-Documentos-blue?logo=googledrive&logoColor=white)](https://drive.google.com/drive/folders/12bSoTxOGh3vUiAucfdEUXaNt9Qit2mPP)
---

## Estrutura do Repositório

O repositório está dividido nas três frentes de engenharia do projeto. Cada pasta tem seu próprio README detalhado de execução e montagem:

* **[Software](./Software/)**: Contém a arquitetura ROS 2, configurações do Docker, mapeamento (SLAM), navegação (Nav2) e o script de visão (YOLOv8).
* **[Estrutural](./Estrutural/)**: Contém as modelagens 3D, projetos do suporte customizado e parâmetros de impressão para o upgrade físico do robô.
* **[Hardware](./Hardware/)**: Documentação de Hardware, Engenharia e Integração de Sistemas.Contém o projeto da PCB, esquemáticos, lista de componentes e detalhes de montagem do circuito de controle.

---

## Visão Geral: Software

A simulação e o controle rodam em um ambiente Docker isolado, com suporte a aceleração por GPU NVIDIA.

**Principais implementações:**
* Mapeamento do ambiente usando LiDAR (SLAM).
* Criação de Costmaps globais e locais (Nav2) para rotas seguras.
* Processamento de imagem rodando em paralelo com YOLOv8n para detecção de pessoas.
* Controle de prioridade de movimento: integração do `twist_mux` para garantir que o comando de segurança (ré) do YOLO sobressaia sobre o Nav2 em risco de colisão.

![Visão geral do sistema com Gazebo, RViz e Visão YOLOv8](Software/imgs/gazebo-rviz2-yolov8.png)

Instruções completas de instalação, comandos do Gazebo e explicação dos terminais estão no **[Guia de Software](./Software/README.md)**.

---

## Visão Geral: Estrutural

Para o robô aguentar rodar a visão computacional e o Nav2 sem engasgar, trocamos a Raspberry Pi 4 de fábrica por uma NVIDIA Jetson Orin Nano. Isso exigiu um reprojeto da plataforma superior.

**Principais implementações:**
* Suporte customizado modelado para a furação 12x12 da base Create 3.
* Espaço para o módulo XL4016 para regulação de tensão.
* Fixação feita com insertos roscados de latão a quente e parafusos M2.5.
* Peças projetadas para impressão 3D em ABS (resistência mecânica e térmica).

<img width="800" src="https://github.com/user-attachments/assets/0864b150-c884-4562-87a3-d0839fac3c56" alt="Renderização CAD do novo suporte com Jetson e XL4016">

Os arquivos CAD (.STEP, .SLDPRT) e o detalhamento da montagem estão no **[Guia Estrutural](./Estrutural/README.md)**.

---

## Visão Geral: Hardware

A eletrônica de expansão do robô foi centralizada em uma Shield/HAT customizada (100 mm × 79 mm), projetada para acoplamento direto via *stacking headers* sobre os 40 pinos da NVIDIA Jetson Orin Nano. A arquitetura elimina microcontroladores secundários no MVP para mitigar latências de barramento.

**Principais implementações:**
* **Gerenciamento de Potência Unificado:** Alimentação total do sistema a partir da bateria nativa de 14.4V da base Create 3, utilizando um regulador chaveado Buck XL4016 externo para a linha de +5V periférica e um robusto banco capacitivo Low-ESR para proteção contra quedas de tensão (*voltage sags*).
* **Telemetria Absoluta de Bateria:** Monitoramento de tensão em tempo real por meio de um divisor resistivo acoplado ao conversor analógico-digital **ADS1115 (16-bits I2C)**, fornecendo cálculo preciso de SoC% e prevenção de desligamentos críticos (<11.5V).
* **Controle de Acesso e Autenticação:** Integração de um módulo RFID **MFRC522 operando via barramento SPI síncrono**, atuando como validação biométrica de operadores autorizados em ambiente fabril.
* **Monitoramento Ambiental Ativo:** Sensoriamento de fumaça e gases inflamáveis com o **MQ-2**, utilizando condicionamento de sinal analógico via ADC e digital conectado diretamente à GPIO da Jetson com tratamento de interrupção por hardware.

O esquemático elétrico completo, lista de materiais (BOM), mapa de Netlist e orientações de soldagem estão no **[Guia de Hardware](./Hardware/README.md)**.

---

## Como rodar

Clone o repositório na sua máquina:

```bash
git clone [https://github.com/vvvvvdal/turtlebot4-pequi.git](https://github.com/vvvvvdal/turtlebot4-pequi.git)
cd turtlebot4-pequi
