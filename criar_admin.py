from app import app, db, User

def criar_usuario_admin():
    with app.app_context():
        print("Criando tabelas no banco de dados...")
        db.create_all() 
        admin_existente = User.query.filter_by(username='admin').first()
        
        if not admin_existente:
            novo_admin = User(
                username='admin', 
                password='123' 
            )
            db.session.add(novo_admin)
            db.session.commit()
            print("Sucesso: Usuário 'admin' criado com a senha '123'!")
        else:
            print("Aviso: O usuário 'admin' já existe.")

if __name__ == '__main__':
    criar_usuario_admin()