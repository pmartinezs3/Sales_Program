
# Objetivo: Crear un sistema de gestión de productos y ventas

import tkinter as tk 
from tkinter import messagebox 
from tkinter import ttk
from tkinter import scrolledtext 
import re 
import sqlite3 
import os

ruta = os.path.dirname(os.path.abspath(__file__))

# Functionn: Open connection of the database
def OpenConnection():
    connection = sqlite3.connect(f"{ruta}\\local.db")
    return connection

# Función: Create tables in the database
def createTables():
    # Open the connection
    connection = OpenConnection()
    cursor = connection.cursor()
    # Create the tables
    try:
        cursor.execute("""
            CREATE TABLE users(
                id integer primary key AUTOINCREMENT,
                user varchar(20) unique,
                password varchar(50),
                rol varchar(20)
            )
        """)
        cursor.execute("""
            CREATE TABLE product(
                id integer primary key AUTOINCREMENT,
                nombre varchar(30),
                marca varchar(20),
                precioCompra integer,
                precioVenta integer,
                Order integer,
                vendidos integer
            )
        """)
        cursor.execute("""
            CREATE TABLE descuentos(
                id integer primary key AUTOINCREMENT,
                product varchar(30),
                descuento integer
            )
        """)
        cursor.execute("""
            CREATE TABLE Order(
                id integer primary key AUTOINCREMENT,
                product varchar(30),
                Quantity integer,
                mensaje text
            )
        """)
        cursor.execute("""
            CREATE TABLE profit(
                id integer primary key AUTOINCREMENT,
                dia integer,
                mes integer,
                year integer,
                profit integer
            )
        """)
        print("Tables are created")
    except sqlite3.OperationalError:
        print("Tables already exist in the database")
    finally:
        # Close conection
        connection.commit()
        connection.close()

# Function: Insert admin to the database
def insertAdmin():
    connection = OpenConnection()
    cursor = connection.cursor()
    try:
        cursor.execute("insert into user (id, user, password, rol) values(null, 'admin', 'admin123', 'Admin')")
        print("Admin entered correctly")
    except sqlite3.IntegrityError:
        print("Admin already exist")
    finally:
        connection.commit()
        connection.close()

# Function: Search user in database

def SearchUsers(user):
    connection = OpenConnection()
    cursor = connection.cursor()
    cursor.execute("select * from users where user = ?", user)
    user = cursor.fetchone()
    connection.close()
    return user

# Function: Insert user to the database

def insertUser(data):
   
    connection = OpenConnection()
    cursor = connection.cursor()
    try:
        cursor.execute("insert into users(id, user, password, rol) values (null, ?, ?, ?)", data)
        messagebox.showinfo(title="Sucessful register", message="The registry was successful")
    except sqlite3.IntegrityError:
        messagebox.showerror(title="Existing user", message="this user is already in the database")
    finally:
        connection.commit()
        connection.close()

#Class for the login window
class Login:
    def __init__(self):
        createTables()
        insertAdmin()
        self.createWindow()

    def createWindow(self):
        self.window = tk.Tk()
        self.window.title("User Login")
        self.AskData()
        self.createButtons()
        self.window.mainloop()

    def AskData(self):
        self.user = tk.StringVar()
        self.labelUser = tk.Label(self.window, text="User")
        self.labelUser.grid(column=0, row=0, padx=10, pady=10)

        self.cashregisterUser = tk.Entry(self.window, textvariable=self.user)
        self.cashregisterUser.grid(column=1, row=0, padx=10, pady=10)

        self.password = tk.StringVar()
        self.labelPassword = tk.Label(self.window, text="Password")
        self.labelPassword.grid(column=0, row=1, padx=10, pady=10)

        self.cashierPassword = tk.Entry(self.window, textvariable=self.password)
        self.cashierPassword.config(show="*")
        self.cashierPassword.grid(column=1, row=1, padx=10, pady=10)

    def createButtons(self):
        self.RegisterButton = tk.Button(self.window, text="Register", command=self.registrarUsuario)
        self.RegisterButton.grid(column=0, row=2, padx=10, pady=10)

        self.LoginButton = tk.Button(self.window, text="Login", command=self.verificarUsuario)
        self.LoginButton.grid(column=1, row=2, padx=10, pady=10)
    
    #Functions
    
    def verificarUsuario(self):
        self.userDatabase = SearchUsers((self.user.get(),))
        if self.user.get() == "":
            messagebox.showwarning(title="Users", message="Ingrese su User")
        elif self.password.get() == "":
            messagebox.showwarning(title="Password", message="Enter Password")
        elif self.userDatabase == None:
            messagebox.showwarning(title="Error", message="The data entered is not correct")
        elif self.user.get() != self.userDatabase[1] or self.password.get() != self.userDatabase[2]:
            messagebox.showwarning(title="Datos erroneos", message="The data entered is not correct")
            messagebox.showinfo(title="User", message="Correct Data")
            self.window.destroy()
            self.WindowSales = Sales(self.user.get(), self.password.get(), self.userDatabase[3])
    
    def registrarUsuario(self):
        self.window.destroy()
        self.ventanaRegister = Register()

class Register:
    def __init__(self):
        self.createWindow()

    def createWindow(self):
        self.window = tk.Tk()
        self.window.title("Register")
        self.AskData()
        self.createButtons()
        self.window.mainloop()

    def AskData(self):
        self.frameRegister = tk.Frame(self.window)
        self.frameRegister.pack()
        self.frameConfirmar = tk.Frame(self.window)
        self.frameConfirmar.pack()

        self.labelRegister = tk.Label(self.frameRegister, text="Register Data")
        self.labelRegister.grid(column=0, row=0, padx=10, pady=10)

        self.user = tk.StringVar()
        self.labelUser = tk.Label(self.frameRegister, text="User")
        self.labelUser.grid(column=0, row=1, padx=10, pady=10)

        self.cashregisterUser = tk.Entry(self.frameRegister, textvariable=self.user)
        self.cashregisterUser.grid(column=1, row=1, padx=10, pady=10)

        self.password = tk.StringVar()
        self.labelPassword = tk.Label(self.frameRegister, text="Password")
        self.labelPassword.grid(column=0, row=2, padx=10, pady=10)

        self.cashierPassword = tk.Entry(self.frameRegister, textvariable=self.password)
        self.cashierPassword.config(show="*")
        self.cashierPassword.grid(column=1, row=2, padx=10, pady=10)

        self.password2 = tk.StringVar()
        self.labelPassword = tk.Label(self.frameRegister, text="Verify Password")
        self.labelPassword.grid(column=0, row=3, padx=10, pady=10)

        self.cashierPassword = tk.Entry(self.frameRegister, textvariable=self.password2)
        self.cashierPassword.config(show="*")
        self.cashierPassword.grid(column=1, row=3, padx=10, pady=10)

        self.rol = tk.StringVar()
        self.labelRol = tk.Label(self.frameRegister, text="Select a rol")
        self.labelRol.grid(column=0, row=4, padx=10, pady=10)

        self.roles = ("Seller", "Admin")
        self.spinboxRol = tk.Spinbox(self.frameRegister, values=self.roles, textvariable=self.rol)
        self.spinboxRol.grid(column=1, row=4, padx=10, pady=10)

        self.labelAdmin = tk.Label(self.frameConfirmar, text="Data Admin")
        self.labelAdmin.grid(column=0, row=0, padx=10, pady=10)

        self.admin = tk.StringVar()
        self.labelAdmin = tk.Label(self.frameConfirmar, text="Admin user")
        self.labelAdmin.grid(column=0, row=1, padx=10, pady=10)

        self.cashierAdmin = tk.Entry(self.frameConfirmar, textvariable=self.admin)
        self.cashierAdmin.grid(column=1, row=1, padx=10, pady=10)

        self.passwordAdmin = tk.StringVar()
        self.labelPasswordAdmin = tk.Label(self.frameConfirmar, text="Password")
        self.labelPasswordAdmin.grid(column=0, row=2, padx=10, pady=10)

        self.cashierPasswordAdmin = tk.Entry(self.frameConfirmar, textvariable=self.passwordAdmin)
        self.cashierPasswordAdmin.config(show="*")
        self.cashierPasswordAdmin.grid(column=1, row=2, padx=10, pady=10)
        
    def createButtons(self):
        self.RegisterButton= tk.Button(self.frameConfirmar, text="Register", command=self.registrarUsuario)
        self.RegisterButton.grid(column=0, row=3, padx=10, pady=10)

        self.LoginButton = tk.Button(self.frameConfirmar, text="Login", command=self.ingresar)
        self.LoginButton.grid(column=1, row=3, padx=10, pady=10)
    
    #

    def ingresar(self):
        self.window.destroy()
        self.WindowLogin = Login()
    
    def registrarUsuario(self):
        self.data = (self.user.get(), self.password.get(), self.rol.get())
        self.userDatabase = SearchUsers((self.admin.get(),))
        if self.user.get() == "":
            messagebox.showwarning(title="User", message="Ingrese un user")
        elif self.password.get() == "" or self.password2.get() == "":
            messagebox.showwarning(title="Passwords", message="Enter both Passwords")
        elif self.password.get() != self.password2.get():
            messagebox.showerror(title="Error in the Password", message="The Passwords are diferent")
        elif len(self.password.get()) < 8:
            messagebox.showwarning(title="Password length", message="Password must contain at least 8 caracters")
            messagebox.showwarning(title="Password", message="Your Password must have at least 1 number")
        elif re.search('[a-z]', self.password.get()) is None: 
            messagebox.showwarning(title="Password", message="Your Password must have at least one letter")
        elif re.search('[A-Z]', self.password.get()) is None: 
            messagebox.showwarning(title="Password", message="Your Password must have at least one capital letter")
        elif self.admin.get() == "" or self.passwordAdmin.get() == "":
            messagebox.showwarning(title="Admin user", message="The Admin data is necesary to confirm")
        elif self.admin.get() != self.userDatabase[1] or self.passwordAdmin.get() != self.userDatabase[2] or self.userDatabase == None or self.userDatabase[3] != "Admin":
            messagebox.showwarning(title="Admin user", message="Admin data is incorrect")
        else:
            insertUser(self.data)
            self.ingresar()

class Sales:
    def __init__(self, usuario, password, estado):
        self.conexion = (usuario, password, estado)
        self.createWindow()

    def createWindow(self):
        self.window = tk.Tk()
        self.window.title("Local Sales")
        self.crearCuaderno()
        self.crearSalida()
        self.window.mainloop()
    
    def crearCuaderno(self):
        self.secciones = ttk.Notebook(self.window)
        self.seccionListado()
        self.secctionSales()
        if self.conexion[2] == "Admin":
            self.sectionOrder()
            self.seccionRegister()
            self.seccionPendientes()
            self.sectionProfit()
            self.seccionModificaciones()
        self.secciones.grid(column=0, row=0, padx=10, pady=10)
    
    def crearSalida(self):
        self.botonSalir = tk.Button(self.window, text = "Salir", command = self.salida)
        self.botonSalir.grid(column = 0, row = 1, padx = 10, pady = 10)

    def seccionListado(self):
        self.pagina1 = ttk.Frame(self.secciones)
        self.frameProducts = tk.Frame(self.pagina1)
        self.frameBuscar = tk.Frame(self.pagina1)
        self.frameBotones = tk.Frame(self.pagina1)
        self.frameProducts.pack()
        self.frameBuscar.pack()
        self.frameBotones.pack()
        self.secciones.add(self.pagina1, text="Stock of products")
        self.labelFrame1 = ttk.LabelFrame(self.frameProducts, text = "Products")
        self.labelFrame1.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.listaProducts = scrolledtext.ScrolledText(self.frameProducts, width=50, height=30)
        self.listaProducts.grid(column=0, row=1, padx=10, pady=10)

        self.labelNombre = tk.Label(self.frameBuscar, text="Name product:")
        self.labelNombre.grid(row=0, column=0, padx=10, pady=10)
        self.nombreProduct = tk.StringVar()
        self.cuadroNombreProduct = tk.Entry(self.frameBuscar, textvariable=self.nombreProduct)
        self.cuadroNombreProduct.grid(row=0, column=1, padx=10, pady=10)
        self.botonBuscarProduct = tk.Button(self.frameBuscar, text="Search")
        self.botonBuscarProduct.grid(row=0, column=2, padx=10, pady=10)

        self.botonBuscar = tk.Button(self.frameBotones, text="List of products")
        self.botonBuscar.grid(column=0, row=0, padx=10, pady=10)
        self.botonLimpiar = tk.Button(self.frameBotones, text="Clean products")
        self.botonLimpiar.grid(column=1, row=0, padx=10, pady=10)
    
    def secctionSales(self):
        self.productsVendidos = list()
        self.pagina2 = ttk.Frame(self.secciones)

        self.frameSales()
        self.searchProduct()
        self.datosBoleta()

        self.secciones.add(self.pagina2, text="Local Sale")
    
    def frameSales(self):
        self.frameDatos = tk.Frame(self.pagina2)
        self.frameProducts = tk.Frame(self.pagina2)
        self.frameBotoneProducts = tk.Frame(self.pagina2)
        self.frameBoleta = tk.Frame(self.pagina2)
        self.frameBotonesBoleta = tk.Frame(self.pagina2)

        self.frameDatos.pack()
        self.frameProducts.pack()
        self.frameBotoneProducts.pack()
        self.frameBoleta.pack()
        self.frameBotonesBoleta.pack()
    
    def searchProduct(self):
        self.labelNombreProduct = tk.Label(self.frameDatos, text = "Product Name: ")
        self.labelNombreProduct.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.product = tk.StringVar()
        self.cashiersearchproduct = tk.Entry(self.frameDatos, textvariable = self.product)
        self.cashiersearchproduct.grid(column = 1, row = 0, padx = 10, pady = 10)
        self.botonBuscar = tk.Button(self.frameDatos, text="Search")
        self.botonBuscar.grid(column = 2, row = 0, padx = 10, pady = 10)

        self.listProducts = scrolledtext.ScrolledText(self.frameProducts, width=50, height=8)
        self.listProducts.grid(column=0, row=0, padx=10, pady=10)

        self.id = tk.IntVar()
        self.labelId = tk.Label(self.frameBotoneProducts, text = "Product ID")
        self.labelId.grid(column=0, row=0, padx=10, pady=10)
        self.idSeleccionar = tk.Entry(self.frameBotoneProducts, textvariable = self.id)
        self.idSeleccionar.grid(column=1, row=0, padx=10, pady=10)
        self.botonAgregar = tk.Button(self.frameBotoneProducts, text = "Add to the receipt")
        self.botonAgregar.grid(column=2, row=0, padx=10, pady=10)
        self.botonBorrar = tk.Button(self.frameBotoneProducts, text = "Delete from the receipt")
        self.botonBorrar.grid(column=3, row=0, padx=10, pady=10)
    
    def datosBoleta(self):
        self.labelBoleta = tk.Label(self.frameBoleta, text = "Receipt Data")
        self.labelBoleta.grid(column=0, row=0, padx=10, pady=10)
        self.listProducts = scrolledtext.ScrolledText(self.frameBoleta, width=50, height=12)
        self.listProducts.grid(column=0, row=1, padx=10, pady=10)

        self.botonDescartar = tk.Button(self.frameBotonesBoleta, text = "Delete Receipt")
        self.botonDescartar.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.labelMetodoPago = tk.Label(self.frameBotonesBoleta, text = "Select payment method: ")
        self.labelMetodoPago.grid(column = 1, row = 0, padx = 10, pady = 10)
        self.mediosDePago = ("Cash", "Credit card", "Debit Card", "Transfer")
        self.pago = tk.StringVar()
        self.spinboxRol = tk.Spinbox(self.frameBotonesBoleta, values=self.mediosDePago, textvariable = self.pago)
        self.spinboxRol.grid(column = 2, row = 0, padx = 10, pady = 10)
        
        self.labelEfectivo = tk.Label(self.frameBotonesBoleta, text ="Cash: ")
        self.labelEfectivo.grid(column = 0, row = 1, padx = 10, pady = 10)
        self.monto = tk.IntVar()
        self.cashierAmount = tk.Entry(self.frameBotonesBoleta, textvariable = self.monto)
        self.cashierAmount.grid(column = 1, row = 1, padx = 10, pady = 10)
        self.botonPagar = tk.Button(self.frameBotonesBoleta, text = "Pay")
        self.botonPagar.grid(column = 2, row = 1, padx = 10, pady = 10)
    
    def sectionOrder(self):
        self.pagina3 = ttk.Frame(self.secciones)
        
        self.crearFramesOrder()
        self.dataProducts()
        self.QuantityOrderFrame()
        self.OrderSummary()

        self.secciones.add(self.pagina3, text="Provider Order")
    
    def crearFramesOrder(self):
        self.frameDataOrder = tk.Frame(self.pagina3)
        self.frameResumen = tk.Frame(self.pagina3)

        self.frameDataOrder.pack()
        self.frameResumen.pack()

        self.frameDatos = tk.Frame(self.frameDataOrder)
        self.frameOrder = tk.Frame(self.frameDataOrder)

        self.frameDatos.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.frameOrder.grid(row = 0, column = 1, padx = 10, pady = 10)
        
        self.frameOrder = tk.Frame(self.frameOrder)
        self.frameMensaje = tk.Frame(self.frameOrder)
        
        self.frameOrder.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.frameMensaje.grid(row = 1, column = 0, padx = 10, pady = 10)
    
    def dataProducts(self):
        self.labelID = tk.Label(self.frameDatos, text = "ID: ")
        self.labelID.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.id = tk.IntVar()
        self.cashierId = tk.Entry(self.frameDatos, textvariable = self.id)
        self.cashierId.grid(column = 1, row = 0, padx = 10, pady = 10)

        self.labelNombre = tk.Label(self.frameDatos, text = "Name: ")
        self.labelNombre.grid(column = 0, row = 1, padx = 10, pady = 10)
        self.nombre = tk.StringVar()
        self.cashierName = tk.Entry(self.frameDatos, textvariable = self.nombre)
        self.cashierName.grid(column = 1, row = 1, padx = 10, pady = 10)

        self.labelMarca = tk.Label(self.frameDatos, text = "Brand: ")
        self.labelMarca.grid(column = 0, row = 2, padx = 10, pady = 10)
        self.marca = tk.StringVar()
        self.cashierBrand = tk.Entry(self.frameDatos, textvariable = self.marca, state = "readonly")
        self.cashierBrand.grid(column = 1, row = 2, padx = 10, pady = 10)

        self.labelCompra = tk.Label(self.frameDatos, text = "Precio compra: ")
        self.labelCompra.grid(column = 0, row = 3, padx = 10, pady = 10)
        self.precioCompra = tk.StringVar()
        self.cashierBuy = tk.Entry(self.frameDatos, textvariable = self.precioCompra, state = "readonly")
        self.cashierBuy.grid(column = 1, row = 3, padx = 10, pady = 10)

        self.labelVenta = tk.Label(self.frameDatos, text = "Price Sell: ")
        self.labelVenta.grid(column = 0, row = 4, padx = 10, pady = 10)
        self.precioVenta = tk.StringVar()
        self.cashierSell = tk.Entry(self.frameDatos, textvariable = self.precioVenta, state = "readonly")
        self.cashierSell.grid(column = 1, row = 4, padx = 10, pady = 10)

        self.labelOrder = tk.Label(self.frameDatos, text = "Orders: ")
        self.labelOrder.grid(column = 0, row = 5, padx = 10, pady = 10)
        self.Order = tk.IntVar()
        self.cashierOrder = tk.Entry(self.frameDatos, textvariable = self.Order, state = "readonly")
        self.cashierOrder.grid(column = 1, row = 5, padx = 10, pady = 10)

        self.labelVendidos = tk.Label(self.frameDatos, text = "Vendidos: ")
        self.labelVendidos.grid(column = 0, row = 6, padx = 10, pady = 10)
        self.Order = tk.IntVar()
        self.cashierOrder = tk.Entry(self.frameDatos, textvariable = self.Order, state = "readonly")
        self.cashierOrder.grid(column = 1, row = 6, padx = 10, pady = 10)

        self.botonBorrar = tk.Button(self.frameDatos, text = "Clean ")
        self.botonBorrar.grid(column = 0, row = 7, padx = 10, pady = 10)
        self.botonBuscar = tk.Button(self.frameDatos, text = "Search Product")
        self.botonBuscar.grid(column = 1, row = 7, padx = 10, pady = 10)

    def QuantityOrderFrame(self):
        self.labelOrder = tk.Label(self.frameOrder, text = "Quantity to Order: ")
        self.labelOrder.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.QuantityOrder = tk.IntVar()
        self.cashierOrder = tk.Entry(self.frameOrder, textvariable = self.QuantityOrder)
        self.cashierOrder.grid(column = 1, row = 0, padx = 10, pady = 10)

        self.labelMensaje = tk.Label(self.frameMensaje, text = "Mensage:")
        self.labelMensaje.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.scrollMensaje = scrolledtext.ScrolledText(self.frameMensaje, width = 25, height = 10)
        self.scrollMensaje.grid(column = 0, row = 1, padx = 10, pady = 10)
        self.botonAgregar = tk.Button(self.frameMensaje, text = "Add")
        self.botonAgregar.grid(column = 0, row = 2, padx = 10, pady = 10)
    
    def OrderSummary(self):
        self.labelResumen = tk.Label(self.frameResumen, text = "Order Summary")
        self.labelResumen.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.scrollResumen = scrolledtext.ScrolledText(self.frameResumen, width = 50, height = 10)
        self.scrollResumen.grid(column = 0, row = 1, padx = 10, pady = 10)
        self.botonOrder = tk.Button(self.frameResumen, text = "Make Order")
        self.botonOrder.grid(column = 0, row = 2, padx = 10, pady = 10)
    
    def seccionRegister(self):
        self.pagina4 = tk.Frame(self.secciones)

        self.crearFramesRegister()
        self.AskUserData()
        self.AskDataAdmin()        

        self.secciones.add(self.pagina4, tex ="Registry of users")

    def crearFramesRegister(self):
        self.frameRegistrados = tk.Frame(self.pagina4)
        self.frameModificar = tk.Frame(self.pagina4)
        self.frameRegistrar = tk.Frame(self.pagina4)

        self.frameRegistrados.pack()
        self.frameModificar.pack()
        self.frameRegistrar.pack()
    
    def AskUserData(self):
        self.labelRegisters = tk.Label(self.frameRegistrados, text = "Users register in the database")
        self.labelRegisters.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.scrollResumen = scrolledtext.ScrolledText(self.frameRegistrados, width = 60, height = 10)
        self.scrollResumen.grid(column = 0, row = 1, padx = 10, pady = 10)

        self.labelModificaciones = tk.Label(self.frameModificar, text = "Datos para modificar")
        self.labelModificaciones.grid(column = 0, row = 0, padx = 10, pady = 10)

        self.labelId = tk.Label(self.frameModificar, text = "Id:")
        self.labelId.grid(column = 0, row = 1, padx = 10, pady = 10)
        self.id = tk.IntVar()
        self.cuadroId = tk.Entry(self.frameModificar, textvariable = self.id)
        self.cuadroId.grid(column = 1, row = 1, padx = 10, pady = 10)

        self.labelNombre = tk.Label(self.frameModificar, text = "User:")
        self.labelNombre.grid(column = 2, row = 1, padx = 10, pady = 10)
        self.nombre = tk.StringVar()
        self.cuadroNombre = tk.Entry(self.frameModificar, textvariable = self.nombre)
        self.cuadroNombre.grid(column = 3, row = 1, padx = 10, pady = 10)

        self.labelRol = tk.Label(self.frameModificar, text = "Rol:")
        self.labelRol.grid(column = 0, row = 2, padx = 10, pady = 10)
        self.roles = ("Seller", "Admin")
        self.rol = tk.StringVar()
        self.spinboxRol = tk.Spinbox(self.frameModificar, values=self.roles, textvariable=self.rol)
        self.spinboxRol.grid(column = 1, row = 2, padx = 10, pady = 10)

        self.labelPassword = tk.Label(self.frameModificar, text = "Password:")
        self.labelPassword.grid(column = 2, row = 2, padx = 10, pady = 10)
        self.password = tk.StringVar()
        self.cuadroPassword = tk.Entry(self.frameModificar, textvariable = self.password)
        self.cuadroPassword.grid(column = 3, row = 2, padx = 10, pady = 10)
    
    def AskDataAdmin(self):
        self.labelRegister = tk.Label(self.frameRegistrar, text="Register Data")
        self.labelRegister.grid(column=0, row=0, padx=10, pady=10)

        self.user = tk.StringVar()
        self.labelUser = tk.Label(self.frameRegistrar, text="User")
        self.labelUser.grid(column=0, row=1, padx=10, pady=10)

        self.cashregisterUser = tk.Entry(self.frameRegistrar, textvariable=self.user)
        self.cashregisterUser.grid(column=1, row=1, padx=10, pady=10)

        self.password = tk.StringVar()
        self.labelPassword = tk.Label(self.frameRegistrar, text="Password")
        self.labelPassword.grid(column=0, row=2, padx=10, pady=10)

        self.cashierPassword = tk.Entry(self.frameRegistrar, textvariable=self.password)
        self.cashierPassword.config(show="*")
        self.cashierPassword.grid(column=1, row=2, padx=10, pady=10)

        self.password2 = tk.StringVar()
        self.labelPassword = tk.Label(self.frameRegistrar, text="Verify Password")
        self.labelPassword.grid(column=0, row=3, padx=10, pady=10)

        self.cashierPassword = tk.Entry(self.frameRegistrar, textvariable=self.password2)
        self.cashierPassword.config(show="*")
        self.cashierPassword.grid(column=1, row=3, padx=10, pady=10)

        self.rol = tk.StringVar()
        self.labelRol = tk.Label(self.frameRegistrar, text="Select a rol")
        self.labelRol.grid(column=0, row=4, padx=10, pady=10)

        self.roles = ("Seller", "Admin")
        self.spinboxRol = tk.Spinbox(self.frameRegistrar, values=self.roles, textvariable=self.rol)
        self.spinboxRol.grid(column=1, row=4, padx=10, pady=10)

        # Admin data
        self.labelAdmin = tk.Label(self.frameRegistrar, text="Data Admin")
        self.labelAdmin.grid(column=2, row=0, padx=10, pady=10)

        self.admin = tk.StringVar()
        self.labelAdmin = tk.Label(self.frameRegistrar, text="Admin")
        self.labelAdmin.grid(column=2, row=1, padx=10, pady=10)

        self.cashierAdmin = tk.Entry(self.frameRegistrar, textvariable=self.admin)
        self.cashierAdmin.grid(column=3, row=1, padx=10, pady=10)

        self.passwordAdmin = tk.StringVar()
        self.labelPasswordAdmin = tk.Label(self.frameRegistrar, text="Password")
        self.labelPasswordAdmin.grid(column=2, row=2, padx=10, pady=10)

        self.cashierPasswordAdmin = tk.Entry(self.frameRegistrar, textvariable=self.passwordAdmin)
        self.cashierPasswordAdmin.config(show="*")
        self.cashierPasswordAdmin.grid(column=3, row=2, padx=10, pady=10)

        self.opcion = tk.StringVar()
        self.opcionRM = ("Register", "Modify", "Delete")
        self.spinboxRol = tk.Spinbox(self.frameRegistrar, values=self.opcionRM, textvariable=self.opcion)
        self.spinboxRol.grid(column=2, row=3, padx=10, pady=10)

        self.botonConfirmar = tk.Button(self.frameRegistrar, text = "Confirmar")
        self.botonConfirmar.grid(column = 3, row = 3, padx = 10, pady = 10)
    
    def seccionPendientes(self):
        self.pagina5 = ttk.Frame(self.secciones)

        self.crearFramesPendientes()
        self.listaDePendientes()
        self.accionesPendientes()

        self.secciones.add(self.pagina5, tex ="Pending Orders")
    
    def crearFramesPendientes(self):
        self.frameListaPendientes = tk.Frame(self.pagina5)
        self.frameAccionesPendientes = tk.Frame(self.pagina5)

        self.frameListaPendientes.pack()
        self.frameAccionesPendientes.pack()

    def listaDePendientes(self):
        self.scrollResumen = scrolledtext.ScrolledText(self.frameListaPendientes, width = 60, height = 30)
        self.scrollResumen.grid(column = 0, row = 0, padx = 10, pady = 10)

        self.botonObtener = tk.Button(self.frameListaPendientes, text = "Obtain list of pending orders")
        self.botonObtener.grid(column = 0, row = 1, padx = 10, pady = 10)

    def accionesPendientes(self):
        self.labelId = tk.Label(self.frameAccionesPendientes, text = "Product Id:")
        self.labelId.grid(column = 0, row = 0, padx = 10, pady = 10)

        self.id = tk.IntVar()
        self.cashierId = tk.Entry(self.frameAccionesPendientes, textvariable = self.id)
        self.cashierId.grid(column = 1, row = 0, padx = 10, pady = 10)

        self.botonRealizado = tk.Button(self.frameAccionesPendientes, text = "Mark as received")
        self.botonRealizado.grid(column = 2, row = 0, padx = 10, pady = 10)

        self.botonCancelar = tk.Button(self.frameAccionesPendientes, text = "Delete order")
        self.botonCancelar.grid(column = 3, row = 0, padx = 10, pady = 10)
    
    def sectionProfit(self):
        self.pagina6 = ttk.Frame(self.secciones)

        self.crearFramesProfit()
        self.listaProfit()
        self.botonesProfit()
        self.filtarFecha()

        self.secciones.add(self.pagina6, tex ="Profit")

    def crearFramesProfit(self):
        self.frameProfit = tk.Frame(self.pagina6)
        self.frameBotonesProfit(self.pagina6)
        self.frameFilterProfit = tk.Frame(self.pagina6)

        self.frameProfit.pack()
        self.frameBotonesProfit.pack()
        self.frameFilterProfit.pack()

    def listaProfit(self):
        self.scrollResumen = scrolledtext.ScrolledText(self.frameProfit, width = 60, height = 25)
        self.scrollResumen.grid(column = 0, row = 0, padx = 10, pady = 10)

    def botonesProfit(self):
        self.botonObtener = tk.Button(self.frameBotonesProfit, text = "Obtain list daily Profit")
        self.botonObtener.grid(column = 0, row = 0, padx = 10, pady = 10)
        
        self.botonLimpiar = tk.Button(self.frameBotonesProfit, text = "Clean List")
        self.botonLimpiar.grid(column = 1, row = 0, padx = 10, pady = 10)
    
    def filtarFecha(self):
        self.labelFecha = tk.Label(self.frameFilterProfit, text = "Search Date")
        self.labelFecha.grid(column = 0, row = 0, padx = 10, pady = 10)

        self.fechaBuscada = tk.StringVar()
        self.cuadroFecha = tk.Entry(self.frameFilterProfit, textvariable = self.fechaBuscada)
        self.cuadroFecha.grid(column = 1, row = 0, padx = 10, pady = 10)

        self.botonFiltrar = tk.Button(self.frameFilterProfit, text = "Buscar")
        self.botonFiltrar.grid(column = 2, row = 0, padx = 10, pady = 10)

        self.labelMes = tk.Label(self.frameFilterProfit, text = "Mes a buscar")
        self.labelMes.grid(column = 0, row = 1, padx = 10, pady = 10)

        self.mesBuscado = tk.StringVar()
        self.cuadroMes = tk.Entry(self.frameFilterProfit, textvariable = self.mesBuscado)
        self.cuadroMes.grid(column = 1, row = 1, padx = 10, pady = 10)

        self.botonMes = tk.Button(self.frameFilterProfit, text = "Search")
        self.botonMes.grid(column = 2, row = 1, padx = 10, pady = 10)
    
    def seccionModificaciones(self):
        self.pagina7 = ttk.Frame(self.secciones)

        self.crearFramesModificaciones()
        self.dataProducts()
        self.dataAdmin()

        self.secciones.add(self.pagina7, tex ="Modifications")

    def crearFramesModificaciones(self):
        self.frameDataProduct = tk.Frame(self.pagina7)
        self.frameDataConfirmation = tk.Frame(self.pagina7)

        self.frameDataProduct.pack()
        self.frameDataConfirmation.pack()
    
    def dataProduct(self):
        self.labelId = tk.Label(self.frameDataProduct, text = "Id:")
        self.labelId.grid(column = 0, row = 0, padx = 10, pady = 10)

        self.idModificar = tk.IntVar()
        self.cuadroId = tk.Entry(self.frameDataProduct, textvariable = self.idModificar)
        self.cuadroId.grid(column = 1, row = 0, padx = 10, pady = 10)

        self.labelNombre = tk.Label(self.frameDataProduct, text = "Name:")
        self.labelNombre.grid(column = 0, row = 1, padx = 10, pady = 10)

        self.nombreModificar = tk.StringVar()
        self.cuadroNombre = tk.Entry(self.frameDataProduct, textvariable = self.nombreModificar)
        self.cuadroNombre.grid(column = 1, row = 1, padx = 10, pady = 10)

        self.labelMarca = tk.Label(self.frameDataProduct, text = "Brand:")
        self.labelMarca.grid(column = 0, row = 2, padx = 10, pady = 10)

        self.marcaModificar = tk.StringVar()
        self.cuadroMarca = tk.Entry(self.frameDataProduct, textvariable = self.marcaModificar)
        self.cuadroMarca.grid(column = 1, row = 2, padx = 10, pady = 10)

        self.labelCompra = tk.Label(self.frameDataProduct, text = "Price:")
        self.labelCompra.grid(column = 0, row = 3, padx = 10, pady = 10)

        self.compraModificar = tk.IntVar()
        self.cuadroCompra = tk.Entry(self.frameDataProduct, textvariable = self.compraModificar)
        self.cuadroCompra.grid(column = 1, row = 3, padx = 10, pady = 10)

        self.labelVenta = tk.Label(self.frameDataProduct, text = "Total Price:")
        self.labelVenta.grid(column = 0, row = 4, padx = 10, pady = 10)

        self.ventaModificar = tk.IntVar()
        self.cuadroVenta = tk.Entry(self.frameDataProduct, textvariable = self.ventaModificar)
        self.cuadroVenta.grid(column = 1, row = 4, padx = 10, pady = 10)

        self.labelDescuento = tk.Label(self.frameDataProduct, text = "Discount:")
        self.labelDescuento.grid(column = 0, row = 5, padx = 10, pady = 10)

        self.descuentoModificar = tk.IntVar()
        self.cuadroDescuento = tk.Entry(self.frameDataProduct, textvariable = self.descuentoModificar)
        self.cuadroDescuento.grid(column = 1, row = 5, padx = 10, pady = 10)

        self.botonLimpiar = tk.Button(self.frameDataProduct, text = "Clean Data")
        self.botonLimpiar.grid(column = 0, row = 6, padx = 10, pady = 10)

        self.botonBuscar = tk.Button(self.frameDataProduct, text = "Search product")
        self.botonBuscar.grid(column = 1, row = 6, padx = 10, pady = 10)
    
    def dataAdmin(self):
        self.labelAdmin = tk.Label(self.frameDataConfirmation, text = "Admin:")
        self.labelAdmin.grid(column = 0, row = 0, padx = 10, pady = 10)

        self.Admin = tk.StringVar()
        self.cashierAdmin = tk.Entry(self.frameDataConfirmation, textvariable = self.Admin)
        self.cashierAdmin.grid(column = 1, row = 0, padx = 10, pady = 10)

        self.labelPassword = tk.Label(self.frameDataConfirmation, text = "Password:")
        self.labelPassword.grid(column = 0, row = 1, padx = 10, pady = 10)

        self.password = tk.StringVar()
        self.cashierPassword = tk.Entry(self.frameDataConfirmation, textvariable = self.password)
        self.cashierPassword.config(show = "*")
        self.cashierPassword.grid(column = 1, row = 1, padx = 10, pady = 10)

        self.botonConfirmarCambios = tk.Button(self.frameDataConfirmation, text = "Confirm Changes")
        self.botonConfirmarCambios.grid(column = 1, row = 2, padx = 10, pady = 10)

    #
    
    def salida(self):
        resp = messagebox.askyesno(title = "Are you sure you want to Exit?", message = "Are you sure?")
        if resp:
            self.window.destroy()
        

########################
### Bloque principal ###
########################

objVentana = Login()