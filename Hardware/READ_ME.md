# 🐢 Pequi Mecânico: TurtleBot 4 MVP Shield
**Documentação de Hardware, Engenharia e Integração de Sistemas**

![Version](https://img.shields.io/badge/Versão-MVP_v1.0-blue.svg)
![Status](https://img.shields.io/badge/Status-Design_Validado-success.svg)
![Plataforma](https://img.shields.io/badge/SBC-NVIDIA_Jetson_Orin_Nano-76B900.svg)
![ROS](https://img.shields.io/badge/ROS_2-Humble_Hawksbill-22314E.svg)
![EDA](https://img.shields.io/badge/EDA-EasyEDA_Pro-orange.svg)

---

## 📑 Índice de Conteúdos
1. [Introdução e Filosofia de Arquitetura](#1-introdução-e-filosofia-de-arquitetura)
2. [Especificações Computacionais (Jetson Orin Nano)](#2-especificações-computacionais-jetson-orin-nano)
3. [Restrições Mecânicas, Térmicas e Validação 3D](#3-restrições-mecânicas-térmicas-e-validação-3d)
4. [Infraestrutura de Potência (Power Tree)](#4-infraestrutura-de-potência-power-tree)
5. [Condicionamento de Sinais e Barramentos](#5-condicionamento-de-sinais-e-barramentos)
6. [Memória de Cálculo de Engenharia](#6-memória-de-cálculo-de-engenharia)
7. [Estratégias de Blindagem e EMI](#7-estratégias-de-blindagem-e-emi)
8. [Mapeamento Físico e Netlist Completo](#8-mapeamento-físico-e-netlist-completo)
9. [Bill of Materials (BOM)](#9-bill-of-materials-bom)
10. [Integração de Software: ROS 2 e Docker](#10-integração-de-software-ros-2-e-docker)
11. [Roteiro de Expansão (Fase 2)](#11-roteiro-de-expansão-fase-2)
12. [Guia de Troubleshooting e Manutenção](#12-guia-de-troubleshooting-e-manutenção)
13. [Referências Técnicas](#13-referências-técnicas)
14. [Imagens e Anexos](#14-imagens-e-anexos)

---

## 1. Introdução e Filosofia de Arquitetura

O **TurtleBot 4 MVP Shield** é uma placa de expansão customizada (HAT/Shield) concebida para atuar como a espinha dorsal elétrica e de aquisição de dados do robô móvel autónomo (AMR) desenvolvido pela equipa Pequi Mecânico. O projeto visa a atualização massiva da capacidade computacional da plataforma base (iRobot Create 3), migrando do tradicional Raspberry Pi 4 para a **NVIDIA Jetson Orin Nano Developer Kit (8GB)**.

### 1.1 A Eliminação de Co-processadores (Mitigação de Latência)
A arquitetura eletrónica foi desenhada com uma forte filosofia **Edge Computing**. Eliminou-se intencionalmente a presença de microcontroladores secundários (como STM32, Arduino ou ESP32) como intermediários lógicos nesta primeira fase (MVP). Em sistemas robóticos convencionais, a divisão de tarefas gera latência estocástica de barramentos seriais (UART/CAN). Ao injetar os sinais físicos diretamente nos pinos nativos (GPIO, SPI, I2C) do SoC Ampere/ARM da NVIDIA, a latência de comunicação é virtualmente reduzida a zero, permitindo que a *stack* de navegação autónoma reaja a eventos críticos (como a deteção de fumo) em tempo real absoluto.

### 1.2 Filosofia COTS (Commercial Off-The-Shelf)
Para garantir velocidade de iteração (Time-to-Market) sem sacrificar a robustez industrial, o projeto adotou componentes COTS. A PCB customizada atua como uma **Placa Base de Interconexão Modular**, unindo módulos validados no mercado global de semicondutores:
* **MFRC522:** Segurança e autenticação criptográfica RFID em 13.56 MHz.
* **MQ-2:** Segurança ambiental contra gases combustíveis e fumo (SnO2).
* **ADS1115:** Telemetria analógica de ultra-alta precisão (16 bits) para digitalização da bateria.
* **XL4016:** Regulação de potência bruta industrial (Buck Converter) lidando com correntes de até 8A.

---

## 2. Especificações Computacionais (Jetson Orin Nano)

A transição para a Jetson Orin Nano de 8GB dita as regras do design de hardware. O SoC (System-on-Chip) exige uma refrigeração rigorosa e possui tolerâncias elétricas estritas que não podem ser violadas sob pena de destruição permanente do silício.

### 2.1 Limites Lógicos de 3.3V
A característica mais crítica da Jetson Orin Nano é o seu domínio de tensão de entrada/saída (I/O). Diferente de arquiteturas legadas e microcontroladores baseados em 5V (como o Arduino Uno), todos os pinos de dados da NVIDIA operam estritamente a **3.3V lógicos**. Injetar 5V numa porta GPIO provoca a quebra dielétrica instantânea dos transístores MOSFET internos. Esta restrição de semicondutor obrigou o desenvolvimento de circuitos atenuadores passivos na Shield para casar as impedâncias e tensões.

### 2.2 Capacidade de Processamento e GPU
Com 40 TOPS de desempenho, GPU de arquitetura Ampere com 1024 núcleos CUDA (além de 32 Tensor Cores) e CPU ARM Cortex-A78AE de 6 núcleos, a Jetson gere localmente e em tempo real a inferência de redes neuronais (como o YOLOv8) e os complexos algoritmos de SLAM (Simultaneous Localization and Mapping) do ecossistema ROS 2. O hardware da Shield atua apenas como condutor sensorial limpo para alimentar este cérebro.

---

## 3. Restrições Mecânicas, Térmicas e Validação 3D

O desenvolvimento em torno da Jetson Orin Nano introduz um desafio crítico de engenharia térmica e mecânica. O módulo dissipador de alumínio extrudido e o cooler ativo PWM são incrivelmente volumosos. Colocar uma Shield standard no topo bloquearia a admissão radial de ar, induzindo *thermal throttling* (estrangulamento térmico) em poucos minutos sob carga computacional pesada.

### 3.1 Estratégia de Elevação e Stacking
Para garantir o fluxo de ar contínuo, a PCB (dimensionada rigorosamente em **100 mm × 79 mm** no ambiente CAD do EasyEDA Pro) foi projetada utilizando três pilares de fixação espacial:

1. **Stacking Header Extra Tall (11-15mm):** O conector fêmea de 40 pinos (HDR1) possui isolamento plástico estendido, elevando a linha de base da placa para longe do metal do dissipador.
2. **Montagem Bottom Layer (Espelhada):** O conector HDR1 é soldado na face inferior da placa (*Bottom Layer*), utilizando o próprio corpo plástico do conector como um espaçador mecânico natural. Os componentes periféricos (bornes, módulos, capacitores) residem estritamente no *Top Layer*.
3. **Standoffs Estruturais (M2.5):** A PCB possui quatro furos de montagem nos cantos. Eles são fixados ao suporte principal (impresso em ABS de alta densidade) através de espaçadores roscados (standoffs) M2.5 de Nylon ou Latão. Isto impede a fadiga mecânica, a flexão da placa e o consequente choque contra o cooler durante a trepidação do robô no chão de fábrica.

---

## 4. Infraestrutura de Potência (Power Tree)

A base motriz iRobot Create 3 é alimentada por uma bateria interna inteligente de iões de lítio. Esta bateria fornece uma tensão que varia dinamicamente entre **11.5V (descarga profunda crítica)** e **16.8V (carga máxima em doca)**, com um valor nominal de 14.4V. A Shield não utiliza baterias externas ou powerbanks secundários, unificando a extração de energia a partir desta única bateria central.

### 4.1 Alimentação Principal e Filtragem (Rede `V_BAT`)
A energia é admitida na Shield através de bornes de parafuso industriais do tipo **KF301 (Passo 5.08mm)** (designadores U1, U2, U3). O aperto mecânico previne desconexões por vibração que os jumpers comuns sofreriam.
A proteção primária da Jetson e do sistema é efetuada por um **fusível de vidro cilíndrico de ação rápida (Fast-Blow) de 5A** (F1), que atua de forma sacrificial rompendo em milissegundos num evento de curto-circuito, blindando o hardware da NVIDIA.

Os motores de corrente contínua da base geram picos de tensão reversa (*Back-EMF*) e ruído de comutação de escovas. Para proteger o microprocessador, a rede `V_BAT` atravessa um banco de filtragem massivo e desacoplado na Shield:
* **Capacitor Eletrolítico C1 (470µF / 25V / Low-ESR):** Atua como um reservatório de inércia de baixa frequência para compensar afundamentos momentâneos de corrente (*voltage sags*) durante arranques bruscos de locomoção. A margem de isolamento de 25V garante segurança operacional absoluta.
* **Capacitor Cerâmico C2 (100nF):** Desacopla ruídos eletromagnéticos e harmónicos de altíssima frequência (EMI) introduzidos pelo chaveamento PWM dos inversores de ponte H da base motriz.

### 4.2 O Isolamento Térmico e Lógico do Regulador XL4016 (Rede `+5V_EXT`)
O sensor de deteção ambiental MQ-2 possui um elemento resistivo de aquecimento interno fabricado em Dióxido de Estanho ($SnO_2$) que drena constantemente cerca de 200mA a rigorosos 5.0V. Extrair esta carga pesada e térmica através do *Power Management IC* (PMIC) interno da Jetson (pelos pinos de 5V do header) induziria stress térmico massivo na placa-mãe, arriscando *brownouts* e travamentos do sistema operativo Ubuntu.

A solução de engenharia adotada foi delegar esta regulação de alta corrente para um **Conversor DC-DC Buck Step-Down XL4016** montado externamente ao chassi da Shield. O XL4016 aceita os 14.4V brutos e, operando a 180kHz com eficiência chaveada de até 93%, providencia **5.0V estabilizados a até 8A**. Esta linha limpa regressa à Shield pelo borne U5 (`+5V_EXT`), alimentando o MQ-2 de forma totalmente isolada, não gerando aquecimento por Efeito Joule nas trilhas delicadas da PCB e reservando amperagem massiva para os futuros ecrãs LCD com retroiluminação.

---

## 5. Condicionamento de Sinais e Barramentos

Garantir que os sensores analógicos e digitais funcionem em harmonia com o limite destrutivo de 3.3V da Jetson exigiu topologias de divisão resistiva rigorosas e a introdução de digitalizadores I2C de precisão.

### 5.1 Barramento SPI de Alta Velocidade (Módulo MFRC522)
Para a autenticação de segurança dos operadores fabris, integrou-se um leitor RFID MIFARE de 13.56 MHz (MFRC522). Este chip da NXP Semiconductors opera nativamente no domínio de 3.3V, permitindo o acoplamento direto sobre o barramento SPI0 nativo da Jetson Orin Nano sem transdutores lógicos (*logic level shifters*).
As linhas de dados (MISO, MOSI, SCK, CS) garantem taxas de transferência determinísticas para validação criptográfica em tempo real, e o pino GPIO 22 foi alocado como *Hardware Reset* (RST) para reiniciar e restabelecer o módulo em caso de falha no barramento ou interferência estática (*timeout*).

### 5.2 Divisor Lógico de Tensão do Sensor MQ-2
Alimentado a 5.0V pela rede `+5V_EXT`, a saída digital (DO) controlada pelo comparador LM393 do módulo MQ-2 emite um impulso retangular de 5.0V exatos quando deteta concentrações perigosas de gás ou fumo. Para impedir a morte do processador da Jetson, implementou-se um atenuador passivo a nível de hardware na PCB:
* Um resistor de **1 kΩ (R3)** em série com a linha.
* Um resistor de **2 kΩ (R4)** em paralelo referenciado ao Ground comum (GND).
Este nó matemático atesta uma saída constante, rebaixada e segura que é encaminhada ao Pino 15 da Jetson. No nó de software (ROS 2), este pino está configurado como uma *Hardware Interrupt* de borda de subida (*Rising Edge*) que injeta um comando prioritário de paragem de emergência (*Emergency Stop / E-Stop*) na árvore cinemática do Nav2 Stack.

### 5.3 O Digitalizador Analógico-Digital I2C (ADS1115)
Como a Jetson Orin Nano carece totalmente de conversores A/D integrados no seu *pinout*, adicionou-se o módulo externo **ADS1115 (Conversor ADC Delta-Sigma de 16 bits)**. O barramento I2C1 (Pinos 3 e 4) da Jetson possui resistores pull-up internos nativos de 3.3V, simplificando radicalmente a cablagem e roteamento da placa.
* **Canal A1:** Diretamente ligado à saída analógica (AO) linear do MQ-2 para mapear espacialmente a variação contínua de concentração gasosa em PPM (Partes Por Milhão).
* **Canal A0 (Telemetria de Bateria):** Acoplado a um divisor de tensão de ultraprecisão (usando resistores de película metálica rigorosa com 1% de tolerância), composto por **R1 (100 kΩ)** e **R2 (10 kΩ)**, atenuando a perigosa e flutuante tensão da bateria numa taxa segura de atenuação de 11:1.

---

## 6. Memória de Cálculo de Engenharia

Esta secção prova matematicamente a robustez absoluta das escolhas de design e do balanceamento resistivo realizados na Shield.

### 6.1 Condicionamento Lógico do Alarme MQ-2 (5V para ~3.33V)
A tensão proveniente do pino DO do MQ-2 ($V_{in}$) é de 5.0V em caso de alarme máximo. Pela fórmula da lei de Kirchhoff para o divisor resistivo com R3 ($1 k\Omega$) e R4 ($2 k\Omega$):

$$V_{out} = V_{in} \times \left( \frac{R_4}{R_3 + R_4} \right) = 5.0\text{V} \times \left( \frac{2000}{1000 + 2000} \right)$$
$$V_{out} = 5.0\text{V} \times \left( \frac{2}{3} \right) = 3.333\text{V}$$

**Veredicto de Engenharia:** A amplitude analítica de 3.33V é lida perfeitamente como nível lógico ALTO (HIGH) pela porta CMOS da Jetson, operando no limiar seguro exato e impedindo a quebra do dielétrico semicondutor.

### 6.2 Divisor de Telemetria de Bateria (Atenuação 11:1)
No pico extremo de carga elétrica, a bateria entrega $V_{max} = 16.8\text{V}$. A entrada analógica A0 do ADS1115 jamais pode exceder o seu referencial VCC (3.3V). Utilizando a impedância formidável de R1 ($100 k\Omega$) e R2 ($10 k\Omega$):

$$V_{ADC\_MAX} = 16.8\text{V} \times \left( \frac{10.000}{100.000 + 10.000} \right) = 16.8\text{V} \times \left( \frac{1}{11} \right) = 1.527\text{V}$$

**Veredicto de Engenharia:** Mesmo no pico destrutivo de carga total da iRobot Create 3, a tensão máxima injetada no conversor será de apenas **1.527V**, garantindo uma margem massiva de segurança de quase 50% abaixo do limite limite físico de 3.3V. No limite inferior crónico de descarga da bateria (11.5V), a leitura medida será de confortáveis **1.045V**.

### 6.3 Resolução Analítica do Conversor (LSB e FSR)
O ADS1115 fornece 15 bits efetivos de quantização operando em modo *Single-Ended* com GND ($2^{15} = 32.768$ degraus discretos). Configurou-se o Amplificador de Ganho Programável (PGA) no software Python para um *Full Scale Range* (FSR) de $\pm 2.048\text{V}$, otimizando a leitura:

$$LSB = \frac{2.048\text{V}}{32768} = 0.0000625\text{ V} = 62.5 \mu\text{V}$$

Multiplicando este limite atómico de perceção pelo fator do divisor de tensão da bateria (11x), encontramos o valor real que o robô distingue na bateria:

$$\text{Sensibilidade} = 62.5 \mu\text{V} \times 11 = 687.5 \mu\text{V} \approx 0.68 \text{ mV}$$

**Veredicto de Engenharia:** O sistema consegue distinguir variações micro-elétricas na tensão da bateria em degraus ínfimos de **0.68 milivolts**. Esta granularidade extrema permite que as redes neuronais ou os nós do ROS 2 gerem curvas estocásticas de *State of Charge* (SoC%) de altíssima fidelidade.

### 6.4 Corrente de Fuga Parasita e Dissipação Térmica
A carga da bateria é drenada de forma parasita continuamente (mesmo em Standby) pelo divisor resistivo através da malha R1+R2 ($110 k\Omega$):

$$I_{fuga} = \frac{16.8\text{V}}{110.000 \Omega} = 0.000152\text{ A} = 0.152\text{ mA}$$

A potência térmica real dissipada por Efeito Joule pelo resistor de queda principal R1 (100k):

$$P_{dissipada} = I_{fuga}^2 \times R_1 = (0.000152\text{A})^2 \times 100.000 \Omega = 0.0023\text{ W} = 2.3\text{ mW}$$

**Veredicto de Engenharia:** Uma drenagem de 0.15mA é insignificante para a capacidade de milhares de miliamperes-hora da base Create 3. A potência irrisória de 2.3mW está severamente abaixo dos 250mW máximos suportados pelo resistor axial, assegurando que o componente opera totalmente frio. Um resistor frio impede desvios nas leituras provocados pelo seu Coeficiente de Temperatura (ppm/°C), preservando a matemática exata durante anos de serviço contínuo.

---

## 7. Estratégias de Blindagem e EMI (Compatibilidade Eletromagnética)

Pavilhões industriais e células de manufatura geram ruídos eletromagnéticos agressivos e radiações parasitas (EMI). O projeto adotou regras rigorosas de *layout* de PCB para garantir estabilidade:
1. **Dimensionamento Massivo de Trilhas:** As malhas de potência `V_BAT` e `+5V_EXT` foram roteadas muito espessas (até 2.0mm / 80 mils) para suportar altas correntes sem estrangulamento indutivo, enquanto sinais digitais rápidos (SPI/I2C) utilizaram trilhas finas (0.25mm) para mitigar capacitâncias parasitas que deformariam as ondas quadradas de clock.
2. **Plano de Terra Sólido e Unificado (Copper Pour):** Todo o *Bottom Layer* foi preenchido com malha de GND contínua. Este escudo térmico e eletromagnético minimiza radicalmente as áreas dos *loops* de corrente e protege as linhas I2C e SPI contra a irradiação indutiva provocada pelos motores elétricos do robô.
3. **Clearance Analógico (Mitigação de Diafonia):** As pistas sensíveis analógicas de leitura de gás e bateria foram roteadas propositadamente longe dos *clocks* do barramento SPI (que oscilam em megahertz) para evitar indução capacitiva cruzada e acoplamento mútuo (*Crosstalk*).

---

## 8. Mapeamento Físico e Netlist Completo

A integridade do *Hardware Layer* é demonstrada no Netlist final validado exportado do PADS/EasyEDA Pro.

| Nome da Net (Rede) | Componentes e Pinos Atribuídos | Descrição da Função de Engenharia Elétrica |
| :--- | :--- | :--- |
| **`V_BAT`** | U1.1, U2.1, U3.1, F1.2, C1.1, C2.2, R1.1 | Barramento primário da bateria (11.5V a 16.8V). Rota de alta potência, atravessada fisicamente pelo fusível F1 e pelo banco capacitivo estabilizador C1/C2. |
| **`+5V_EXT`** | U5.1, MQ2.1, U_LCD.1 | Alimentação estável de alta corrente gerada pelo módulo XL4016 externo para abastecer o aquecedor do MQ-2 e o backpanel do LCD, protegendo a Jetson. |
| **`+3V3`** | HDR1.1, RFID.1, U4.8 | Referência de tensão lógica hiperestável gerada pelo PMIC da Jetson. Alimenta a lógica digital do RFID MFRC e o VCC base do ADC. |
| **`GND`** | HDR1.6, C1.2, C2.1, U3.2, MQ2.2, R2.2, RFID.2, U4.1, U5.2 | Plano de terra referencial equipotencial massivo e contínuo da Shield. |
| **`BATERIA_SINAL`**| R1.2, R2.1, U4.4 (Canal A0) | Tensão analógica 11 vezes rebaixada e segura da bateria para telemetria. Max 1.52V. |
| **`MQ2_SINAL_3V3`**| R3.2, R4.1, HDR1.15 | Impulso atenuado lógico de deteção de fumo (3.33V) disparando *Hardware Interrupt* na GPIO 15. |
| **`MQ2_SINAL_A0`** | MQ2.4, U4.5 (Canal A1) | Leitura analógica linear bruta da curva de concentração gasosa (AO) do sensor MQ-2. |
| **`I2C_SDA`** | HDR1.3, U4.9, U_LCD.2 | Dados seriais bidirecionais (*Serial Data*) do Barramento I2C1 nativo. Compartilhado de forma daisy-chain entre ADS1115 e PCF8574. |
| **`I2C_SCL`** | HDR1.4, U4.10, U_LCD.3 | Clock serial (*Serial Clock*) sincronizador gerado pelo mestre I2C1 (Jetson) operando a 100kHz/400kHz. |
| **`SPI_MOSI`** | HDR1.19, RFID.5 | *Master Out Slave In* - Comandos enviados da arquitetura mestre (Jetson) para o leitor MFRC522. |
| **`SPI_MISO`** | HDR1.21, RFID.4 | *Master In Slave Out* - Retorno dos IDs criptográficos validados do cartão RFID para a Jetson. |
| **`SPI_SCK`** | HDR1.23, RFID.6 | Clock Serial gerado pela Jetson ditando a temporização restrita do barramento SPI0. |
| **`SPI_CS`** | HDR1.24, RFID.7 | *Chip Select* (Active Low) manipulado pelo kernel Linux para acordar o leitor MFRC522 do Standby. |
| **`RFID_RST`** | HDR1.22, RFID.3 | Pino de *Hardware Reset* manipulável ativamente pelo ROS 2 para recuperar travamentos espúrios do módulo. |

---

## 9. Bill of Materials (BOM)

Tabela unificada com o detalhamento completo dos componentes COTS, passivos e conexões mecânicas homologadas para a produção da Shield industrial:

| Referência | Qtd | Especificação Técnica e Descrição do Componente | Encapsulamento / Package | Tipo de Montagem (Assembly) | Função Arquitetural na Placa |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **SBC** | 1 | NVIDIA Jetson Orin Nano Developer Kit (8GB RAM, CPU ARM 6-Cores, GPU Ampere de 40 TOPS) | DevKit Pro Module | Fixação por Standoffs (M2.5) | Cérebro computacional central, executa ROS 2 Humble em Docker, pacotes SLAM e IA (YOLOv8). |
| **REG** | 1 | Módulo Buck Step-Down baseado no robusto CI XL4016 (Ajustado p/ 5.0V / 8A) | Módulo Externo Volumoso | Fixação no Chassi Metálico | Rebaixa a bateria instável para 5V hiper-estáveis e isola o ruído/térmica longe da Jetson. |
| **U4** | 1 | Módulo ADC 16-bits I2C Texas Instruments ADS1115 (Com PGA Integrado) | Módulo Vertical COTS | Soldadura THT (Furo Passante) | Digitaliza sinais analógicos precisos da bateria e dos gases. |
| **RFID** | 1 | Módulo Leitor RFID/NFC MFRC522 (Frequência 13.56MHz) c/ suporte MIFARE ISO/IEC 14443 A | Módulo Vertical COTS | Soldadura THT (Furo Passante) | Barreira restritiva de segurança fabril e autenticação obrigatória do operador. |
| **MQ2** | 1 | Módulo Sensor Gás Combustível e Fumo MQ-2 (Aquecedor microfabricado SnO2 e comparador LM393) | Módulo Vertical COTS | Soldadura THT (Furo Passante) | Sensoriamento ambiental precoce e ativação do E-Stop cinemático contra princípios de incêndio. |
| **U(1-5)**| 4 | Borne de Parafuso robusto KRE KF301-5.0-2P (Passo 5.08mm) em termoplástico industrial | KF301 2-Pinos | Soldadura THT (Furo Passante) | Conexão imune a vibrações severas para barramentos de potência em cabos 18 AWG. |
| **F1** | 1 | Fusível de Vidro cilíndrico de Ação Rápida (Fast-Blow) 5A (Tensão de isolamento de 250V) | Cilíndrico 5x20 mm | Clipes Metálicos (Porta-Fusíveis) | Elemento sacrificial para isolamento térmico e elétrico da Jetson contra curto-circuitos. |
| **C1** | 1 | Capacitor Eletrolítico Alumínio 470µF / 25V (Especificação especial de baixo ESR) | Radial Can 8mm | Soldadura THT (Furo Passante) | Amortecimento inercial de transientes, quedas de baixa frequência e compensação motriz. |
| **C2** | 1 | Capacitor Cerâmico Multicamadas (MLCC) 100nF / 50V de alto dielétrico | Axial/Radial THT | Soldadura THT (Furo Passante) | Desacoplamento rápido de alta frequência indutiva (PWM) dos inversores da base Create 3. |
| **R1** | 1 | Resistor de Película Metálica 100 kΩ (Tolerância laboratorial de 1%, 1/4W) | Axial DO-35 | Soldadura THT (Furo Passante) | Braço resistivo em série de alta precisão do divisor de tensão da telemetria (Canal A0). |
| **R2** | 1 | Resistor de Película Metálica 10 kΩ (Tolerância laboratorial de 1%, 1/4W) | Axial DO-35 | Soldadura THT (Furo Passante) | Braço resistivo em paralelo aterrado (GND) do divisor de telemetria da bateria. |
| **R3** | 1 | Resistor Filme de Carbono/Metal 1 kΩ (Tolerância padronizada de 5%, 1/4W) | Axial DO-35 | Soldadura THT (Furo Passante) | Braço resistivo em série limitador lógico do alarme digital DO (5V) proveniente do sensor MQ-2. |
| **R4** | 1 | Resistor Filme de Carbono/Metal 2 kΩ (Tolerância padronizada de 5%, 1/4W) | Axial DO-35 | Soldadura THT (Furo Passante) | Braço resistivo paralelo aterrado rebaixando o alarme fatal de 5V para exatos 3.33V seguros para a NVIDIA. |
| **HDR1** | 1 | Conector Fêmea Extra Alto (*Stacking Header / Extra Tall*) - Isolamento estendido de 11mm a 15mm | Receptáculo 2x20 (40P) | Soldadura THT no Bottom Layer (Espelhado) | Cria distanciamento aerodinâmico vital (Gap de ar) entre a PCB da Shield e as aletas do dissipador térmico da Jetson. |
| **ESP** | 4 | Espaçador cilíndrico sextavado roscado M2.5 (Standoff) fabricado em Nylon isolante ou Latão niquelado | Standoff M2.5 | Travamento por Parafuso Mecânico | Ancoragem rígida que liga as placas e previne fraturas por fadiga ou flexão da PCB sob stress mecatrónico. |

---

## 10. Integração de Software: ROS 2 e Docker

A decisão de arquitetura por isolar os processos num *runtime* de contêineres Docker impõe desafios formidáveis de passagem de hardware (*Hardware Passthrough*). O kernel *host* da Jetson precisa ser modificado a nível de *boot* e os descritores de dispositivos expostos com exatidão no ficheiro Compose do ROS 2.

### 10.1 Preparação Específica do Host (Modificação Jetson-IO)
Os barramentos SPI e I2C nativos não vêm ativos de fábrica na imagem do JetPack Ubuntu. O desenvolvedor deve invocar a ferramenta proprietária da NVIDIA para reconfigurar e recompilar a árvore de dispositivos (*Device Tree Overlay*):
```bash
sudo /opt/nvidia/jetson-io/jetson-io.py
# 1. No menu interativo, navegue por "Configure Jetson 40pin Header".
# 2. Habilite explicitamente os periféricos "spidev" (SPI) e "i2c1" (I2C).
# 3. Guarde as alterações, aplique ao bootloader e reinicie o sistema físico host.
# 🐢 Pequi Mecânico: TurtleBot 4 MVP Shield
**Documentação de Hardware, Engenharia e Integração de Sistemas**

![Version](https://img.shields.io/badge/Versão-MVP_v1.0-blue.svg)
![Status](https://img.shields.io/badge/Status-Design_Validado-success.svg)
![Plataforma](https://img.shields.io/badge/SBC-NVIDIA_Jetson_Orin_Nano-76B900.svg)
![ROS](https://img.shields.io/badge/ROS_2-Humble_Hawksbill-22314E.svg)
![EDA](https://img.shields.io/badge/EDA-EasyEDA_Pro-orange.svg)

---

## 📑 Índice de Conteúdos
1. [Introdução e Filosofia de Arquitetura](#1-introdução-e-filosofia-de-arquitetura)
2. [Especificações Computacionais (Jetson Orin Nano)](#2-especificações-computacionais-jetson-orin-nano)
3. [Restrições Mecânicas, Térmicas e Validação 3D](#3-restrições-mecânicas-térmicas-e-validação-3d)
4. [Infraestrutura de Potência (Power Tree)](#4-infraestrutura-de-potência-power-tree)
5. [Condicionamento de Sinais e Barramentos](#5-condicionamento-de-sinais-e-barramentos)
6. [Memória de Cálculo de Engenharia](#6-memória-de-cálculo-de-engenharia)
7. [Estratégias de Blindagem e EMI](#7-estratégias-de-blindagem-e-emi)
8. [Mapeamento Físico e Netlist Completo](#8-mapeamento-físico-e-netlist-completo)
9. [Bill of Materials (BOM)](#9-bill-of-materials-bom)
10. [Integração de Software: ROS 2 e Docker](#10-integração-de-software-ros-2-e-docker)
11. [Roteiro de Expansão (Fase 2)](#11-roteiro-de-expansão-fase-2)
12. [Guia de Troubleshooting e Manutenção](#12-guia-de-troubleshooting-e-manutenção)
13. [Referências Técnicas](#13-referências-técnicas)
14. [Imagens e Anexos](#14-imagens-e-anexos)

---

## 1. Introdução e Filosofia de Arquitetura

O **TurtleBot 4 MVP Shield** é uma placa de expansão customizada (HAT/Shield) concebida para atuar como a espinha dorsal elétrica e de aquisição de dados do robô móvel autónomo (AMR) desenvolvido pela equipa Pequi Mecânico. O projeto visa a atualização massiva da capacidade computacional da plataforma base (iRobot Create 3), migrando do tradicional Raspberry Pi 4 para a **NVIDIA Jetson Orin Nano Developer Kit (8GB)**.

### 1.1 A Eliminação de Co-processadores (Mitigação de Latência)
A arquitetura eletrónica foi desenhada com uma forte filosofia **Edge Computing**. Eliminou-se intencionalmente a presença de microcontroladores secundários (como STM32, Arduino ou ESP32) como intermediários lógicos nesta primeira fase (MVP). Em sistemas robóticos convencionais, a divisão de tarefas gera latência estocástica de barramentos seriais (UART/CAN). Ao injetar os sinais físicos diretamente nos pinos nativos (GPIO, SPI, I2C) do SoC Ampere/ARM da NVIDIA, a latência de comunicação é virtualmente reduzida a zero, permitindo que a *stack* de navegação autónoma reaja a eventos críticos (como a deteção de fumo) em tempo real absoluto.

### 1.2 Filosofia COTS (Commercial Off-The-Shelf)
Para garantir velocidade de iteração (Time-to-Market) sem sacrificar a robustez industrial, o projeto adotou componentes COTS. A PCB customizada atua como uma **Placa Base de Interconexão Modular**, unindo módulos validados no mercado global de semicondutores:
* **MFRC522:** Segurança e autenticação criptográfica RFID em 13.56 MHz.
* **MQ-2:** Segurança ambiental contra gases combustíveis e fumo ($SnO_2$).
* **ADS1115:** Telemetria analógica de ultra-alta precisão (16 bits) para digitalização da bateria.
* **XL4016:** Regulação de potência bruta industrial (Buck Converter) lidando com correntes de até 8A de forma externa.

---

## 2. Especificações Computacionais (Jetson Orin Nano)

A transição para a Jetson Orin Nano de 8GB dita as regras do design de hardware. O SoC (System-on-Chip) exige uma refrigeração rigorosa e possui tolerâncias elétricas estritas que não podem ser violadas sob pena de destruição permanente do silício.

### 2.1 Limites Lógicos de 3.3V
A característica mais crítica da Jetson Orin Nano é o seu domínio de tensão de entrada/saída (I/O). Diferente de arquiteturas legadas e microcontroladores baseados em 5V (como o Arduino Uno), todos os pinos de dados da NVIDIA operam estritamente a **3.3V lógicos**. Injetar 5V numa porta GPIO provoca a quebra dielétrica instantânea dos transístores MOSFET internos. Esta restrição de semicondutor obrigou o desenvolvimento de circuitos atenuadores baseados em divisores resistivos na Shield para casar as tensões de módulos de 5V.

### 2.2 Capacidade de Processamento e GPU
Com 40 TOPS de desempenho, GPU de arquitetura Ampere com 1024 núcleos CUDA (além de 32 Tensor Cores) e CPU ARM Cortex-A78AE de 6 núcleos, a Jetson gere localmente e em tempo real a inferência de redes neuronais (como o YOLOv8) e os complexos algoritmos de SLAM (Simultaneous Localization and Mapping) do ecossistema ROS 2. O hardware da Shield atua apenas como condutor sensorial limpo para alimentar este cérebro.

---

## 3. Restrições Mecânicas, Térmicas e Validação 3D

O desenvolvimento em torno da Jetson Orin Nano introduz um desafio crítico de engenharia térmica e mecânica. O módulo dissipador de alumínio extrudido e o cooler ativo PWM são incrivelmente volumosos. Colocar uma Shield standard diretamente acoplada bloquearia a admissão radial de ar, induzindo *thermal throttling* (estrangulamento térmico) em poucos minutos sob carga computacional pesada.

### 3.1 Estratégia de Elevação e Stacking
Para garantir o fluxo de ar contínuo, a PCB (dimensionada rigorosamente em **100 mm × 79 mm** no ambiente CAD do EasyEDA Pro) foi projetada utilizando três pilares de fixação espacial:

1. **Stacking Header Extra Tall (11-15mm):** O conector fêmea de 40 pinos (HDR1) possui isolamento plástico estendido, elevando a linha de base da placa para longe do metal do dissipador.
2. **Montagem Bottom Layer (Espelhada):** O conector HDR1 é soldado na face inferior da placa (*Bottom Layer*), utilizando o próprio corpo plástico do conector como um espaçador mecânico natural. Os componentes periféricos (bornes, módulos, capacitores, resistores) residem no *Top Layer*.
3. **Standoffs Estruturais (M2.5):** A PCB possui quatro furos de montagem nos cantos. Eles são fixados ao suporte principal (impresso em ABS de alta densidade) através de espaçadores roscados (standoffs) M2.5 de Nylon ou Latão. Isto impede a fadiga mecânica, a flexão da placa e o consequente choque contra o cooler durante a trepidação do robô no chão de fábrica.

---

## 4. Infraestrutura de Potência (Power Tree)

A base motriz iRobot Create 3 é alimentada por uma bateria interna inteligente de iões de lítio. Esta bateria fornece uma tensão que varia dinamicamente entre **11.5V (descarga profunda crítica)** e **16.8V (carga máxima em doca)**, com um valor nominal de 14.4V. A Shield unifica a extração de energia a partir desta única bateria central.

### 4.1 Alimentação Principal e Filtragem (Rede `V_BAT`)
A energia é admitida na Shield através de bornes de parafuso industriais do tipo **KF301 (Passo 5.00mm/5.08mm)**. O aperto mecânico previne desconexões por vibração que os jumpers comuns sofreriam.
A proteção primária da Jetson e do sistema é efetuada por um **fusível cilíndrico de ação rápida (Fast-Blow) de 5A** (F1), que atua de forma sacrificial rompendo em milissegundos num evento de curto-circuito, blindando o hardware da NVIDIA.

Os motores de corrente contínua da base geram picos de tensão reversa (*Back-EMF*) e ruído de comutação de escovas. Para proteger o microprocessador, a rede `V_BAT` atravessa um banco de filtragem massivo e desacoplado na Shield:
* **Capacitor Eletrolítico C1 (470µF / 25V / Low-ESR):** Atua como um reservatório de inércia de baixa frequência para compensar afundamentos momentâneos de corrente (*voltage sags*) durante arranques bruscos de locomoção. A margem de isolamento de 25V garante segurança operacional absoluta.
* **Capacitor Cerâmico C2 (100nF):** Desacopla ruídos eletromagnéticos e harmónicos de altíssima frequência (EMI) introduzidos pelo chaveamento PWM dos inversores de ponte H da base motriz.

### 4.2 O Isolamento Térmico e Lógico do Regulador XL4016 (Rede `+5V_EXT`)
O sensor de deteção ambiental MQ-2 possui um elemento resistivo de aquecimento interno fabricado em Dióxido de Estanho ($SnO_2$) que drena constantemente cerca de 200mA a rigorosos 5.0V. Extrair esta carga pesada e térmica através do *Power Management IC* (PMIC) interno da Jetson (pelos pinos de 5V do header) induziria stress térmico massivo na placa-mãe, arriscando *brownouts* e travamentos do sistema operativo Ubuntu.

A solução de engenharia adotada foi delegar esta regulação de alta corrente para um **Conversor DC-DC Buck Step-Down XL4016** montado externamente ao chassi da Shield. O XL4016 aceita os 14.4V brutos e providencia **5.0V estabilizados a até 8A**. Esta linha limpa regressa à Shield pelo borne U5 (`+5V_EXT`), alimentando o MQ-2 de forma totalmente isolada, não gerando aquecimento por Efeito Joule nas trilhas delicadas da PCB e reservando capacidade de corrente para os futuros ecrãs LCD com retroiluminação.

---

## 5. Condicionamento de Sinais e Barramentos

Garantir que os sensores analógicos e digitais funcionem em harmonia com o limite destracional de 3.3V da Jetson exigiu topologias de divisão resistiva rigorosas e a introdução de digitalizadores I2C de precisão.

### 5.1 Barramento SPI de Alta Velocidade (Módulo MFRC522)
Para a autenticação de segurança dos operadores fabris, integrou-se um leitor RFID MIFARE de 13.56 MHz (MFRC522). Este chip da NXP Semiconductors opera nativamente no domínio de 3.3V, permitindo o acoplamento direto sobre o barramento SPI0 nativo da Jetson Orin Nano sem transdutores lógicos (*logic level shifters*).
As linhas de dados (MISO, MOSI, SCK, CS) garantem taxas de transferência determinísticas para validação criptográfica em tempo real, e o pino GPIO 22 foi alocado como *Hardware Reset* (RST) para reiniciar e restabelecer o módulo em caso de falha no barramento ou interferência estática (*timeout*).

### 5.2 Divisor Lógico de Tensão do Sensor MQ-2
Alimentado a 5.0V pela rede `+5V_EXT`, a saída digital (DO) controlada pelo comparador LM393 do módulo MQ-2 emite um impulso retangular de 5.0V exatos quando deteta concentrações perigosas de gás ou fumo. Para impedir a queima do processador da Jetson, implementou-se um atenuador passivo a nível de hardware na PCB usando os resistores **R1** e **R2**:
* Um resistor de **1 kΩ (R1)** em série com a linha de sinal DO do sensor.
* Um resistor de **2 kΩ (R2)** em paralelo referenciado ao Ground comum (GND).
Este nó matemático atesta uma saída constante, rebaixada e segura que é encaminhada ao Pino 15 (GPIO) da Jetson. No nó de software (ROS 2), este pino está configurado como uma *Hardware Interrupt* de borda de subida (*Rising Edge*) que injeta um comando prioritário de paragem de emergência (*Emergency Stop / E-Stop*) na árvore cinemática do Nav2 Stack.

### 5.3 O Digitalizador Analógico-Digital I2C e Telemetria de Bateria (ADS1115)
Como a Jetson Orin Nano carece totalmente de conversores A/D integrados no seu *pinout*, adicionou-se o módulo externo **ADS1115 (Conversor ADC Delta-Sigma de 16 bits)** conectado ao barramento I2C1 (Pinos 3 e 4). 
* **Canal A1 (MQ2_SINAL_A0):** Diretamente ligado à saída analógica (AO) linear do MQ-2 para mapear espacialmente a variação contínua de concentração gasosa em PPM (Partes Por Milhão).
* **Canal A0 (BATERIA_SINAL):** Acoplado a um divisor de tensão de ultraprecisão composto pelos resistores **R3 (10 kΩ)** e **R4 (1 kΩ)**. Esse arranjo atenua a flutuante e perigosa tensão direta da bateria (`V_BAT`) em uma taxa segura de 11:1 antes de ser entregue à porta analógica do ADC.

---

## 6. Memória de Cálculo de Engenharia

Esta secção prova matematicamente a robustez absoluta das escolhas de design e do balanceamento resistivo realizados na Shield.

### 6.1 Condicionamento Lógico do Alarme MQ-2 (5V para ~3.33V)
A tensão proveniente do pino DO do MQ-2 ($V_{in}$) é de 5.0V em caso de alarme máximo. Pela fórmula da lei de Kirchhoff para o divisor resistivo com R1 ($1 k\Omega$) e R2 ($2 k\Omega$):

$$V_{out} = V_{in} \times \left( \frac{R_2}{R_1 + R_2} \right) = 5.0\text{V} \times \left( \frac{2000}{1000 + 2000} \right)$$
$$V_{out} = 5.0\text{V} \times \left( \frac{2}{3} \right) = 3.333\text{V}$$

**Veredicto de Engenharia:** A amplitude analítica de 3.33V é lida perfeitamente como nível lógico ALTO (HIGH) pela porta CMOS da Jetson, operando no limiar seguro exato e impedindo a quebra do dielétrico semicondutor.

### 6.2 Divisor de Telemetria de Bateria (Atenuação 11:1)
No pico extremo de carga elétrica, a bateria entrega $V_{max} = 16.8\text{V}$. A entrada analógica A0 do ADS1115 jamais pode exceder o seu referencial VCC (3.3V). Utilizando a impedância de R3 ($10 k\Omega$) e R4 ($1 k\Omega$):

$$V_{ADC\_MAX} = 16.8\text{V} \times \left( \frac{R_4}{R_3 + R_4} \right) = 16.8\text{V} \times \left( \frac{1000}{10000 + 1000} \right) = 16.8\text{V} \times \left( \frac{1}{11} \right) = 1.527\text{V}$$

**Veredicto de Engenharia:** Mesmo no pico de carga total da iRobot Create 3 (16.8V), a tensão máxima injetada no conversor será de apenas **1.527V**, garantindo uma margem massiva de segurança (cerca de 53% abaixo do limite limite físico de 3.3V). No limite inferior crónico de descarga da bateria (11.5V), a leitura medida será de confortáveis **1.045V**.

### 6.3 Resolução Analítica do Conversor (LSB e FSR)
O ADS1115 fornece 15 bits efetivos de quantização operando em modo *Single-Ended* com GND ($2^{15} = 32.768$ degraus discretos). Configurou-se o Amplificador de Ganho Programável (PGA) no software para um *Full Scale Range* (FSR) de $\pm 2.048\text{V}$, otimizando a leitura:

$$LSB = \frac{2.048\text{V}}{32768} = 0.0000625\text{ V} = 62.5 \mu\text{V}$$

Multiplicando este limite de perceção pelo fator do divisor de tensão da bateria (11x), encontramos o valor real mínimo que o robô distingue na bateria:

$$\text{Sensibilidade} = 62.5 \mu\text{V} \times 11 = 687.5 \mu\text{V} \approx 0.68 \text{ mV}$$

**Veredicto de Engenharia:** O sistema consegue distinguir variações elétricas na tensão da bateria em degraus ínfimos de **0.68 milivolts**. Esta granularidade extrema permite que as redes neuronais ou os nós do ROS 2 gerem curvas estocásticas de *State of Charge* (SoC%) de altíssima fidelidade.

### 6.4 Corrente de Fuga Parasita e Dissipação Térmica
A carga da bateria é drenada de forma parasita continuamente pelo divisor resistivo através da malha R3+R4 ($11 k\Omega$):

$$I_{fuga} = \frac{16.8\text{V}}{11.000 \Omega} = 0.001527\text{ A} \approx 1.53\text{ mA}$$

A potência térmica real dissipada por Efeito Joule pelo resistor de queda principal R3 (10kΩ):

$$P_{dissipada} = I_{fuga}^2 \times R_3 = (0.001527\text{A})^2 \times 10.000 \Omega = 0.0233\text{ W} = 23.3\text{ mW}$$

**Veredicto de Engenharia:** Uma drenagem de 1.53mA é totalmente insignificante para a capacidade de milhares de miliamperes-hora da base Create 3. A potência irrisória de 23.3mW está severamente abaixo dos 250mW máximos suportados pelo resistor SMD/Axial convencional (1/4W), assegurando que o componente opera totalmente frio, prevenindo desvios de leitura provocados pelo Coeficiente de Temperatura.

---

## 7. Estratégias de Blindagem e EMI (Compatibilidade Eletromagnética)

Pavilhões industriais e células de manufatura geram ruídos eletromagnéticos agressivos. O projeto adotou regras rigorosas de *layout* de PCB para garantir estabilidade:
1. **Dimensionamento Massivo de Trilhas:** As malhas de potência `V_BAT` e `+5V_EXT` foram roteadas muito espessas (até 2.0mm / 80 mils) para suportar altas correntes sem estrangulamento indutivo, enquanto sinais digitais rápidos (SPI/I2C) utilizaram trilhas finas (0.25mm) para mitigar capacitâncias parasitas.
2. **Plano de Terra Sólido e Unificado (Copper Pour):** Todo o *Bottom Layer* foi preenchido com malha de GND contínua. Este escudo térmico e eletromagnético minimiza radicalmente as áreas dos *loops* de corrente e protege as linhas I2C e SPI contra a irradiação indutiva provocada pelos motores elétricos do robô.
3. **Clearance Analógico (Mitigação de Diafonia):** As pistas sensíveis analógicas de leitura de gás e bateria foram roteadas propositadamente longe dos *clocks* do barramento SPI ( que oscilam em megahertz) para evitar indução capacitiva cruzada e acoplamento mútuo (*Crosstalk*).

---

## 8. Mapeamento Físico e Netlist Completo

A integridade do *Hardware Layer* é demonstrada no Netlist final validado exportado do EasyEDA Pro / PADS.

| Nome da Net (Rede) | Componentes e Pinos Atribuídos | Descrição da Função de Engenharia Elétrica |
| :--- | :--- | :--- |
| **`V_BAT`** | U2.1, U3.1, F1.2, C1.1, C2.2, R3.1 | Barramento primário da bateria (11.5V a 16.8V). Rota de alta potência, protegida pelo fusível F1 e estabilizada por C1/C2. |
| **`+5V_EXT`** | U5.1, MQ2.1, U_LCD.1 | Alimentação estável de alta corrente gerada pelo módulo XL4016 externo para abastecer o aquecedor do MQ-2 e periféricos. |
| **`+3V3`** | HDR1.1, RFID.1, U4.8 | Referência de tensão lógica estável gerada pela Jetson. Alimenta a lógica digital do RFID MFRC e do ADC ADS1115. |
| **`GND`** | U3.2, C1.2, C2.1, MQ2.2, R2.2, RFID.2, HDR1.6, U_LCD.4, U4.1, U4.3, U5.2, R4.2 | Plano de terra referencial equipotencial massivo e contínuo da Shield. |
| **`BATERIA_SINAL`**| R3.2, R4.1, U4.4 (Canal A0) | Tensão analógica 11 vezes rebaixada da bateria para telemetria segura. Max 1.52V. |
| **`MQ2_SINAL_3V3`**| R1.2, R2.1, HDR1.15 | Impulso atenuado lógico de alarme do MQ-2 (3.33V) direcionado à GPIO Pino 15 da Jetson. |
| **`MQ2_SINAL_A0`** | MQ2.4, U4.5 (Canal A1) | Leitura analógica linear bruta da curva de concentração gasosa (AO) do sensor MQ-2. |
| **`I2C_SDA`** | HDR1.3, U_LCD.2, U4.9 | Dados seriais bidirecionais (*Serial Data*) do Barramento I2C1 nativo compartilhado entre ADS1115 e LCD. |
| **`I2C_SCL`** | HDR1.4, U_LCD.3, U4.10 | Clock serial (*Serial Clock*) sincronizador gerado pelo mestre I2C1 (Jetson Orin Nano). |
| **`SPI_MOSI`** | HDR1.19, RFID.5 | *Master Out Slave In* - Linha de comandos enviados da Jetson para o leitor MFRC522. |
| **`SPI_MISO`** | HDR1.21, RFID.4 | *Master In Slave Out* - Retorno dos dados criptográficos validados das tags RFID para a Jetson. |
| **`SPI_SCK`** | HDR1.23, RFID.6 | Clock Serial gerado pela Jetson regulando a taxa de amostragem síncrona do SPI0. |
| **`SPI_CS`** | HDR1.24, RFID.7 | *Chip Select* (Active Low) controlado pela Jetson para ativação do escravo RFID. |
| **`RFID_RST`** | HDR1.22, RFID.3 | Pino de *Hardware Reset* alocado no header para reinicialização forçada do módulo RFID. |

---

## 9. Bill of Materials (BOM)

Tabela unificada com o detalhamento completo dos componentes COTS, passivos e conexões mecânicas homologadas para a produção da Shield industrial:

| Referência | Qtd | Especificação Técnica e Descrição do Componente | Encapsulamento / Package | Tipo de Montagem (Assembly) | Função Arquitetural na Placa |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **SBC** | 1 | NVIDIA Jetson Orin Nano Developer Kit (8GB RAM, CPU ARM 6-Cores, GPU Ampere de 40 TOPS) | DevKit Pro Module | Fixação por Standoffs (M2.5) | Cérebro computacional central, executa ROS 2 Humble em Docker, pacotes SLAM e IA (YOLOv8). |
| **REG** | 1 | Módulo Buck Step-Down baseado no robusto CI XL4016 (Ajustado p/ 5.0V / 8A) | Módulo Externo Volumoso | Fixação no Chassi Metálico | Rebaixa a bateria instável para 5V estáveis e isola o ruído/térmica longe da Jetson. |
| **U4** | 1 | Módulo ADC 16-bits I2C Texas Instruments ADS1115 (Com PGA Integrado) | Módulo Vertical COTS | Soldadura THT (Furo Passante) | Digitaliza sinais analógicos precisos da bateria e dos gases. |
| **RFID** | 1 | Módulo Leitor RFID/NFC MFRC522 (Frequência 13.56MHz) c/ suporte MIFARE ISO/IEC 14443 A | Módulo Vertical COTS | Soldadura THT (Furo Passante) | Barreira restritiva de segurança fabril e autenticação obrigatória do operador. |
| **MQ2** | 1 | Módulo Sensor Gás Combustível e Fumo MQ-2 (Aquecedor microfabricado SnO2 e comparador LM393) | Módulo Vertical COTS | Soldadura THT (Furo Passante) | Sensoriamento ambiental precoce e ativação do E-Stop cinemático contra princípios de incêndio. |
| **U(1-3, 5)**| 4 | Borne de Parafuso robusto KRE KF301-5.0-2P (Passo 5.00mm/5.08mm) em termoplástico industrial | KF301 2-Pinos | Soldadura THT (Furo Passante) | Conexão imune a vibrações severas para barramentos de potência e alimentação de periféricos. |
| **F1** | 1 | Fusível de Vidro cilíndrico de Ação Rápida (Fast-Blow) 5A (Tensão de isolamento de 250V/300V) | Cilíndrico 5x20 mm | Clipes Metálicos (Porta-Fusíveis) | Elemento sacrificial para proteção elétrica da Jetson e do circuito contra curto-circuitos. |
| **C1** | 1 | Capacitor Eletrolítico Alumínio 470µF / 25V (Especificação especial de baixo ESR) | Radial Can 8mm | Soldadura THT (Furo Passante) | Amortecimento inercial de transientes, quedas de baixa frequência e compensação motriz. |
| **C2** | 1 | Capacitor Cerâmico Multicamadas (MLCC) 100nF / 50V de alto dielétrico | Axial/Radial THT | Soldadura THT (Furo Passante) | Desacoplamento rápido de alta frequência indutiva (PWM) dos inversores da base Create 3. |
| **R1** | 1 | Resistor Filme de Carbono/Metal 1 kΩ (Tolerância padronizada de 5%, 1/4W) | Axial/SMD | Soldadura THT / SMT | Braço resistivo em série limitador lógico do alarme digital DO (5V) proveniente do sensor MQ-2. |
| **R2** | 1 | Resistor Filme de Carbono/Metal 2 kΩ (Tolerância padronizada de 5%, 1/4W) | Axial/SMD | Soldadura THT / SMT | Braço resistivo paralelo aterrado rebaixando o alarme de 5V para exatos 3.33V seguros para a NVIDIA. |
| **R3** | 1 | Resistor de Película Metálica 10 kΩ (Tolerância laboratorial de 1%, 1/4W) | Axial/SMD | Soldadura THT / SMT | Braço resistivo em série de alta precisão do divisor de tensão da telemetria (Canal A0). |
| **R4** | 1 | Resistor de Película Metálica 1 kΩ (Tolerância laboratorial de 1%, 1/4W) | Axial/SMD | Soldadura THT / SMT | Braço resistivo em paralelo aterrado (GND) do divisor de telemetria da bateria. |
| **HDR1** | 1 | Conector Fêmea Extra Alto (*Stacking Header / Extra Tall*) - Isolamento estendido de 11mm a 15mm | Receptáculo 2x20 (40P) | Soldadura THT no Bottom Layer (Espelhado) | Cria distanciamento aerodinâmico vital (Gap de ar) entre a PCB da Shield e as aletas do dissipador térmico da Jetson. |
| **ESP** | 4 | Espaçador cilíndrico sextavado roscado M2.5 (Standoff) fabricado em Nylon isolante ou Latão niquelado | Standoff M2.5 | Travamento por Parafuso Mecânico | Ancoragem rígida que liga as placas e previne fraturas por fadiga ou flexão da PCB sob stress mecatrónico. |

---

## 10. Integração de Software: ROS 2 e Docker

A decisão de arquitetura por isolar os processos num *runtime* de contêineres Docker impõe desafios formidáveis de passagem de hardware (*Hardware Passthrough*). O kernel *host* da Jetson precisa ser modificado a nível de *boot* e os descritores de dispositivos expostos com exatidão no ficheiro Compose do ROS 2.

### 10.1 Preparação Específica do Host (Modificação Jetson-IO)
Os barramentos SPI e I2C nativos não vêm ativos de fábrica na imagem do JetPack Ubuntu. O desenvolvedor deve invocar a ferramenta proprietária da NVIDIA para reconfigurar e recompilar a árvore de dispositivos (*Device Tree Overlay*):
```bash
sudo /opt/nvidia/jetson-io/jetson-io.py
# 1. No menu interativo, navegue por "Configure Jetson 40pin Header".
# 2. Habilite explicitamente os periféricos "spidev" (SPI) e "i2c1" (I2C).
# 3. Guarde as alterações, aplique ao bootloader e reinicie o sistema físico host.
### 10.1 Preparação Específica do Host (Modificação Jetson-IO)
Os barramentos SPI e I2C nativos não vêm ativos de fábrica na imagem padrão do JetPack Ubuntu. O desenvolvedor deve invocar a ferramenta proprietária da NVIDIA para reconfigurar e recompilar a árvore de dispositivos (*Device Tree Overlay*) diretamente no terminal do sistema operacional hospedado (*Host*):

```bash
sudo /opt/nvidia/jetson-io/jetson-io.py
# 1. No menu interativo, navegue por "Configure Jetson 40pin Header".
# 2. Habilite explicitamente os periféricos "spidev" (SPI) e "i2c1" (I2C).
# 3. Guarde as alterações, aplique ao bootloader e reinicie o sistema físico host.
```

### 10.2 Configuração Estrita do Docker Compose
A decisão de engenharia por isolar os processos da stack de robótica num runtime de contêineres Docker impõe o desafio de passagem direta de hardware (*Hardware Passthrough*). O contêiner virtual do ROS 2 Humble requer ativação do modo privilegiado e acesso direto aos descritores de arquivo de Kernel localizados no diretório `/dev`:

```yaml
version: '3.8'
services:
  pequi_hardware_layer:
    image: pequi/turtlebot4_mvp:humble
    runtime: nvidia # Permite acesso à Runtime e aceleração CUDA da GPU
    privileged: true # Mandatório para chamadas de interrupção GPIO no Python
    network_mode: host # Sincroniza o Discovery do protocolo DDS do ROS2
    devices:
      - "/dev/i2c-1:/dev/i2c-1"           # Concessão do canal I2C (ADC ADS1115)
      - "/dev/spidev0.0:/dev/spidev0.0"   # Concessão do canal SPI0 (RFID MFRC522)
      - "/dev/gpiochip1:/dev/gpiochip1"   # Concessão de Interrupção por Hardware (Alarme MQ-2) e RST
    environment:
      - ROS_DOMAIN_ID=0
    restart: always # Recupera o nó automaticamente após reboots fabris
```

---

## 11. Roteiro de Expansão (Fase 2)

O TurtleBot 4 MVP atua como uma robusta prova de conceito (PoC) para navegação logística operando com a base cinemática iRobot em piso industrial. A malha elétrica da Shield foi dimensionada deliberadamente com tolerâncias excedentes para receber as atualizações agendadas para a Fase 2 (Industry 4.0) sem qualquer necessidade de redesenho da PCB atual.

### 11.1 Desoneração Computacional Assíncrona (Microcontrolador Auxiliar ESP32)
A inserção de dezenas de sensores periféricos suplementares (como *arrays* LiDAR secundários, módulos ultrassónicos, sensores de penhasco infravermelhos e fins-de-curso mecânicos industriais) geraria um custo proibitivo de consumo de I/O em *polling* contínuo na CPU da Jetson. O roadmap tecnológico prevê a instalação nativa de um SoC dual-core de 32 bits (como o **ESP32**) na própria malha da arquitetura.

Este ESP32 lidará de forma autónoma, isolada e puramente determinística com todo o IO analógico/digital secundário de baixo nível. Utilizando a abstração da *framework* **Micro-ROS**, o microcontrolador empacotará os dados em frames DDS e transferirá essa informação serializada diretamente para a Jetson via protocolo UART assíncrono de altíssima velocidade (taxas de 921600 baud ou superior). A GPU Ampere e os núcleos Cortex-A78AE da NVIDIA ficarão blindados destas interrupções, dedicando-se inteiramente à navegação SLAM 3D e tarefas de IA.

### 11.2 Transformação Definitiva em Edge Gateway IoT (MQTT, InfluxDB, Painéis Grafana)
A Shield eletrônica e a Jetson assumem o posto de convergência final em Indústria 4.0. Os dados brutos analógicos coletados do MQ-2, as *hash keys* criptográficas extraídas da leitura dos crachás RFID MFRC522 e o estado estocástico de degradação da bateria (SoC% via I2C) não serão armazenados apenas localmente.

Um nó de rede no ROS 2 empacotará todas estas variáveis dinâmicas de telemetria num string de dados unificado com formato estruturado **JSON**. Através de clientes de baixo *overhead* **MQTT (Message Queuing Telemetry Transport)**, este string JSON viajará via a interface Wi-Fi de banda dupla industrial da Jetson diretamente para um *Broker* centralizado (como o Eclipse Mosquitto) instalado no Centro de Processamento de Dados (CPD) da fábrica. Este fluxo contínuo será arquivado numa base de dados otimizada para séries temporais (Time-Series Database, como **InfluxDB** ou Data Warehouses **Firebase**). Os engenheiros de planta acessarão remotamente estas informações através de **Dashboards dinâmicos em Grafana**, correlacionando as métricas e gerando relatórios de *Predictive Maintenance* (Manutenção Preditiva), programando a troca de baterias ou calibração de motores muito antes de uma avaria estatística interromper o fluxo no chão de fábrica.

### 11.3 Monitorização Autárquica e Redundância Visual Local (Display LCD I2C em Fábrica)
Em caso de quebra no servidor Wi-Fi, o pin-header de expansão `U_LCD` aguarda ativamente a ligação *plug-and-play* de um display alfanumérico padrão LCD industrial de 16x2 polegadas (com retroiluminação) impulsionado por um circuito integrado expansor **PCF8574**. 

O chip expansor PCF8574 converte os pinos de dados paralelos do LCD e conversa nativamente em protocolo I2C puro, executando o *Daisy-chaining* com fios partilhados no barramento (pinos 3 e 4). Devido à capacidade de identificação de endereços de barramento, ele coabitará de forma transparente ao lado do ADS1115 (sem colisões lógicas ou desperdício de pinos GPIO). O visor LCD fornecerá um sistema ótico de redundância local:
* Exibirá alarmes visuais intermitentes de "Bateria Crítica (<11.5V)".
* Exibirá aprovações locais ("CARTÃO DE OPERADOR MFRC AUTORIZADO") aos técnicos da linha de montagem, sem exigir que abram laptops para aceder ao ambiente CLI / SSH Docker do robô.

A intervenção visual precoce estimulada pelo LCD previne esgotamentos mecânicos catastróficos. Descargas abaixo de 11.5V desencadeiam interrupções súbitas da PMIC, o que corrompe de forma fatal a partição lógica de 128GB NVMe SSD ou MicroSD, destruindo o Ubuntu Server OS e inutilizando o robô.

---

## 12. Guia de Troubleshooting e Manutenção

Em operações fabris duras e implacáveis, a Shield e os seus componentes mecânicos enfrentam degradação inevitável. Este quadro consolida e mapeia as principais anomalias sistémicas e a respetiva abordagem de engenharia para correção imediata em manutenção.

| Anomalia / Sintoma Registado | Causa Físico-Química e Justificação Teórica Mais Provável | Resolução de Engenharia, Testes e Ação Corretiva Recomendada |
| :--- | :--- | :--- |
| **Robô desliga-se abruptamente (Blackout) no pico de aceleração ou reversão de sentido cinemático.** | Quedas de tensão massivas (Voltage Sags) no barramento `V_BAT` induzem o desligamento forçado do PMIC da Jetson. O banco capacitivo falhou em fornecer a energia inercial de compensação, ou a bateria cruzou o limiar letal dos 11.5V sob stress indutivo dos motores. | Falha sistémica no banco capacitivo. Verifique e analise a integridade estrutural do condensador eletrolítico C1 (estufamento, vazamento de eletrólito ou ruptura dielétrica no topo). Aplique torquímetro e verifique o aperto e a tração mecânica dos parafusos dos bornes e Force carregamento imediato na Doca iRobot. |
| **Pilha de Navegação do ROS 2 aborta e lança exceção do kernel Linux `OSError: [Errno 121] Remote I/O error` ao ler o ADS1115.** | Erro fatal de Timeout na comunicação I2C1 do Host Ubuntu. A Jetson está a interrogar o canal, mas o escravo I2C não responde com o ACK bit (Acknowledge). | Indício forte de conflito de endereço eletrónico, soldadura fria (mau contato) ou fios I2C trocados acidentalmente entre os pinos 3 (SDA) e 4 (SCL). Paralise o container Docker temporariamente, aceda via SSH e corra o comando utilitário `sudo i2cdetect -y 1` no host; o endereço hexadecimal estrito `0x48` (ADS1115 nativo) deve obrigatoriamente surgir ativo na matriz de dispositivos do barramento. |
| **Autenticação bloqueada: O Módulo MFRC522 (RFID) rejeita tags válidas ou o nó de software reporta Timeout em loop infinito contínuo.** | A interface SPI de dados está ativa, porém sem sinal de sincronismo de relógio, ou o firmware da memória interna do MFRC encontra-se congelado ou encravado por EMI. | Inspecione com um osciloscópio o ruído massivo transitando no plano 3V3. Reveja o código Python: Garanta inequivocamente que a sua classe de controlo de nó força e executa a sequência de *toggle* por software `LOW -> HIGH -> LOW` no pino GPIO 22 (`RFID_RST`) no momento do `__init__`, reiniciando o periférico via Hardware antes de despachar a primeira tentativa de leitura de cartões MIFARE. |
| **Leituras da interface de telemetria de Bateria reportam tensões completamente erráticas, randómicas e flutuantes no tópico (0.81V, seguido de 0.12V, e depois picos irrealistas).** | O pino analógico A0 do chip ADC encontra-se numa situação de "Porta Aberta" (*Floating Pin*), atuando como uma mini-antena receptora de ruído AM/FM estático do ambiente de fábrica. | Trata-se de uma falha franca no hardware divisor. O resistor axial/SMD R3 (10kΩ) fundiu abrindo o circuito, ou uma soldadura fria (oxidada) mecanicamente isolou a base de cobre do divisor de tensão. Desligue a energia, aplique o modo de continuidade/resistência no multímetro e ateste se o divisor R3+R4 exibe aproximadamente 11kΩ. |
| **O alarme crítico do sensor MQ-2 dispara repetidamente com *falsos positivos* durante o robô estar em andamento rápido.** | A avaria é fundamentalmente mecânica e advém do Trimpot azul soldado no topo do módulo MQ-2. O módulo induz falsamente o comparador LM393. | A ressonância e a vibração estrutural de alta amplitude do robô a transitar pelas juntas de dilatação do pavimento industrial está a rodar e a afrouxar milimetricamente o eixo interno do trimpot, descalibrando de forma imprevisível a resistência limitadora do limiar de deteção. **Solução Definitiva:** Recalibre o potenciómetro em bancada limpa e sele/lacre hermeticamente a engrenagem plástica superior e as bases metálicas com aplicação de verniz fixador ou esmalte de alta resistência mecânica para travar de forma permanente qualquer trepidação. |

---

## 13. Referências Técnicas

A fiabilidade e validade deste documento e da arquitetura produzida assentam fortemente nos guiões, relatórios de pesquisa exaustivos, *datasheets* laboratoriais de fabricantes e guias metodológicos de desenvolvimento que regem o panorama de Indústria 4.0 global.

1. **Documentação Oficial e Repositório do Ecossistema ROS 2 (Distribuição Humble Hawksbill):** Fundamentos, normas de compatibilidade entre distribuições LTS, guias estritos de alta abstração de hardware (HAL), e topologias de comunicação distribuída com DDS via publishers e subscribers. Portal central disponível online no index: [docs.ros.org/en/humble/](https://docs.ros.org/en/humble/)
2. **NVIDIA Jetson Embedded Support Center & NVIDIA Developer Docs:** Guias elétricos exaustivos do PMIC e de *power sequencing* no boot de sistema, esquemas de *pinmuxing* avançado, procedimentos vitais para a reconfiguração em tempo real e compilação do núcleo e da *Device Tree Overlay*. Documentação acerca dos limites operacionais, limites lógicos restritos ao domínio de 3.3V no SoC Ampere e métricas de regulação térmica do ventilador PWM. [developer.nvidia.com/embedded](https://developer.nvidia.com/embedded)
3. **iRobot Create 3 Educational Robot Platform e TurtleBot 4 Open-Source Hardware Repository:** Plantas CAD 3D originais, dimensões espaciais mecânicas precisas em milímetros, e especificação das grelhas de fixação nativas (furos roscados M3) no convés superior. Compreensão das rotinas cinemáticas implementadas e especificação base do sistema eletrónico. Arquivos disponíveis e hospedados publicamente no GitHub: [github.com/turtlebot/turtlebot4-hardware](https://github.com/turtlebot/turtlebot4-hardware/tree/master/TurtleBot%204)
4. **Bases de Conhecimento Experimental - Articulated Robotics & Random Nerd Tutorials:** Utilização de provas de conceito empíricas, relatórios de arquitetura de instrumentação analógica/matemática complexa. Exemplos práticos de implementação de multiplexagem massiva e *daisy chaining* utilizando o protocolo I2C acoplado a ecrãs LCD industriais HD44780 em harmonia com chips expansores da série PCF8574. Guias intensivos sobre modelação transitória de picos elétricos e amortecimento de perturbações eletromagnéticas nocivas provocadas pelo fenómeno da tensão de *Back-EMF* induzida transversalmente aos terminais dos motores e atuadores de corrente contínua escovados das bases de tração.
5. **Datasheets de Fabricantes e Engenharia de Semicondutores (Texas Instruments & NXP):** *Datasheet* oficial laboratorial emitido pela Texas Instruments detalhando as curvas não lineares e as características paramétricas e de tolerância de erro de *offset* e ganho do ADC ADS1115 (detalhes sobre a arquitetura do núcleo Delta-Sigma, o impacto do ganho do conversor de Programmable Gain Amplifier - PGA em relação ao ruído sistémico (SNR)). Referencial e diagrama de blocos de estados e *timings* oficiais estipulados pela NXP Semicondutores para as interrogações e comandos de escrita e leitura síncrona nos bancos de memória via protocolo SPI do controlador biométrico inteligente (Leitor/Transcetor MFRC522 ISO/IEC 14443).

---

## 14. Imagens e Anexos

![PCB 2D](/Hardware/PCB/2D_PCB.png)
![PCB 3D_1](/Hardware/PCB/3D_PCB1_1.png)
![PCB 3D_2](/Hardware/PCB/3D_PCB1_2.png)
![PCB 3D_3](/Hardware/PCB/3D_PCB1_3.png)
![Esquemático](/Hardware/Schematic/Schematic.png)


---