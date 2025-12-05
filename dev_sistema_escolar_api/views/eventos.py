from django.db import transaction
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from dev_sistema_escolar_api.models import Evento
from dev_sistema_escolar_api.serializers import EventoSerializer
import json



# OBTENER TODOS LOS EVENTOS
class EventosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        eventos = Evento.objects.all().order_by("id")
        lista = EventoSerializer(eventos, many=True).data



        return Response(lista, 200)


class EventosView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventoSerializer



    # OBTENER EVENTO POR ID
    def get(self, request, *args, **kwargs):
        evento = get_object_or_404(Evento, id=request.GET.get("id"))
        evento = EventoSerializer(evento, many=False).data



        return Response(evento, 200)



    @transaction.atomic
    def post(self, request, *args, **kwargs):

        responsable = get_object_or_404(User, id=request.data["responsable_id"])

        evento = Evento.objects.create(
            nombre_evento = request.data["nombre_evento"],
            tipo_evento = request.data["tipo_evento"],
            fecha_realizacion = request.data["fecha_realizacion"],
            hora_inicio = request.data["hora_inicio"],
            hora_fin = request.data["hora_fin"],
            lugar = request.data["lugar"],
            publico_objetivo = request.data.get("publico_objetivo"),
            programa_educativo = request.data.get("programa_educativo"),
            responsable = responsable,
            descripcion = request.data.get("descripcion"),
            cupo_maximo = request.data["cupo_maximo"]
        )

        evento.save()

        return Response(
            {"evento_created_id": evento.id},
            status=201
        )


    @transaction.atomic
    def put(self, request, *args, **kwargs):

        evento = get_object_or_404(Evento, id=request.data["id"])

        evento.nombre_evento = request.data.get("nombre_evento")
        evento.tipo_evento = request.data.get("tipo_evento")
        evento.fecha_realizacion = request.data.get("fecha_realizacion")
        evento.hora_inicio = request.data.get("hora_inicio")
        evento.hora_fin = request.data.get("hora_fin")
        evento.lugar = request.data.get("lugar")
        evento.programa_educativo = request.data.get("programa_educativo")
        evento.descripcion = request.data.get("descripcion")
        evento.cupo_maximo = request.data.get("cupo_maximo")
        evento.responsable = get_object_or_404(User, id=request.data["responsable_id"])
        evento.publico_objetivo = request.data.get("publico_objetivo")





        evento.save()

        return Response(
            {"message": "Evento actualizado correctamente", "evento_updated_id": evento.id},
            status=200
        )


    # ============================
    # ELIMINAR EVENTO
    # ============================
    @transaction.atomic
    def delete(self, request, *args, **kwargs):

        evento = get_object_or_404(Evento, id=request.GET.get("id"))

        try:
            evento.delete()
            return Response({"details": "Evento eliminado correctamente"}, 200)
        except Exception:
            return Response({"details": "Algo pasó al eliminar"}, 400)
