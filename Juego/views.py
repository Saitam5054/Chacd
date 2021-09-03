from django.db import reset_queries
from django.http import request
from django.shortcuts import redirect, render
from Juego import models

# Create your views here.

categorias = ["HISTORIA", "DEPORTE", "GEOGRAFÍA", "ECONOMÍA", "CIENCIA Y EDUCACIÓN", "ENTRETENIMIENTO"]
contador_preguntas = 0
contador_correctas = 0
categoria = ''
pregunta = []
cantidad_preguntas = {}
id_usadas = []
preguntas_acertadas = 0
url = '127.0.0.1:8000'
tipoopcion = True


def JuegoPregunta(request):
    global categoria
    global contador_preguntas
    global contador_correctas
    global pregunta
    global id_usadas
    global preguntas_acertadas
    global tipoopcion 

    if request.user.username: #condicional para que solo juegue si esta logueado
        if request.method == 'POST':  #condicional para que solo se juegue si entra por el metodo post

            if 'opcioncategoria' in request.POST: #condicional para seleccionar las preguntas de la categoria elejidas
                categoria = ""
                for i in request.POST["opcioncategoria"]:  #condicional para que solo quede el nombre de la categoria
                    if i == '-':
                        categoria = categoria[:-2]
                        break
                    categoria += i
                contador_preguntas = 0 #inicializa un contador para manejar la lista de las preguntas
                preguntas_acertadas = 0 #inicializa un contador para guardar las veces que el usuario acerto una pregunta
                pregunta = models.Pregunta.objects.filter(categoria=categoria)
                respuestas = models.Respuesta.objects.filter(id_respuesta = pregunta[contador_preguntas].id_respuesta)
                contador_correctas = 0
                id_usadas = []
                for i in respuestas: #cuenta las cantidad de respuestas correctas
                    if i.es_correcta:
                        contador_correctas += 1
                        id_usadas.append(str(i.id))

                
                tipoopcion = True if contador_correctas < 2 else False  #selecciona si es tipo radio o checkbox segun la cantidad de respuestas correctas 

                return render(request, 'Juego/JuegoPregunta.html', {'categoria':categoria, 'pregunta':pregunta[contador_preguntas].pregunta, 'respuestas':respuestas, 'tipoopcion': tipoopcion, 'numeropregunta':contador_preguntas+1,})

            elif 'respuestaactual' in request.POST and tipoopcion: #condicional para cuando las respuestas son de tipo radio
                respuesta = request.POST["respuestaactual"]
                respuesta = models.Respuesta.objects.get(id=respuesta)
                acerto = respuesta.es_correcta
                contador_preguntas += 1
                if acerto:
                    if contador_preguntas + 1 <= cantidad_preguntas[categoria]: #condicional para saber si las preguntas se terminaron
                        mensaje = 'Has acertado continua'
                        preguntas_acertadas += 1
                        respuestas = models.Respuesta.objects.filter(id_respuesta=pregunta[contador_preguntas].id_respuesta)
                        id_usadas = []                       
                        contador_correctas = 0
                        id_usadas = []
                        for i in respuestas: #cuenta las cantidad de respuestas correctas
                            if i.es_correcta:
                                contador_correctas += 1
                                id_usadas.append(str(i.id))
                        tipoopcion = True if contador_correctas < 2 else False  #selecciona si es tipo radio o checkbox segun la cantidad de respuestas
                                
                        return render(request, 'Juego/JuegoPregunta.html', {'categoria':categoria, 'pregunta':pregunta[contador_preguntas].pregunta, 'respuestas':respuestas, 'tipoopcion': tipoopcion, 'mensaje':mensaje, 'numeropregunta':contador_preguntas+1,})
                    else:
                        mensaje = 'Has completado todas las preguntas'
                        preguntas_acertadas += 1
                        trofeo = True if preguntas_acertadas == cantidad_preguntas[categoria] else False #condicional para ver si contesto correctamente todas las preguntas
                        return render(request, "Juego/JuegoFinal.html", {'mensaje':mensaje,'numerocontestado':preguntas_acertadas, 'numerototalpreguntas':cantidad_preguntas[categoria], 'categoriapregunta':categoria, 'url':url, 'trofeo':trofeo})
                else:
                    mensaje = 'Has perdido'
                    return render(request, "Juego/JuegoFinal.html", {'mensaje':mensaje,'numerocontestado':preguntas_acertadas, 'numerototalpreguntas':cantidad_preguntas[categoria], 'categoriapregunta':categoria, 'url':url})
            
            elif not tipoopcion: #condicional para cuando las respuestas son de tipo checkbox
                contador_preguntas += 1
                acerto_contador = 0
                for i in id_usadas:  #bucle para determinar si el usuario acerto las respuestas checkbox
                    if i in request.POST:
                        acerto_contador += 1

                if acerto_contador == contador_correctas: #condicional para determinar si el usuario acerto todas las respuestas checkbox
                    if contador_preguntas + 1 <= cantidad_preguntas[categoria]: #condicional para saber si las preguntas se terminaron
                        mensaje = 'Has acertado continua'
                        preguntas_acertadas += 1
                        respuestas = models.Respuesta.objects.filter(id_respuesta = pregunta[contador_preguntas].id_respuesta)
                        contador_correctas = 0
                        id_usadas = []
                        for i in respuestas: #cuenta las cantidad de respuestas correctas
                            if i.es_correcta:
                                contador_correctas += 1
                                id_usadas.append(str(i.id))
                        
                        tipoopcion = True if contador_correctas < 2 else False  #selecciona si es tipo radio o checkbox segun la cantidad de respuestas  
                                
                        return render(request, 'Juego/JuegoPregunta.html', {'categoria':categoria, 'pregunta':pregunta[contador_preguntas].pregunta, 'respuestas':respuestas, 'tipoopcion': tipoopcion, 'mensaje':mensaje, 'numeropregunta':contador_preguntas+1,})
                    else:
                        mensaje = 'Has completado todas las preguntas'
                        preguntas_acertadas += 1
                        trofeo = True if preguntas_acertadas == cantidad_preguntas[categoria] else False #condicional para ver si contesto correctamente todas las preguntas
                        return render(request, "Juego/JuegoFinal.html", {'mensaje':mensaje,'numerocontestado':preguntas_acertadas, 'numerototalpreguntas':cantidad_preguntas[categoria], 'categoriapregunta':categoria, 'url':url, 'trofeo':trofeo})
                elif acerto_contador > 0: #condicional para determinar si el usuario acerto parcialmente las respuestas checkbox
                    if contador_preguntas + 1 <= cantidad_preguntas[categoria]: #condicional para saber si las preguntas se terminaron
                        mensaje = 'Has acertado parcialmente continua'
                        respuestas = models.Respuesta.objects.filter(id_respuesta = pregunta[contador_preguntas].id_respuesta)
                        contador_correctas = 0
                        id_usadas = []
                        for i in respuestas: #cuenta las cantidad de respuestas correctas
                            if i.es_correcta:
                                contador_correctas += 1
                                id_usadas.append(str(i.id))
                        tipoopcion = True if contador_correctas < 2 else False  #selecciona si es tipo radio o checkbox segun la cantidad de respuestas 
                                
                        return render(request, 'Juego/JuegoPregunta.html', {'categoria':categoria, 'pregunta':pregunta[contador_preguntas].pregunta, 'respuestas':respuestas, 'tipoopcion': tipoopcion, 'mensaje':mensaje, 'numeropregunta':contador_preguntas+1,})
                    else:  
                        mensaje = 'Has completado todas las preguntas'
                        trofeo = True if preguntas_acertadas == cantidad_preguntas[categoria] else False #condicional para ver si contesto correctamente todas las preguntas
                        return render(request, "Juego/JuegoFinal.html", {'mensaje':mensaje,'numerocontestado':preguntas_acertadas, 'numerototalpreguntas':cantidad_preguntas[categoria], 'categoriapregunta':categoria, 'url':url, 'trofeo':trofeo})
                elif acerto_contador == 0:
                    mensaje = 'Has perdido'
                    return render(request, "Juego/JuegoFinal.html", {'mensaje':mensaje,'numerocontestado':preguntas_acertadas, 'numerototalpreguntas':cantidad_preguntas[categoria], 'categoriapregunta':categoria, 'url':url})
            else:
                return redirect('/juego') 
        else:
            return redirect('/juego')
    else: 
        return redirect('/login')
            

def JuegoCategoria(request):

    if request.user.username:
        global cantidad_preguntas
        cantidad_preguntas = {}
        for i in categorias:
            cantidad = len(models.Pregunta.objects.filter(categoria=i))
            cantidad_preguntas[i] = cantidad
        
        return render(request, 'Juego/JuegoCategoria.html', {'cantidadpreg': cantidad_preguntas})
    else:
        return redirect('/login')

def JuegoInicio(request):

    return render(request, "Juego/JuegoFinal.html")
