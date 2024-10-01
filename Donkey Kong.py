import pyxel
from random import randint


class Tablero:
    def __init__(self):
        
        pyxel.init(210, 240, caption="Donkey Kong", fps=60)
        pyxel.load("Sprites.pyxres")
        
        self.Mario=Mario()#Objeto de clase Mario
        
        self.Platform=Platform()#Objeto de clase Plataforma
    
        self.Pauline=Pauline()#Objeto de clase Pauline
        
        self.Stairs=Stairs()#Objeto de clase Stairs
        
        self.Donkey=DonkeyKong()#Objeto de clase Donkey Kong
        
        self.BarrilList=[]#Lista que almacena pa posicion y hitbox de todos los Barriles
        
        self.timer=100#Variable que determina el numero de frame en el que se empiezan a lanzar barriles
        
        self.Vidas=Vidas()#Objeto de clase Vidas
        
        self.Muerte=False#Representa el estado de Mario, en lo refernte a su vida, si golpea un Barril
        
        self.Ganar=False#Representa el estado de Mario, indicando si ha gando
        
        self.Fin=False#Estado que se usa para reprentar el final de la Partida y desde el cual s puede empezar de nuevo
        
        self.Puntuacion=Puntuacion()#Objeto de clase Puntuacion
        
        pyxel.play(3,4, loop=True)#La cancion que suena de forma constante
        
        pyxel.run(self.Update, self.Draw)#Ejecuta el programa
        
    def Update(self):
        self.Mario.updateMario()#Ejecuta la funcion Update dentro del objeto Mario
        if pyxel.btnp(pyxel.KEY_Q):#Si de pulsa "Q" de finaliza el programa
            pyxel.quit()
            
        """Todos estos procedimientos son expliacdos con detalle en la Memoria"""


        """No caida sobre plataforma:"""
        ##################################################
        if self.hitboxPlat()==True and self.subido==False:
            self.Mario.y-=1
        ##################################################
        
        """Derecha/Izquierda Mario:"""
        ############################################################################################
        if pyxel.btn(pyxel.KEY_LEFT) and (self.subido==False  or self.hitboxStairsBase()==True):
            self.Mario.x-=1
        elif pyxel.btn(pyxel.KEY_RIGHT) and (self.subido==False  or self.hitboxStairsBase()==True):
            self.Mario.x+=1      
        ############################################################################################
        

        """Salto de Mario:"""
        ###############################################################################################################
        if pyxel.btn(pyxel.KEY_SPACE) and self.Mario.Salto==False and self.hitboxPlat()==True and self.subido==False and self.Fin==False:
            self.Mario.Salto=True
            self.Mario.salto-=2
            pyxel.play(0, 3)#Sonido que surge al saltar
        if self.Mario.Salto==True:
         
            if self.Mario.salto <self.Mario.limit:
                self.Mario.y -=1
                self.Mario.salto-=1
            if self.Mario.salto == 0:
                self.Mario.salto=self.Mario.limit
                self.Mario.Salto=False
        elif self.Mario.Salto==False: #Mario cae de forma contante a no ser que este Saltando
            self.Mario.y +=1
        ################################################################################################################
        
        """Subir escalones:"""
        ############################################################
        for i in self.Mario.hitbox_Lateral:
            if i in self.Platform.posPlat2 and self.subido==False:
                self.Mario.y-=1
        ############################################################
        
        """Subir/Bajar escaleras:"""
        ###############################################################################################################################################################
        if (pyxel.btn(pyxel.KEY_UP)or pyxel.btn(pyxel.KEY_DOWN)) and self.hitboxStairs()==True and (self.hitboxStairsBase()==True or self.hitboxStairsFin()==True):
            self.subido=True
        if self.hitboxStairs()==False:
            self.subido=False
        if self.subido==True:
            self.Mario.y-=1
            if pyxel.btn(pyxel.KEY_UP):
                self.Mario.y-=1
            elif pyxel.btn(pyxel.KEY_DOWN) and self.hitboxStairsBase()==False:#225
                self.Mario.y+=1
        ###############################################################################################################################################################
        
        """Barrel Sistem:"""
        ####################################################################
        if len(self.BarrilList)<10 and (pyxel.frame_count==self.timer):
            self.timer+=300
            self.BarrilList.append(Barril())
        
        x=0
        for i in self.BarrilList:
            i.y+=1
            i.hitBarrel()
            if self.TrueBarrilPlat(x)==True:
                i.y-=1
                self.TruePendiente(71,75,-1,x)
                self.TruePendiente(97,109,1,x)
                self.TruePendiente(139,151,-1,x)
                self.TruePendiente(183,195,1,x)
                self.TruePendiente(223,229,-1,x)
            if self.hitPuntuación(x)==True and self.Fin==False:
                self.Puntuacion.timer=60
                self.Puntuacion.cont+=100
                pyxel.play(1,2)
            if self.hitBarril(x)==True:
                self.Muerte=True
                   
                    
                    
            if i.y>250:
                del(self.BarrilList[x])
            if self.TrueBarrilStair(x)==True and randint(0,35)==0:
                i.y+=1
            x+=1
        ####################################################################
        
        """Muerte"""
        #######################
        if self.Muerte==True:
            
            self.Mario.x=0
            self.Mario.y=213
            self.BarrilList=[]
            self.Vidas.cont-=1
            self.Muerte=False
        #######################
        
        """Ganar"""
        ################################
        if self.hitPauline()==True:
            self.Puntuacion.cont+=1000
            self.Ganar=True
            self.Mario.x-=5
        ################################
        
        
        """Fin and Restart"""
        ###################################
        if self.Vidas.cont<=0:
            self.Fin=True
            if pyxel.btn(pyxel.KEY_ENTER):
                    self.Vidas.cont=3
                    self.Puntuacion.cont=0
                    self.Mario.x=0
                    self.Mario.y=213
                    self.BarrilList=[]
                    self.Fin=False
        ###################################

    def Draw(self):
        if self.Fin==False and self.Ganar==False:
            pyxel.cls(0)#Pinta el fondo del Tablero con el color Negro
            pyxel.text(0, 5,str("Puntuacion:"), 7)
            pyxel.text(45, 5,str(self.Puntuacion.cont), 7)#Muestra la puntuacion del jugador
            pyxel.text(0, 15,str("Vidas:"), 7)
            pyxel.text(30, 15,str(self.Vidas.cont), 7)#Muesta la Cantidad de vidas
            self.Stairs.DrawStairs()#Pinta las escaleras en el Tablero
            self.Platform.draw()#Pinta las plataformas en el Tablero
            self.Donkey.draw()#Pinta a Donkey Kong en el Tabalero
            self.Pauline.draw()#Pinta a Pauline en el Tablero
            self.Mario.drawMario()#Pinta a Mario en el Tablero
            for i in self.BarrilList:#Pinta cada uno de los Bariles de la lista en el Tablero
                i.draw()
            if self.Puntuacion.timer !=0:#Dibuja un 100 cerca de Mario cuando este aumenta su puntuación durante 1 segundo
                self.Puntuacion.timer-=1
                pyxel.text(self.Mario.x-7, self.Mario.y-7,str("100"), 7)
        elif self.Fin==True:
            pyxel.cls(0)
            pyxel.text(80, 87,str("GAME OVER"),pyxel.frame_count % 16)
            pyxel.text(75, 110,str("Puntuacion:"), 7)
            pyxel.text(120, 110,str(self.Puntuacion.cont), 7)
            pyxel.text(70, 125,str("ENTER to restart"),6)
            pyxel.text(140, 220,str("Q to exit"),8)
        elif self.Ganar==True:
            pyxel.cls(0)
            pyxel.text(80, 90,str("!!!YOU WIN!!!"),pyxel.frame_count % 16)
            pyxel.text(75, 110,str("Puntuacion:"), 7)
            pyxel.text(120, 110,str(self.Puntuacion.cont), 7)
            pyxel.text(140, 220,str("Q to exit"),8)

    def hitboxPlat(self): #Si Mario y la Plataforma Comparten espacio se activa
        for i in self.Mario.hitbox_Lateral:
            if i in self.Platform.posPlat:
                return True

    def hitboxStairs(self):#Si Mario toca ambos Barrotes de la escalera se activa
        x=False
        y=False
        for i in self.Mario.hitbox_Lateral:
            if i in self.Stairs.hitBarra1 :
                x=True
            if  i in self.Stairs.hitBarra2:
                y=True
        if x==True and y==True:
            return True
        else:
            return False

    def hitboxStairsBase(self):#Si Mario toca la base de las escaleras se activa
        x=False
        for i in self.Mario.hitbox_Lateral:
            if i in self.Stairs.base:
                x=True
        return x
    def hitboxStairsFin(self):#Si mario toca el fin de las escaleras se activa
        x=False
        for i in self.Mario.hitbox_Lateral:
            if i in self.Stairs.hitTop:
                x=True
        return x
    def hitPuntuación(self,num):#Si Mario toca el pixel de puntuación se activa
        for i in self.BarrilList[num].point:
            if i in self.Mario.hitbox_Puntuacion:
                return True
    def hitBarril(self,num):#Si Mario toca un Barril se activa
        for i in self.BarrilList[num].hit:
            if i in self.Mario.hit:
                return True
    def hitPauline(self):#Si mário toca a Pauline se activa
        for i in self.Mario.hit:
            if i in self.Pauline.hit:
                return True

    def TrueBarrilPlat(self,num):#Si un barril determinado de la lista toca una plataforma se activa solo para ese barril
        for i in self.BarrilList[num].base:
            if i in self.Platform.posPlat:
                return True
            
    def TrueBarrilStair(self,num):#Si un barril determinado de la lista toca la parte superior de una escalera se activa solo para ese barril
        for i in self.BarrilList[num].base:
            if i in self.Stairs.hitTop:
                return True

    def TruePendiente(self,y1,y2,direccion,num):#Funcion que determina las zonas del eje Y en el que hay una "corriente" que hace que el barril se mueva a izquierda o derecha si toca una plataforma
        if (self.BarrilList[num].y+10>=y1) and (self.BarrilList[num].y+10)<=y2:
            self.BarrilList[num].x+=direccion

    
class Mario:
    def __init__(self):
        self.x = 0
        self.y=213
        
        self.limit=18#Variable que determina el tope del Salto de Mario
        self.salto=self.limit #Variable que determina la altura del salto actual
        self.Salto=False#Variable que indica si Mario esta saltando

    def updateMario(self):
        self.hitbox_Lateral=[]#Almacena la hitbox que recorre la suela de los pies de Mario
        self.hitbox_Puntuacion=[]#Almecana la hitbox que permitira a mario aumentar su puntuación
        self.hit=[]#Almacena el area que acupa Mario
        
        #Hitbox Lateral
        for x in range(self.x,self.x+12,1):
            self.hitbox_Lateral.append((x,self.y+16))
        #Hit
        for y in range(self.y,self.y+16,1):
            for x in range(self.x,self.x+12,1):
                self.hit.append((x,y))
        #Puntuación
        for y in range(self.y,self.y+16,1):
            self.hitbox_Puntuacion.append((self.x+6,y))
        
        #Limitadores que hacen que Mario no se salga de la pantalla:
        if self.x > 196:
            self.x = 196
        if self.x < -2:
            self.x = -2
    
    def drawMario(self):
        pyxel.blt(self.x,self.y,0,2,1,12,16,3)#Sprite Mario

class Platform:
    def draw(self):
        def Crear(x1,x2,y,pendiente):#Crea conjuntos de escaleras dependiendo de un apendiente, una posicion "y", un inicio que es X1 y el final que es X2
            for x in range(x1,x2,15):
                pyxel.blt(x, y, 0, 236, 103, 15, 8, colkey=3)
                y+=pendiente
        Crear(0,100,230,0)#Primera hilera de plataformas
        
        Crear(105,200,230,-1)#Segunda hilera, rampa ascendente hacia la derecha
        
        Crear(0,181,184,1)#Tercera hilera, rampa descendiente desde la izquierda
        
        Crear(15,196,152,-1)#Cuarta hilera, rampa ascendente haca la derecha
        
        Crear(0,181,98,1)#Quinta hilera, rampa descendente desde la izquierda
        
        Crear(15,61,76,-1)#Sexta hilera, rampa ascendente haca la derecha (Bastante pequeña)
        
        Crear(75,205,72,0)#Septima hilera, donde se ubica Donkey Kong y se generan los Barriles
        
        Crear(75,130,33,0)#Octava hilera, donde de ubica Pauline

    def __init__( self):
        self.posPlat=[]#Lista de hitbox de la primera linea de la platforma que hace que Mario no caiga
        self.posPlat2=[]#Lista de hitbox de la primera linea de la platforma que hace que Mario no caiga
        
        def Crear(x1,x2,y,pendiente):#Funcion cradora de las dos listas
            for x in range(x1,x2,15):
                for i in range(x,x+15,1):
                    self.posPlat.append((i,y))
                    self.posPlat2.append((i,y+1))
                y+=pendiente
        Crear(0,100,230,0)#Primera hilera de plataformas
        
        Crear(105,200,230,-1)#Segunda hilera, rampa ascendente hacia la derecha
        
        Crear(0,184,184,1)#Tercera hilera, rampa descendiente desde la izquierda
        
        Crear(15,196,152,-1)#Cuarta hilera, rampa ascendente haca la derecha
        
        Crear(0,181,98,1)#Quinta hilera, rampa descendente desde la izquierda
        
        Crear(75,205,72,0)#Sexta hilera, rampa ascendente haca la derecha (Bastante pequeña)
        
        Crear(15,61,76,-1)#Septima hilera, donde se ubica Donkey Kong y se generan los Barriles
        
        Crear(75,130,33,0)#Octava hilera, donde de ubica Pauline

class Stairs():
    def __init__(self):
        self.hitBarra1=[]#Lista que acumula la "hitbox" del barrote izquierdo de la escalera
        self.hitBarra2=[]#Lista que acumula la "hitbox" del barrote derecho de la escalera
        self.hitTop=[]#Lista que acumula la hitbox de la parte superior de la escalera
        self.base=[]#Lista que acumula la hitbox de la base desde donde se sube a la escalera

        def CrearBase(X,Y):#Crea el segmento de escaleras desde el que se sube al conjunto
            for y in range(Y,Y+17,1):
                self.hitBarra1.append((X+1,y))
                self.hitBarra2.append((X+8,y))
            for x in range(X+1,X+8,1):
                self.base.append((x,Y+16))

        def CrearMedio(X,Y):#Crea unas escaleras para poner en un segmento medio.
            for y in range(Y,Y+17,1):
                self.hitBarra1.append((X+1,y))
                self.hitBarra2.append((X+8,y))
                
        def CrearFin(X,Y):  #Crear las escaleras que conectan con una plataforma superior
            for y in range(Y-7,Y+17,1):
                self.hitBarra1.append((X+1,y))
                self.hitBarra2.append((X+8,y))
            self.hitTop.append((X+1,Y-7))

            
        CrearBase(167,210)# 1/2 Primeras escaleras en la segunda hilera de plataformas
        CrearFin(167,202)# 2/2
        
        CrearBase(107,175)#Segundas escaleras, rotas, en la tercera hilera de plataformas
        
        CrearBase(32,170)# 1/2 Tercera Escalera, en la tercera hilera de plataformas
        CrearFin(32,158)# 2/2
        
        CrearBase(183,125)# 1/2 Cuarta escalera, en al cuarta hilera de plataformas
        CrearFin(183,117)# 2/2
        
        CrearFin(122,113)#Quinta escalera, rota, en la quinta hilera de plataformas
        
        CrearBase(17,83)# 1/2Sexta escalera, en la quinta hilera de plataformas 
        CrearFin(17,83)# 2/2
        
        CrearBase(80,56)# 1/2 Septima escalera, a la altura de Donkey Kong y que lleva a Pauline
        CrearFin(80,40)# 2/2

    def DrawStairs(self):
        def Crear(X,Y):#Creador del Sprite de Escalera
            pyxel.blt(X, Y, 0, 121, 237, 10, 16, colkey = 3)#Escalera
    
        Crear(167,210)# 1/2 Primeras escaleras en la segunda hilera de plataformas
        Crear(167,202)# 2/2
        
        Crear(107,175)#Segundas escaleras, rotas, en la tercera hilera de plataformas
        
        Crear(32,170)# 1/2 Tercera Escalera, en la tercera hilera de plataformas
        Crear(32,158)# 2/2
        
        Crear(183,125)# 1/2 Cuarta escalera, en al cuarta hilera de plataformas
        Crear(183,117)# 2/2
        
        Crear(122,113)#Quinta escalera, rota, en la quinta hilera de plataformas
        
        Crear(17,83)#Sexta escalera, en la quinta hilera de plataformas 
        
        Crear(80,56)# 1/2 Septima escalera, a la altura de Donkey Kong y que lleva a Pauline
        Crear(80,40)# 2/2
        
        #Escaleras sin hitbox de al lado de Donkey Kong
        for i in range(56,0,-16):
            Crear(135,i)
        for i in range(56,0,-16):
            Crear(155,i)

class DonkeyKong:
    def draw(self):
        pyxel.blt(190,40 ,0, 3, 99, 20, 32, colkey = 3)#Sprite Taco de Barriles
        pyxel.blt(150,39 ,1, 33, 94, 42, 33, colkey = 3)#Sprite Donkey Kong
        
class Pauline:
    def draw(self):
        pyxel.blt(119,10,0,190,228,16,24, colkey = 3)#Sprite Pauline
    def __init__(self):
        self.hit=[]#Lista que almacena pas posiciones del area de Pauline
        for y in range(10,10+24,1):
            for x in range(119,119+16,1):
                self.hit.append((x,y))
class Barril:
    def __init__(self):
        self.x=137
        self.y=61
        
    def hitBarrel(self):
        self.base=[]   #En esta lsita se almacena una serie de posiciones con ejes x,y que definen la "hitbox" del barril.
        self.point=[]  #En esta lista se almacenan las posiciones de los puntos que al ser tocados por Mario aumentarán la puntuación
        self.hit=[]    #En esta liste se almacenan las posiciones del area del Barril
        #Base:
        for i in range(self.x,self.x+13,1):
            self.base.append((i,self.y+10))
        #Point:
        self.point.append((self.x+6,self.y-9))
        self.point.append((self.x+7,self.y-9))
        #Hit:
        for y in range(self.y,self.y+10,1):
            for x in range(self.x,self.x+13,1):
                self.hit.append((x,y))
        
    def draw(self):
        pyxel.blt(self.x,self.y,0,130,117,13,11, colkey = 3)#Sprite Barril
        
class Vidas:
    def __init__(self):
        self.cont=3
        
class Puntuacion:
    def __init__(self):
        self.cont=0
        self.timer=0 #Temporizador para que el pop-up se muestre un determinado tiempo
        
Tablero()