# En el conjunto de datos que quiero separar ( en este caso este tipo de rutas ), importo...
from flask import Blueprint, request, jsonify # Blueprint para modularizar y relacionar con app
from flask_bcrypt import Bcrypt                                  # Bcrypt para encriptación
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity   # Jwt para tokens
from models import User ,Product ,CartItem                                        # importar tabla "User" de models
from database import db                                          # importa la db desde database.py
from datetime import timedelta   
import re
                                # importa tiempo especifico para rendimiento de token válido


admin_bp = Blueprint('api/admin', __name__)     # instanciar admin_bp desde clase Blueprint para crear las rutas.

bcrypt = Bcrypt()
jwt = JWTManager()

# RUTA TEST de http://127.0.0.1:5000/admin_bp que muestra "Hola mundo":
@admin_bp.route('/', methods=['GET'])
def show_hello_world():
     return "Hola mundo",200


# RUTA CREAR USUARIO
@admin_bp.route('/register', methods=['POST'])
def create_user():
    try:
        data =  request.get_json()  # Obtenemos los datos del cuerpo de la solicitud JSON
        email = data.get('email')
        password =data.get('password')
        first_name= data.get('first_name')
        last_name = data.get('last_name')
         # Por defecto, is_admin es False si no se proporciona

       
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            return jsonify({'error': 'El correo electrónico no es válido'}), 400
     
        password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(password_regex, password):
            return jsonify({'error': 'La contraseña debe tener mínimo 8 caracteres, una mayúscula, un número y un símbolo'}), 400

        if not email or not password :
            return jsonify({'error': 'Rellena todos los campos'}), 400
        if not first_name or not last_name:
            return jsonify({'error': 'Nombres y apellidos son obligatorios'}), 400
        

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Este e-mail ya se encuentra registrado.'}), 409

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')


        # Ensamblamos el usuario nuevo
        new_user = User(email=email, password=password_hash, first_name=first_name, last_name=last_name)


        db.session.add(new_user)
        db.session.commit()
        
        good_to_share_user = {
            
            'id': new_user.id,
            'email':new_user.email,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
           
           
        }

        return jsonify({'message': 'Usuario creado.','user_created':good_to_share_user}), 201

    except Exception as e:
        return jsonify({'error': 'Error in user creation: ' + str(e)}), 500


#RUTA LOG-IN ( CON TOKEN DE RESPUESTA )
@admin_bp.route('/login', methods=['POST'])
def login():
    try:
        #  Primero chequeamos que por el body venga la info necesaria:
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return jsonify({'error': 'Email y  contraseña son obligatorios.'}), 400
        
        # Buscamos al usuario con ese correo electronico ( si lo encuentra lo guarda ):
        login_user = User.query.filter_by(email=request.json['email']).first()
        if not login_user:
            return jsonify({'error': 'Usuario no encontrado.'}), 404

        # Verificamos que el password sea correcto:
        password_from_db = login_user.password #  Si loguin_user está vacio, da error y se va al "Except".
        true_o_false = bcrypt.check_password_hash(password_from_db, password)
        
        # Si es verdadero generamos un token y lo devuelve en una respuesta JSON:
        if true_o_false:
            expires = timedelta(minutes=30)  # pueden ser "hours", "minutes", "days","seconds"

            user_id = login_user.id       # recuperamos el id del usuario para crear el token...
            access_token = create_access_token(identity=str(login_user.id) , expires_delta=expires)   # creamos el token con tiempo vencimiento
            return jsonify({ 'access_token':access_token,"login_user":{"id":login_user.id,"email":login_user.email,"first_name":login_user.first_name,"last_name":login_user.last_name}}), 200  # Enviamos el token al front ( si es necesario serializamos el "login_user" y tambien lo enviamos en el objeto json )

        else:
            return {"Error":"Contraseña  incorrecta"}
    
    except Exception as e:
        return {"Error":"El email proporcionado no corresponde a ninguno registrado: " + str(e)}, 500
    
# EJEMPLO DE RUTA RESTRINGIDA POR TOKEN. ( LA MISMA RECUPERA TODOS LOS USERS Y LO ENVIA PARA QUIEN ESTÉ LOGUEADO )
    
@admin_bp.route('/users')
@jwt_required()  # Decorador para requerir autenticación con JWT
def show_users():
    current_user_id = get_jwt_identity()  # Obtiene la id del usuario del token
    if current_user_id:
        users = User.query.all()
        user_list = []
        for user in users:
            user_dict = {
                'id': user.id,
                'email': user.email
            }
            user_list.append(user_dict)
        return jsonify(user_list), 200
    else:
        return {"Error": "Token inválido o no proporcionado"}, 401

@admin_bp.route("/post/products", methods=["POST"])
@jwt_required() 
def post_products():
      current_user_id = get_jwt_identity()  
      user = User.query.get(int(current_user_id))
      if not user or not user.is_admin:
          return jsonify({"error": "Acceso denegado. Solo administradores pueden publicar productos."}), 403
      
      data=request.get_json()
      name = data.get('name')
      price = data.get('price')
      description = data.get('description')
      stock = data.get('stock', 0)
      image_url = data.get('image_url')   
       
      if not name or not price :
            return jsonify({"error": "Nombre, precio y descripción son obligatorios."}), 400
      
      new_poduct=Product(
          name=name,
          price=price,
          description=description,
          stock=stock,
          image_url=image_url
      )
      db.session.add(new_poduct)
      db.session.commit()
      
      return jsonify({"message": "Producto publicado exitosamente."}), 201
    

@admin_bp.route("/get/products", methods=["GET"])
def get_products():
    products=Product.query.all()
    product_list = []
    for product in products:
        product_dict = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'stock': product.stock,
            'image_url': product.image_url
        }
        product_list.append(product_dict)

    return jsonify(product_list), 200

@admin_bp.route("/cart/add", methods=["POST"])
@jwt_required()
def add_to_cart():
      current_user_id = get_jwt_identity()  
      user = User.query.get(int(current_user_id))
      if not user:
            return jsonify({"error": "Usuario no encontrado."}), 404
      data= request.get_json()
      product_id = data.get('product_id')
      quantity = data.get('quantity')
      talla = data.get('talla')
      if not product_id or not quantity or not talla:
                return jsonify({"error": "ID del producto, cantidad y talla son obligatorios."}), 400
      product = Product.query.get(product_id)
      if not product:
                return jsonify({"error": "Producto no encontrado."}), 404
      new_cart_item = CartItem(
          user_id=current_user_id,
          product_id=product.id,
          quantity=quantity,
          talla=talla
      )
      db.session.add(new_cart_item)
      db.session.commit()
      return jsonify({"message": "Producto agregado al carrito exitosamente."}), 201

@admin_bp.route("/get/carts", methods=["GET"])
@jwt_required()
def get_cart_items():
    current_user_id = get_jwt_identity()  
    user = User.query.get(int(current_user_id))
    if not user:
        return jsonify({"error": "Debe estar logueado para ver los productos del carrito."}), 404
    
    cart_items= CartItem.query.filter_by(user_id=current_user_id).all()
    if not cart_items:
        return jsonify({"message": "El carrito está vacío."}), 200
    total_price = 0

    cart_items_list = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            subtotal = product.price * item.quantity
            total_price += subtotal

            cart_items_list.append({
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "talla": item.talla,
                "product_name": product.name,
                "product_price": product.price,
                "subtotal": subtotal,
               
            })

    return jsonify(cart_items_list,total_price), 200

@admin_bp.route("/cart/remove/<int:item_id>", methods=["DELETE"])
@jwt_required()
def remove_from_cart(item_id):
    current_user_id = int(get_jwt_identity())  
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404
    cart_item = CartItem.query.get(item_id)
    if not cart_item or cart_item.user_id != current_user_id:
        return jsonify({"error": "Artículo del carrito no encontrado o no pertenece al usuario."}), 404 
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Artículo del carrito eliminado exitosamente."}), 200

