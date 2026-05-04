# Guia de Desenvolvimento - Projeto Nivelamento

## Visão Geral

O **Equipment Rent** propõe um sistema moderno de reservas e controle de equipamentos, integrando funcionalidades de automação e feedback em tempo real via **MQTT**. Esse sistema permite que usuários reservem recursos como **salas, máquinas ou estações de trabalho**, enviem comandos para os equipamentos e recebam respostas em tempo real, garantindo maior eficiência e controle.

## Objetivos do Sistema

- Permitir a reserva de equipamentos via API REST.
- Controlar equipamentos remotamente através de comandos enviados via **MQTT** (opcional).
- Receber e registrar feedbacks dos equipamentos em tempo real.
- Garantir acesso controlado por meio de **JWT Authentication**.
- Fornecer um painel de acompanhamento atualizado em tempo real via **WebSockets** (opcional).

---

## Arquitetura do Sistema

### 🏭 Fluxo de Funcionamento

1. **Reserva do Equipamento**
   - O usuário reserva um equipamento por meio da API.
   - O sistema armazena os dados da reserva no banco de dados.
   
2. **Liberação e Controle do Equipamento**
   - Quando a reserva inicia, o usuário pode liberar ou iniciar o uso via API.
   - O backend publica comandos MQTT no tópico correspondente.
   
3. **Resposta do Equipamento**
   - O equipamento responde via MQTT informando seu status.
   - O backend processa essa resposta e atualiza o banco de dados.
   
4. **Durante o Uso**
   - O usuário pode enviar comandos adicionais (ajustar parâmetros, parar, reiniciar).
   - O equipamento continua enviando atualizações de status.
   
5. **Finalização**
   - O equipamento pode enviar dados como tempo de uso, logs e possíveis erros.
   - O backend encerra a reserva e registra o histórico.

---

## 🔧 Tecnologias e Ferramentas Utilizadas

| Conceito             | Aplicação                      |
|----------------------|--------------------------------|
| **FastAPI**  | API REST para reservas e controle de equipamentos |
| **Tortoise ORM** | Persistência das reservas e status |
| **gmqtt** | Cliente MQTT para envio e recebimento de mensagens |
| **Mosquitto Broker** | Broker MQTT para comunicação entre API e equipamentos |
| **WebSockets** (opcional) | Atualizações em tempo real para frontend |
| **JWT Authentication** | Controle de acesso seguro à API |
| **Background Tasks / asyncio** | Processamento assíncrono de mensagens MQTT |
| **Docker Compose** | Orquestração de containers para API, banco e broker |

---

## 🎯 Definição de Tópicos MQTT

| Tópico                         | Descrição |
|--------------------------------|----------------------------------------|
| **equipments/{id}/commands**  | Publicação de comandos para os equipamentos |
| **equipments/{id}/status**    | Equipamento publica status atual |
| **equipments/{id}/feedback**  | Dados ou feedbacks enviados após o uso |

---

## 🗃️ Estrutura do Projeto

```bash
/backend
├── app
│   ├── api                # Endpoints da API (reservas, comandos)
│   ├── mqtt_client        # Cliente MQTT para publicação e assinatura
│   ├── database           # Modelos Tortoise
│   ├── services           # Regras de negócio (validações, lógica de reservas)
│   ├── schemas            # Pydantic schemas para validação de dados
│   ├── core
│   │   └── config.py      # Configuração do Broker, DB e Autenticação
│   └── main.py            # Ponto de entrada da API
├── docker-compose.yml     # Orquestração de API, Banco de Dados e MQTT Broker
└── README.md              # Documentação do projeto
```

---

## 🔍 Modelagem das Entidades

### 1. Users (Usuários)
Armazena informações sobre os usuários do sistema.
- **id** (UUID, PK) - Identificador único do usuário.
- **name** (VARCHAR(60), NOT NULL) - Nome do usuário.
- **email** (VARCHAR(60), UNIQUE, NOT NULL) - Email do usuário.
- **is_active** (BOOLEAN, DEFAULT TRUE) - Indica se o usuário está ativo.
- **created_at** (TIMESTAMP, DEFAULT now()) - Data de criação do registro.

### 2. Equipments (Equipamentos)
Armazena os equipamentos disponíveis no sistema.
- **id** (UUID, PK) - Identificador único do equipamento.
- **name** (VARCHAR(60), UNIQUE, NOT NULL) - Nome do equipamento.
- **current_status_id** (UUID, FK -> EquipmentStatuses.id) - Status atual do equipamento.
- **location** (UUID) - Localização do equipamento.
- **last_heartbeat** (TIMESTAMP) - Última comunicação do equipamento.
- **created_at** (TIMESTAMP, DEFAULT now()) - Data de criação do registro.

### 3. EquipmentStatuses (Status dos Equipamentos)
Armazena os diferentes status que um equipamento pode ter.
- **id** (UUID, PK) - Identificador único do status.
- **name** (VARCHAR(60), UNIQUE, NOT NULL) - Nome do status.
- **created_at** (TIMESTAMP, DEFAULT now()) - Data de criação do registro.

### 4. EquipmentStatusLogs (Logs de Status de Equipamento)
Registra as mudanças de status dos equipamentos.
- **id** (UUID, PK) - Identificador único do log.
- **status_id** (UUID, FK -> EquipmentStatuses.id, NOT NULL) - Status registrado.
- **equipment_id** (UUID, FK -> Equipments.id, NOT NULL) - Equipamento correspondente.
- **details** (VARCHAR(300)) - Informações adicionais sobre a mudança de status.
- **reported_at** (TIMESTAMP, DEFAULT now()) - Data do evento.
- **created_at** (TIMESTAMP, DEFAULT now()) - Data de criação do registro.

### 5. ReservationStatuses (Status de Reservas)
Armazena os diferentes status de uma reserva.
- **id** (UUID, PK) - Identificador único do status.
- **name** (VARCHAR(60), UNIQUE, NOT NULL) - Nome do status.
- **created_at** (TIMESTAMP, DEFAULT now()) - Data de criação do registro.

### 6. Reservations (Reservas)
Armazena informações sobre as reservas feitas pelos usuários.
- **id** (UUID, PK) - Identificador único da reserva.
- **user_id** (UUID, FK -> Users.id, NOT NULL) - Usuário que realizou a reserva.
- **equipment_id** (UUID, FK -> Equipments.id, NOT NULL) - Equipamento reservado.
- **start_time** (TIMESTAMP, NOT NULL) - Horário de início da reserva.
- **end_time** (TIMESTAMP, NOT NULL) - Horário de término da reserva.
- **status_id** (UUID, FK -> ReservationStatuses.id, NOT NULL) - Status da reserva.
- **created_at** (TIMESTAMP, DEFAULT now()) - Data de criação do registro.

### 7. CommandTypes (Tipos de Comandos)
Define os diferentes tipos de comandos que podem ser enviados para um equipamento.
- **id** (UUID, PK) - Identificador único do tipo de comando.
- **name** (VARCHAR(60), UNIQUE, NOT NULL) - Nome do tipo de comando.
- **created_at** (TIMESTAMP, DEFAULT now()) - Data de criação do registro.

### 8. Commands (Comandos)
Registra comandos enviados aos equipamentos.
- **id** (UUID, PK) - Identificador único do comando.
- **command_type_id** (UUID, FK -> CommandTypes.id, NOT NULL) - Tipo do comando.
- **equipment_id** (UUID, FK -> Equipments.id, NOT NULL) - Equipamento que receberá o comando.
- **payload** (VARCHAR(200)) - Dados do comando.
- **created_at** (TIMESTAMP, DEFAULT now()) - Data de criação do registro.

### 9. UserAuth (Autenticação de Usuários)
Armazena as credenciais dos usuários.
- **id** (UUID, PK) - Identificador único do registro.
- **username** (VARCHAR(60), UNIQUE, NOT NULL) - Nome de usuário para login.
- **password_hash** (VARCHAR(100), NOT NULL) - Hash da senha do usuário.
- **user_id** (UUID, FK -> Users.id, NOT NULL) - Referência ao usuário.
- **created_at** (TIMESTAMP, DEFAULT now()) - Data de criação do registro.


---

## 🛠 **Endpoints da API**

### 📌 **Autenticação**
1. `POST /auth/register`
   - Permite criar um novo usuário na plataforma.
   - Requer `name`, `email`, `password`.

2. `POST /auth/login`
   - Gera um token JWT para autenticação do usuário.
   - Requer `username` e `password`.

3. `GET /auth/me`
   - Retorna informações do usuário autenticado.

---

### 👤 **Usuários**
4. `GET /users`
   - Lista todos os usuários cadastrados.

5. `GET /users/{user_id}`
   - Retorna detalhes de um usuário específico.

6. `PATCH /users/{user_id}`
   - Atualiza informações do usuário (ex: `name`, `email`).

7. `DELETE /users/{user_id}`
   - Remove um usuário do sistema.

---

### 🔧 **Equipamentos**
8. `GET /equipments`
   - Retorna todos os equipamentos cadastrados.

9. `GET /equipments/{equipment_id}`
   - Retorna detalhes de um equipamento específico.

10. `POST /equipments`
    - Adiciona um novo equipamento ao sistema.

11. `PATCH /equipments/{equipment_id}`
    - Atualiza dados do equipamento (ex: `name`, `location`).

12. `DELETE /equipments/{equipment_id}`
    - Remove um equipamento.

13. `GET /equipments/{equipment_id}/status`
    - Retorna o status atual do equipamento.

---

### 📅 **Reservas**
14. `POST /reservations`
    - Cria uma nova reserva de equipamento.
    - Requer `user_id`, `equipment_id`, `start_time`, `end_time`.

15. `GET /reservations`
    - Lista todas as reservas.

16. `GET /reservations/{reservation_id}`
    - Retorna detalhes de uma reserva específica.

17. `PATCH /reservations/{reservation_id}`
    - Atualiza status de uma reserva.

18. `DELETE /reservations/{reservation_id}`
    - Cancela uma reserva.

---

### 💽 **Comandos**
19. `POST /commands`
    - Envia um comando para um equipamento via MQTT.
    - Requer `equipment_id`, `command_type_id`, `payload` (opcional).

20. `GET /commands`
    - Retorna todos os comandos enviados.

21. `GET /commands/{command_id}`
    - Retorna detalhes de um comando específico.

---

### 📊 **Logs e Status**
22. `GET /equipment-status`
    - Lista todos os status possíveis de equipamentos.

23. `GET /equipment-status-logs`
    - Retorna logs de status dos equipamentos.

24. `GET /equipment-status-logs/{equipment_id}`
    - Retorna logs de um equipamento específico.