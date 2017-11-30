import random
import tkinter

class Snake(tkinter.Canvas):
    def __init__(self, master=None):

        #Lamada al constructor de su padre
        super().__init__(master)

        #Identifica si se movio de posicion recientemente
        self.movio = False

        #Caracter usado para la cabeza de snake
        self.head_sprite = "☻"

        #Objecto de texto de la cabeza
        self.head = None

        #Posicion de la cabeza
        self.head_pos = 0, 0

        #Letras validas
        self.letras = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r","s","t", "u", "v","w","x", "y", "z")

        #Palabras validas
        self.palabras_validas = ["al", "ol"]

        #Palabra actual
        self.palabra = None

        #Letras por palabra
        self.num_letras = 8

        #Esta snake en movimiento
        self.is_corriendo = False

        #Puntaje basado en cantidad de letras de la palabra
        self.puntaje = 0

        #Vidas actuales
        self.vidas = 3

        #Letras capturadas de la palabra actual (Diccionario de tipo string:Container)
        self.letras_capturadas = []

        #Posicion actual de las letras en la pantalla ( Diccionario de tipo string:Container)
        self.letras_pos = {}


        #Inicializacion de el canvas y creacion de objectos
        self.grid(sticky=tkinter.NSEW)

        #Casilla para la palabra completa
        self.entry_p_completa = tkinter.Entry(self.master, text ="", state = "disabled", justify=tkinter.CENTER)
        self.entry_p_completa.grid(sticky=tkinter.N)

        #Casilla para las vidas
        self.entry_vidas = tkinter.Entry(self.master, text="", state="disabled", justify=tkinter.CENTER)
        self.entry_vidas.grid(sticky=tkinter.N)

        #Casilla para las letras
        self.entry_palabra = tkinter.Entry(self.master, text="", state="disabled", justify=tkinter.CENTER)
        self.entry_palabra.grid(sticky=tkinter.N)

        #Boton de inicia
        self.start_button = tkinter.Button(self.master, text='COMENZAR', command=self.start_bt)
        self.start_button.grid(sticky=tkinter.EW)

        #Funcionamiento de teclas de movimiento
        self.master.bind('w', self.up)
        self.master.bind('a', self.left)
        self.master.bind('s', self.down)
        self.master.bind('d', self.right)

    #Evento al presionar el boton
    def start_bt(self):
        if(self.is_corriendo):
            self.is_corriendo = False
            self.start_button["text"] = "Iniciar"
        else:
            self.delete("all")
            ancho = self.winfo_width()
            altura = self.winfo_height()

            self.create_rectangle(10, 10, ancho - 10, altura - 10)
            self.dir = random.choice('wasd')

            #Inicia a snake en la posicion media y asigna su valor a otra variable
            self.head_pos = [round(ancho // 2, -1), round(altura // 2, -1)]
            self.head = self.create_text(tuple(self.head_pos), text=self.head_sprite)

            #Inicializa las vidas
            self.entry_vidas["state"] = "normal"
            self.entry_vidas.delete(0, tkinter.END)
            self.entry_vidas.insert(0, self.head_sprite + "x" + str(self.vidas))
            self.entry_vidas["state"] = "disabled"

            #Elige una palabra al azar
            self.palabra = random.choice(self.palabras_validas)

            #Asigna palabra ek Etnty de la palabra completa
            self.entry_p_completa["state"] = "normal"
            self.entry_p_completa.delete(0, tkinter.END)
            self.entry_p_completa.insert(0, self.palabra)
            self.entry_p_completa["state"] = "disabled"

            #Asigna espacios vacios al entrey de las letras de la palabra
            self.entry_palabra["state"] = "normal"
            self.entry_palabra.delete(0, tkinter.END)
            self.entry_palabra.insert(0, "_"*len(self.palabra))
            self.entry_palabra["state"] = "disabled"

            #Hace aparecer una nueva secuencia de letras
            self.spawn_letras()

            self.is_corriendo = True
            self.start_button["text"] = "Detener"

            #Representacion de una iteracion del juego
            self.tick()

    #Representa una iteracion del juego
    def tick(self):
        ancho = self.winfo_width()
        altura = self.winfo_height()
       # pos_previa = self.head_pos

        #Movimiento
        if self.dir == 'w':
            self.head_pos[1] -= 10
        elif self.dir == 'a':
            self.head_pos[0] -= 10
        elif self.dir == 's':
            self.head_pos[1] += 10
        elif self.dir == 'd':
            self.head_pos[0] += 10

        self.coords(self.head, self.head_pos)
        self.movio = True

        #Verifica si snake a colisionado con su cola o alguna de las paredes, en cuyo case acaba el juego
        if (self.head_pos[0] < 10 or self.head_pos[0] >= ancho - 10 or
                    self.head_pos[1] < 10 or self.head_pos[1] >= altura - 10
            ):
            self.end()
            return

        #Verifica colicion con una letra y realiza acciones appropiadas
        for letra in self.letras_pos:
            data = self.letras_pos[letra]
            d_p = data.get_pos()
            if self.head_pos[1] == d_p[1] and self.head_pos[0] == d_p[0]:
                #Evalua si se eligio la letra incorrecta
                if letra in self.letras_capturadas or letra not in self.palabra:
                    self.vidas-=1
                    if(self.vidas == 0):
                        self.end()
                        return
                    self.entry_vidas["state"] = "normal"
                    self.entry_vidas.delete(0, tkinter.END)
                    self.entry_vidas.insert(0, self.head_sprite + "x" + str(self.vidas))
                    self.entry_vidas["state"] = "disabled"
                else:
                    #Entrega de puntos y actualizacion del marcador
                    self.puntaje += 10
                    self.letras_capturadas.append(letra)
                    self.update_entry()
                    #Evaluacion por palabra completa y reemplazo en caso lo este + asignacion de bono por palabra completa
                    if self.is_palabra_completa():

                        #Añade una vida y actualiza las entradas
                        self.vidas+=1
                        self.entry_vidas["state"] = "normal"
                        self.entry_vidas.delete(0, tkinter.END)
                        self.entry_vidas.insert(0, self.head_sprite+"x"+str(self.vidas))
                        self.entry_vidas["state"] = "disabled"

                        #Añade el puntaje
                        self.puntaje += (len(self.palabra) * 2)

                        #Elige otra palabra al azar y actualiza las entradas en tkinter
                        ch = random.choice(self.palabras_validas)
                        while (ch == self.palabra):
                            ch = random.choice(self.palabras_validas)

                        self.entry_p_completa["state"] = "normal"
                        self.entry_p_completa.delete(0, tkinter.END)
                        self.entry_p_completa.insert(0, self.palabra)
                        self.entry_p_completa["state"] = "disabled"

                        self.entry_palabra["state"] = "normal"
                        self.entry_palabra.delete(0, tkinter.END)
                        self.entry_palabra.insert(0, "_" * len(self.palabra))
                        self.entry_palabra["state"] = "disabled"

                        #Reinicia las letras capturadas
                        self.letras_capturadas.clear()

                #Reinicia las posiciones
                for l in self.letras_pos:
                    parte = self.letras_pos[l]
                    self.delete(parte.get_id())
                self.letras_pos.clear()
                self.spawn_letras()
                break

        #Temporizador
        if self.is_corriendo:
            self.after(50, self.tick)

    #Identifica si ya se completo la palabra
    def is_palabra_completa(self):
        self.entry_palabra["state"] = "normal"
        for l in self.entry_palabra.get():
            if l == "_":
                self.entry_palabra["state"] = "disabled"
                return False
        self.entry_palabra["state"] = "disabled"
        return True

    #Actualiza la entrada para ver la palabra
    def update_entry(self):
        l_pos = ""
        for l in self.palabra:
            if l in self.letras_capturadas:
                l_pos += l
            else:
                l_pos+="_"
        self.entry_palabra["state"] = "normal"
        self.entry_palabra.delete(0, tkinter.END)
        self.entry_palabra.insert(0, l_pos)
        self.entry_palabra["state"] = "disabled"

    #Hace aparecer x letras en el tablero
    def spawn_letras(self):
        ancho = self.winfo_width()
        altura = self.winfo_height()

        #Letra al azar de la palabra que no se haya añadido todabia
        current_letra = self.sig_letra()
        pos = self.sig_pos(ancho, altura)
        self.letras_pos[current_letra] = Container(pos[0], pos[1], current_letra, self.create_text(pos[0], pos[1], text=current_letra))

        #Elige una letra escogida, crea u contenedor y la añade al canvas
        letras_escogidas = []
        for i in range(0, self.num_letras):
            letra_r = random.choice(self.letras)
            while any(letra_r == self.letras_pos[le].get_name() for le in self.letras_pos) or letra_r in self.letras_capturadas or letra_r in letras_escogidas:
                letra_r = random.choice(self.letras)
            pos = self.sig_pos(ancho, altura)
            letras_escogidas.append(letra_r)
            self.letras_pos[letra_r] = Container(pos[0], pos[1], letra_r, self.create_text(pos[0], pos[1], text = letra_r))

    #Retorna una letra al azar de la palabra que falte
    def sig_letra(self):
        l = random.choice(self.palabra)
        while l in self.letras_capturadas:
            l = random.choice(self.palabra)
        return l

    #Final del juego
    def end(self):
        ancho = self.winfo_width()
        alto = self.winfo_height()

        #Reinicia las variables
        self.palabra = None
        self.letras_capturadas.clear()
        self.letras_pos.clear()
        self.head_pos = 0,0
        #Cambia los botones y muestra el puntaje
        self.corriendo = False
        self.start_button["text"]='Reiniciar'
        self.create_text((round(ancho // 2, -1), round(alto// 2, -1)), text='Fin! Tu Puntaje es: ' + str(self.puntaje))
        self.puntaje = 0

    #Eventos de movimiento que basado en a direccion cambia a donde se mueve
    def up(self, event):
        if self.movio and not self.dir == 's':
            self.dir = 'w'
            self.movio = False
    def down(self, event):
        if self.movio and not self.dir== 'w':
            self.dir = 's'
            self.movio = False
    def left(self, event):
        if self.movio and not self.dir == 'd':
            self.dir = 'a'
            self.movio = False
    def right(self, event):
        if self.movio and not self.dir == 'a':
            self.dir = 'd'
            self.movio = False

    #Nos da la siguiente posicion valida
    def sig_pos(self, ancho, altura):
        invalid_pos = []
        invalid_pos.append(self.head_pos)

        # Añade las posiciones actualmente ocupadas
        for index in self.letras_pos:
            invalid_pos.append(self.letras_pos[index].get_pos())

        #Calcula una posicion al azar dentro de el canvas
        pos = (round(random.randint(20, ancho - 20), -1), round(random.randint(20, altura - 20), -1))
        while pos in invalid_pos:
            pos = (round(random.randint(20, ancho - 20), -1), round(random.randint(20, altura - 20), -1))
        return pos

#Contenedor para una posicion
class Container:
    def __init__(self, x, y, name, id=0):
        self.x = x
        self.y = y
        self.id = id
        self.name = name
    def get_pos(self):
        return self.x, self.y
    def get_name(self):
        return self.name
    def get_id(self):
        return self.id



#Crea la instancia de tk y le da sus tamaños
root = tkinter.Tk()
root.title("Snake")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.resizable(width=False, height=False)
root.minsize(500, 500)
root.maxsize(500, 500)

#Inicia la clase
app = Snake(root)
app.mainloop
