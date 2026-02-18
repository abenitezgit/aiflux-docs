import os
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select
from app.models import UsuarioDB, Categoria, Cuaderno, Tema, Anotacion

load_dotenv()

SOURCE_URL = os.getenv("DATABASE_URL_SUPABASE").replace("postgres://", "postgresql://", 1)
DEST_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)

dest_engine = create_engine(DEST_URL)

def clean_uuid(val):
    if val is None: return None
    s_val = str(val).strip()
    if not s_val or s_val == "" or s_val == "None": return None
    try:
        return uuid.UUID(s_val)
    except Exception:
        return None

def run_smart_migration():
    # user_mapping almacenará { id_supabase: id_vps }
    user_mapping = {} 

    print("🔌 Conectando al origen (Supabase)...")
    try:
        src_conn = psycopg2.connect(SOURCE_URL)
        src_cur = src_conn.cursor(cursor_factory=RealDictCursor)
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    try:
        with Session(dest_engine) as dest_session:
            print("\n🔍 Paso 1: Mapeando identidades de usuario...")
            # Los usuarios usualmente se pueden leer porque son la base de la autenticación
            src_cur.execute("SELECT * FROM usuarios")
            src_users = src_cur.fetchall()
            
            for s_user in src_users:
                old_id = clean_uuid(s_user['id'])
                stmt = select(UsuarioDB).where(UsuarioDB.email == s_user['email'])
                d_user = dest_session.exec(stmt).first()

                if d_user:
                    user_mapping[old_id] = d_user.id
                    print(f"   - Usuario: {s_user['email']} ({old_id} -> {d_user.id})")
                else:
                    print(f"   - Nuevo usuario: {s_user['email']}. Migrando cuenta...")
                    new_user = UsuarioDB(
                        id=old_id, email=s_user['email'], 
                        hashed_password=s_user['hashed_password'], 
                        nombre=s_user['nombre'], created_at=s_user['created_at']
                    )
                    dest_session.add(new_user)
                    user_mapping[old_id] = old_id
            
            dest_session.commit()

            # PLAN DE MIGRACIÓN POR USUARIO (Para bypass de RLS)
            migration_plan = [
                (Categoria, "categorias", "Categorías"),
                (Cuaderno, "cuadernos", "Cuadernos"),
                (Tema, "temas", "Temas"),
                (Anotacion, "anotaciones", "Anotaciones")
            ]

            for model_class, table_name, label in migration_plan:
                print(f"\n📦 Migrando {label}...")
                migrated_count = 0
                already_exists_count = 0
                
                # AXIOMA: Iteramos por cada usuario mapeado para "engañar" al RLS
                for old_uid, new_uid in user_mapping.items():
                    try:
                        # 1. Configuramos la sesión de Postgres con el ID del usuario de Supabase
                        src_cur.execute(f"SET app.current_user_id = '{old_uid}';")
                        
                        # 2. Pedimos los datos de ese usuario específicamente
                        src_cur.execute(f"SELECT * FROM {table_name} WHERE user_id = %s", (str(old_uid),))
                        rows = src_cur.fetchall()
                        
                        if not rows:
                            continue

                        for row in rows:
                            data = dict(row)
                            curr_id = clean_uuid(data.get('id'))
                            
                            if not curr_id: continue

                            # 3. Verificar si el registro ya existe en el VPS
                            if dest_session.get(model_class, curr_id):
                                already_exists_count += 1
                                continue

                            # 4. Re-mapear identidades
                            data['id'] = curr_id
                            data['user_id'] = new_uid # El ID del VPS
                            
                            if 'categoria_id' in data: data['categoria_id'] = clean_uuid(data['categoria_id'])
                            if 'cuaderno_id' in data: data['cuaderno_id'] = clean_uuid(data['cuaderno_id'])
                            if 'tema_id' in data: data['tema_id'] = clean_uuid(data['tema_id'])

                            # Limpiar Tags
                            if 'tags' in data:
                                t = data['tags']
                                if t is None: data['tags'] = []
                                elif isinstance(t, str): data['tags'] = t.strip('{}').split(',') if t.strip('{}') else []

                            # Insertar
                            try:
                                new_item = model_class(**data)
                                dest_session.add(new_item)
                                migrated_count += 1
                            except Exception as e:
                                dest_session.rollback()
                                print(f"      ⚠️ Error en registro {curr_id}: {e}")

                        dest_session.commit()
                        
                    except Exception as e:
                        print(f"   ⚠️ Error leyendo {label} para usuario {old_uid}: {e}")
                        src_conn.rollback()

                print(f"   ✅ {migrated_count} migrados.")
                if already_exists_count > 0:
                    print(f"   ℹ️  {already_exists_count} ya existían en destino.")

    except Exception as e:
        print(f"❌ Error crítico: {e}")
    finally:
        src_cur.close()
        src_conn.close()
        print("\n🚀 Proceso finalizado.")

if __name__ == "__main__":
    run_smart_migration()