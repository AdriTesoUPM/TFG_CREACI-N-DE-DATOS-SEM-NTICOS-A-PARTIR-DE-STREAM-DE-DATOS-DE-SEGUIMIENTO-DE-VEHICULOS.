from database import DataBase
import statistics
import datetime
import numpy as np

database = DataBase()

sp = database.select_sp()


def route_toSQL(route, date_):
    if len(route) > 1:

        seg_org = route[0]
        dat_org = database.select_data_forseg(seg_org[0])

        data = list(database.select_data_for_route(dat_org[1], date_))
        data.sort(key=lambda s: s[2])
        data = np.array(data)

        if len(data) > 1:
            Km = []
            Vmaxs = []
            Vavgs = []
            seqs = []
            seqs_fin = []

            for seg in data:
                Km.append(seg[3])
                Vmaxs.append(seg[6])
                Vavgs.append(seg[7])
                seqs.append(seg[4])
                seqs_fin.append(seg[5])

            if seqs_fin:
                seqs.append(seqs_fin[-1])

            Kms = sum(Km)
            Vmax = max(Vmaxs)
            Vavg = statistics.mean(Vavgs)

            seqParadas = ""
            for point in seqs:
                seqParadas = seqParadas + "/" + point[0: 6]
            seqParadas = seqParadas[1:].replace(" ", "")

            seg_ini = []
            seg_fin = []
            for seg in data:
                seg_ini.append(seg[0])
                seg_fin.append(seg[1])

            DurViajes = datetime.timedelta()
            for i in range(0, len(seg_ini)):
                DurViajes = DurViajes + (seg_fin[i] - seg_ini[i])

            DurParadas = datetime.timedelta()
            for i in range(0, len(seg_ini) - 1):
                DurParadas = DurParadas + (seg_ini[i + 1] - seg_fin[i])

            org = data[0]
            end = data[-1]

            date_ = datetime.datetime.strptime(date_, '%Y-%m-%d %H:%M:%S')

            Date = date_
            DiaSem = date_.strftime('%A')
            desde = org[0]
            hasta = end[1]
            Idorg = org[10]
            Idend = end[10]
            matricula = dat_org[1]
            NumSeg = (data[-1])[2]
            NumParadas = (data[-1])[2] - 1

            route_data = (
                Date, desde, hasta, matricula, NumSeg, Idorg, Idend, NumParadas, DurViajes, DurParadas, seqParadas, Kms,
                Vmax, Vavg, DiaSem)

            database.add_route_toSQL(str(Date), str(desde), str(hasta), str(matricula), str(NumSeg), str(Idorg), str(Idend),
                                     str(NumParadas), str(DurViajes), str(DurParadas),
                                     seqParadas, str(Kms), str(Vmax), str(Vavg), DiaSem)

            print(
                f"""Date: {route_data[0]} 
Desde: {route_data[1]} 
Hasta: {route_data[2]} 
Matricula: {route_data[3]} 
Número de Segmentos: {route_data[4]}
ID origen: {route_data[5]}
ID final: {route_data[6]}
Número de Paradas: {route_data[7]}  
Duración Viajes: {route_data[8]} 
Duración Paradas: {route_data[9]}
Secuencia Paradas: {route_data[10]}  
Kilómetros: {route_data[11]} 
Vmax: {route_data[12]} 
Vavg: {route_data[13]} 
Día de la Semana: {route_data[14]} 
                    """
            )


    else:

        print("No route")
