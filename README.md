# Estrutural 

A equipe estrutural tem como objetivo implementar a placa Jetson Orion nano, da NVIDIA, no lugar da Raspberry PI 4, originalmente proposta para o robô Turtlebot4

## Modelo da placa

O modelo da nova placa foi obtido pelo respositório GrabCAD,  https://grabcad.com/library/nvidia-jetson-nano-4

<img width="1066" height="612" alt="Captura de tela 2026-05-21 111509" src="https://github.com/user-attachments/assets/05a5d6d0-3768-49a2-a2e6-912bbcb902f1" />

## Modelo do robô

O modelo do robô TurtleBot4 foi obtido pelo GitHub, https://github.com/turtlebot/turtlebot4-hardware/tree/master/TurtleBot%204

<img width="1054" height="613" alt="Captura de tela 2026-05-21 112447" src="https://github.com/user-attachments/assets/68cddd94-a74a-48ec-af7d-6e8389d2d700" />

## Desafios de instalação 

A superfície de fixação da plataforma robot Create 3 fornece um grid 12x12 com furos de 3mm de diâmetro. Com base nisso modelamos nossa primeira iteração 

<img width="579" height="519" alt="Captura de tela 2026-05-19 210758" src="https://github.com/user-attachments/assets/059317dd-3e23-47fc-8cdd-670ec4e1e5d6" />

### Melhorias 

Tendo em vista a baixa sujeição da peça a forças concentradas e o custo de produção com filamentos de engenharia, decidimos remover material em excesso, mantendo a função 
primária de fixação

<img width="660" height="508" alt="Captura de tela 2026-05-20 181712" src="https://github.com/user-attachments/assets/2019038b-5ec1-48bb-9088-131bee0bc024" />

### Propostas 

Para fixação da placa ao suporte, optamos por parafusos M2.5x0.45, combinados com insertos roscados de latão, que podem ser inseridos no plástico por um ferro de solda

<img width="497" height="468" alt="Captura de tela 2026-05-21 114533" src="https://github.com/user-attachments/assets/18aea4e3-6269-4b64-8621-fb095188ccab" />
 
 ### Fabricação 

Imprimimos a peça em ABS, para resistência mecânica e térmica adequada (a concluir) 
