from flask import Flask, request, jsonify
from models.user import User, Meal
from database import db
from datetime import datetime
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt

#__name__ = __main__
app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3307/flask-crud'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
# view login
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            print(current_user.is_authenticated)

            return jsonify({"message": "Autenticação Realizada com sucesso"})

    return jsonify({"message": "Credenciais Inválidas"}), 400

@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso"})

@app.route('/user', methods=["POST"])
def create_user():

    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuario cadastrado com sucesso"})

    return jsonify({"message": "Dados invalidos"}), 400

@app.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return {"username": user.username}
    
    return jsonify({"message":"Usuario não encontrado"})


@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"message": "Operação não permitida"}), 403
    
    if user and data.get("password"):
        user.password = data.get("password") 
        db.session.commit()
        return jsonify({"message":"Usuario Atualizado"})
    
    return jsonify({"message":"Usuario não encontrado"})

@app.route('/user/<int:id_user>', methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if current_user.role != 'admin':
        return jsonify({"message": "Operação não permitida"}), 403
    if id_user == current_user.id:
        return jsonify({"message": "Deleção não permitida"}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuario {id_user} deletado com sucesso"})


@app.route('/new_meal', methods=['POST'])
@login_required
def add_meal():
    data = request.get_json()
    
    try:
        name = data['name']
        description = data['description']
        date_str = data['date']  
        dentro_da_dieta = data['dentro_da_dieta']

        # Convertendo string para objeto de data
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Criando e associando a refeição ao usuário logado
        new_meal = Meal(
            name=name,
            description=description,
            date=date,
            dentro_da_dieta=dentro_da_dieta,
            user=current_user
        )

        db.session.add(new_meal)
        db.session.commit()

        return jsonify({'message': 'Refeição adicionada com sucesso!'}), 201

    except Exception as e:
        return jsonify({'erro, faltou cadastrar': str(e)}), 400

@app.route('/edit_meal/<int:meal_id>', methods=['PUT'])
@login_required
def edit_meal(meal_id):
    data = request.get_json()

    meal = Meal.query.get(meal_id)
    if not meal:
        return jsonify({'erro': 'Refeição Não Encontrada'}), 404
    
    meal.name = data.get('name', meal.name )
    meal.description = data.get('description', meal.description)
    meal.date = data.get('date', meal.date)  
    meal.dentro_da_dieta = data.get('dentro_da_dieta', meal.dentro_da_dieta)
    
    db.session.commit()

    return jsonify({'message': 'Refeição Atualizada'})


@app.route('/edit_meal/<int:meal_id>', methods=['DELETE'])
@login_required
def delete_meal(meal_id):
    meal = Meal.query.get(meal_id)

    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": f"Refeição {meal_id} deletada com sucesso"})
    

@app.route('/meal/<int:meal_id>', methods=['GET'])
def read_meal(meal_id):
    meal = Meal.query.get(meal_id)

    if meal:
        return {
            "Refeição": meal.name,
            "Descrição": meal.description,
            "Data": meal.date,
            "Usuario": meal.user_id
            }
    
    return jsonify({"message":"Refeição não encontrada"})


@app.route('/meal/<int:id_user>/meals', methods=['GET'])
@login_required
def get_user_meals(id_user):
    if current_user.id != id_user and current_user.role != "admin":
        return jsonify({"message": "Acesso negado"}), 403

    user = User.query.get(id_user)
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    meals = [
        {
            "id": meal.id,
            "name": meal.name,
            "description": meal.description,
            "date": meal.date.strftime('%Y-%m-%d'),
            "dentro_da_dieta": meal.dentro_da_dieta
        }
        for meal in user.meals
    ]

    return jsonify(meals)



if __name__ == "__main__":
    app.run(debug=True)


