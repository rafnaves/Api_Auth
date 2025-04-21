
# 🍽️ API de Registro de Refeições com Autenticação

Este projeto é uma API REST desenvolvida em **Python (Flask)** para o registro e gerenciamento de refeições, com autenticação de usuários e controle de acesso. As informações são persistidas em um banco de dados **MySQL** rodando via **Docker**.

---

## 🚀 Funcionalidades

- ✅ Registro de usuários com senha criptografada (bcrypt)
- ✅ Autenticação de usuários com Flask-Login
- ✅ Registro de refeições com:
  - Nome
  - Descrição
  - Data
  - Está ou não dentro da dieta
- ✅ Edição de refeições
- ✅ Deleção de refeições
- ✅ Listagem de todas as refeições do usuário
- ✅ Visualização de uma única refeição
- ✅ Controle de acesso com base no usuário autenticado
- ✅ Banco de dados com relacionamento entre `User` e `Meal`

---

## 🧱 Tecnologias Utilizadas

- **Python 3.11**
- **Flask**
- **Flask-Login**
- **SQLAlchemy**
- **MySQL** (em container Docker)
- **Docker + Docker Compose**
- **bcrypt** para criptografia de senhas

---

## 🗃️ Estrutura do Banco de Dados

### Tabelas:

#### `User`
| Campo     | Tipo     |
|-----------|----------|
| id        | Integer (PK) |
| username  | String (único) |
| password  | String (criptografado) |
| role      | String (padrão: `user`) |

#### `Meal`
| Campo            | Tipo       |
|------------------|------------|
| id               | Integer (PK) |
| name             | String     |
| description      | String     |
| date             | Date       |
| dentro_da_dieta  | Boolean    |
| user_id          | Integer (FK -> User.id) |

---

## 🐳 Rodando com Docker

### 1. Suba o container do banco de dados:

```bash
docker-compose up -d
```

### 2. Crie as tabelas no banco:

Acesse o shell Python dentro do seu ambiente virtual:

```bash
python
```

E execute:

```python
from app import app
from database import db

with app.app_context():
    db.create_all()
```

---

## 🔐 Rotas de Autenticação

### `POST /login`

Autentica o usuário.

### `GET /logout`

Realiza logout do usuário autenticado.

---

## 🍴 Rotas de Refeições

- `POST /new_meal` – Cria uma nova refeição.
- `PUT /edit_meal/<int:meal_id>` – Edita uma refeição.
- `DELETE /edit_meal/<int:meal_id>` – Remove uma refeição.
- `GET /user/<int:id_user>/meals` – Lista todas as refeições do usuário.
- `GET /user/<int:id_user>` – Visualiza o nome do usuário.

> ⚠️ A maioria das rotas exige autenticação com login.

---

## 🔐 Segurança

- As senhas dos usuários são criptografadas com **bcrypt** antes de serem salvas no banco.
- O acesso às refeições é restrito ao próprio usuário (a não ser que seja um `admin`).

---

## 📦 Requisitos

- Python 3.11+
- Docker
- Docker Compose
- MySQL client (opcional para debug)

---

## 📝 To Do

- [ ] Adicionar testes automatizados
- [ ] Melhorar mensagens de erro
- [ ] Adicionar paginação nas listagens
- [ ] Documentação da API com Swagger ou Postman

---

## 🧑‍💻 Autor

Projeto desenvolvido por **@rafnaves** 🚀  
```
