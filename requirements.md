# 📌 Requisitos Básicos do Projeto

## 📖 Visão Geral
O objetivo deste projeto é desenvolver um sistema que permita a reserva e o controle remoto de equipamentos. A solução deverá oferecer um meio eficiente para que usuários possam reservar equipamentos, enviar comandos para operá-los e receber feedback em tempo real sobre seu status. 

O sistema será composto por uma API RESTful para gerenciar as reservas e os comandos, além de um sistema de comunicação baseado em **MQTT** para interagir com os equipamentos. A autenticação e autorização serão implementadas via **JWT**, garantindo segurança no acesso aos recursos.

---

## 🎯 Requisitos Funcionais

### 🔹 Gestão de Usuários
- O sistema deve permitir o cadastro, autenticação e gerenciamento de usuários.
- Deve ser possível associar um usuário a diferentes perfis de acesso (ex: Administrador, Operador). (opcional)
- Os usuários devem poder recuperar a senha através de um mecanismo seguro. (opcional)

### 🔹 Gestão de Equipamentos
- O sistema deve permitir o cadastro, edição e exclusão de equipamentos.
- Cada equipamento deve possuir um status atualizado em tempo real (Disponível, Ocupado, Offline, etc.).
- Deve ser possível consultar o histórico de status de um equipamento.

### 🔹 Reservas de Equipamentos
- Usuários autenticados devem poder criar reservas de equipamentos.
- Cada reserva deve conter informações como horário de início, horário de término e status (Ativa, Concluída, Cancelada).
- O sistema deve evitar reservas concorrentes para o mesmo equipamento.
- Deve ser possível consultar reservas futuras e passadas.

### 🔹 Envio de Comandos para Equipamentos
- O sistema deve permitir o envio de comandos para equipamentos via API.
- Os comandos devem ser transmitidos via MQTT e registrados no sistema.
- Deve ser possível consultar o histórico de comandos enviados para cada equipamento.

### 🔹 Feedback dos Equipamentos
- Os equipamentos devem enviar feedbacks de status via MQTT.
- O sistema deve processar esses feedbacks e atualizar o status do equipamento em tempo real.
- Logs de feedback devem ser armazenados para futuras análises.

### 🔹 Autenticação e Segurança
- O acesso à API deve ser protegido por JWT.
- Cada usuário deve ter permissões específicas para acessar determinadas funcionalidades.
- Deve ser implementada uma camada de auditoria para registrar ações críticas.

---

## 🏗️ Tecnologias e Ferramentas

| Componente               | Tecnologia/Ferramenta |
|--------------------------|----------------------|
| Backend API             | FastAPI |
| Banco de Dados          | PostgreSQL |
| Mensageria MQTT         | Mosquitto |
| Cliente MQTT            | Gmqtt |
| Autenticação            | JWT Authentication |
| Processamento Assíncrono | asyncio / Background Tasks |
| Containers              | Docker / Docker Compose |

---