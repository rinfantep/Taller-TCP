from flask import Flask
from flask import render_template,request,redirect,url_for,flash
from flaskext.mysql import MySQL
from datetime import datetime
from flask_wtf import CSRFProtect
import os
from config import config
from flask import session


app=Flask(__name__)
app.secret_key="my_password"
csrf=CSRFProtect(app)

mysql=MySQL(app)
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='tcp'
mysql.init_app(app)

@app.route('/')
def index():
    
    sql="SELECT * FROM `cliente`;"
    
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    
    
    cliente=cursor.fetchall()
    print(cliente)
    
    conn.commit()
    
    return render_template('clientes/index.html',cliente=cliente)
    

@app.route('/iniciar_seccion',methods=['GET','POST'])
def iniciar_seccion():
    
    if request.method=='POST':
        usuario=request.form['txtUsuario']
        contrasenia=request.form['txtContrasenia']
        
        if usuario=='' or contrasenia=='':
            flash('Debes llenar los datos de los campos correctamente')
            return redirect(url_for('iniciar_seccion'))
            
        
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("SELECT usuario,contrasenia FROM registro WHERE usuario=%s",(usuario))
        
        user=cursor.fetchone()
        cursor.close()
        
        if len(user)>0:
            if contrasenia==user[1]:
                
                sql="SELECT * FROM `cliente`;"
    
                conn=mysql.connect()
                cursor=conn.cursor()
                cursor.execute(sql)
                
                
                cliente=cursor.fetchall()
                print(cliente)
                
                conn.commit()
                
                return render_template('clientes/index.html',cliente=cliente)
                
               
                
            else: 
                flash('Correo o contraseña invalido')
                return redirect(url_for('iniciar_seccion'))
        else:
            flash('No existe el usuario')
            return redirect(url_for('iniciar_seccion'))
    else:
        return render_template('iniciar_seccion.html')



@app.route("/registro_usu",methods=['GET','POST'])
def registro_usu():
    
   
    
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM registro")
    
    registro=cursor.fetchall()
    cursor.close()
    
    if request.method=='GET':
        return render_template('registro_usu.html',registro=registro)
    
    else:
        _usuario=request.form['txtUsuario']
        _nombre=request.form['txtNombre']
        _apellido=request.form['txtApellido']
        _contrasenia=request.form['txtContrasenia']
        
        
        if _usuario=='' or _nombre=='' or _apellido=='' or _contrasenia=='':
            flash('Debes llenar los datos de los campos')
            return redirect(url_for('registro_usu'))
        
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("INSERT INTO `registro` (`usuario`,`nombre`,`apellido`,`contrasenia`) VALUES (%s,%s,%s,%s)",(_usuario,_nombre,_apellido,_contrasenia))
    
    conn.commit()
    
    return redirect(url_for('iniciar_seccion'))


@app.route("/cerrar_seccion")
def cerrar_seccion():
   
    return redirect('iniciar_seccion')


@app.route('/destroy/<int:id>')
def destroy(id):
    
    conn=mysql.connect()
    cursor=conn.cursor()
    
    cursor.execute("DELETE FROM cliente WHERE id_cliente=%s",(id))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM cliente WHERE id_cliente=%s",(id))
    
    cliente=cursor.fetchall()
    conn.commit()
    print(cliente)    
    
    return render_template('clientes/edit.html',cliente=cliente)

@app.route('/update', methods=['POST'])
def update():
    
    _nombre=request.form['txtNombre']
    _ci=request.form['txtCI']
    _telefono=request.form['txtTelefono']
    id=request.form['txtID']
    
    sql="UPDATE cliente SET nombre=%s, ci=%s, telefono=%s WHERE id_cliente=%s;"
    
    datos=(_nombre,_ci,_telefono,id)
    
    conn=mysql.connect()
    cursor=conn.cursor()
    
    cursor.execute(sql,datos)
    conn.commit()
    
    return redirect('/')

@app.route('/create')
def create():
    return render_template('clientes/create.html')

@app.route('/store', methods=['POST'])
def storage():
    
    _nombre=request.form['txtNombre']
    _ci=request.form['txtCI']
    _telefono=request.form['txtTelefono']
    
    if _nombre=='' or _ci=='' or _telefono=='':
        flash('Debes llenar los datos de los campos')
        return redirect(url_for('create'))
    
    sql="INSERT INTO `cliente` (`id_cliente`, `nombre`, `ci`, `telefono`) VALUES (NULL, %s, %s, %s);"
    
    datos=(_nombre,_ci,_telefono)
    
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    
    return redirect('/')

#Equipos

@app.route('/create_equipos')
def create_equipos():
    return render_template('equipos/create_equipos.html')

@app.route('/store_equipos', methods=['POST'])
def storage_equipos():
    
    _nOrden=request.form['txtOrden']
    _imei=request.form['txtImei']
    _marca=request.form['txtMarca']
    _modelo=request.form['txtModelo']
    _tipo=request.form['txtTipo']
    _defectado=request.form['txtDefectado']
    
    if _nOrden=='' or _imei=='' or _marca=='' or _modelo=='' or _defectado=='':
        flash('Debes llenar los datos de los campos')
        return redirect(url_for('create_equipos'))
    
    sql="INSERT INTO `equipo` (`id_equipo`,`cliente_id_cliente`, `imei`, `marca`, `modelo`, `tipo`,`defectado`) VALUES (NULL,%s,%s,%s,%s,%s,%s);"
    
    datos=(_nOrden,_imei,_marca,_modelo,_tipo,_defectado)
    
    
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    
    return redirect('/')

@app.route('/equipos')
def equipos():
    
    
    sql="SELECT * FROM `equipo`;"
    
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    
    
    equipos=cursor.fetchall()
    print(equipos)
    
    conn.commit()
    
    return render_template('equipos/equipos.html',equipos=equipos)

@app.route('/buscar_equipos')
def buscar_equipos():
    
    sql="SELECT id_equipo,cliente_id_cliente,imei,marca,modelo,tipo,defectado FROM `equipo` ,`cliente`WHERE cliente_id_cliente=id_cliente;"
    
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    
    
    buscar_equipos=cursor.fetchall()
    print(buscar_equipos)
    
    conn.commit()
    return render_template('equipos/buscar_equipos.html',buscar_equipos=buscar_equipos)

@app.route('/destroy_equipo/<int:id>')
def destroy_equipo(id):
    
    conn=mysql.connect()
    cursor=conn.cursor()
    
    cursor.execute("DELETE FROM equipo WHERE id_equipo=%s",(id))
    
    sql="SELECT * FROM `equipo`;"
    cursor.execute(sql)
    equipos=cursor.fetchall()
    print(equipos)
    
    conn.commit()
    return render_template('equipos/equipos.html',equipos=equipos)

@app.route('/edit_equipos/<int:id>')
def edit_equipos(id):
    
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM equipo WHERE id_equipo=%s",(id))
    
    equipos=cursor.fetchall()
    conn.commit()
    print(equipos)    
    
    return render_template('equipos/edit_equipos.html',equipos=equipos)

@app.route('/update_equipos', methods=['POST'])
def update_equipos():
    
    _nOrden=request.form['txtOrden']
    _imei=request.form['txtImei']
    _marca=request.form['txtMarca']
    _modelo=request.form['txtModelo']
    _defectado=request.form['txtDefectado']
    id=request.form['txtID']
    
    sql="UPDATE equipo SET cliente_id_cliente=%s, imei=%s, marca=%s,modelo=%s,defectado=%s WHERE id_equipo=%s;"
    
    datos=(_nOrden,_imei,_marca,_modelo,_defectado,id)
    
    conn=mysql.connect()
    cursor=conn.cursor()
    
    cursor.execute(sql,datos)
    conn.commit()
    
    return redirect('/')

if __name__=='__main__':
    app.config.from_object(config['development'])
    app.run()