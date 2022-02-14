from database import DataBase
import math
from datetime import timedelta

database = DataBase()

sp = database.select_sp()


def seg_toSQL(seg_id, Num, date_):
    global vav, Obs_or, Obs_end

    dat_org = database.select_data_forseg(seg_id[0])
    dat_end = database.select_data_forseg(seg_id[-1])
    SPdata_A = "    "
    SPdata_B = "    "
    PointA = "NotSP"
    PointB = "NotSP"

    Dateseg = date_
    desde = dat_org[5]
    hasta = dat_end[5]
    idorg = seg_id[0]
    idend = seg_id[-1]
    mat = dat_org[1]

    AVERAGE_RADIUS = 6378.137
    AVERAGE_CIR = 2 * math.pi * AVERAGE_RADIUS

    Kms = 0
    for i in range(0, len(seg_id) - 1):
        point = database.select_data_forseg(seg_id[i])
        post = database.select_data_forseg(seg_id[i + 1])
        p_1 = point[3], point[4]
        p_2 = post[3], post[4]

        dist = p_2[0] - p_1[0], p_2[1] - p_1[1]
        Kms = Kms + math.sqrt(dist[0] ** 2 + dist[1] ** 2) * AVERAGE_CIR / 360

    eps = 150 * 360 / (2 * math.pi * AVERAGE_RADIUS * 1000)

    # PointA = [dat_org[3], dat_org[4]]

    counter = 0
    for point in sp:
        if abs(float(point[0]) - float(dat_org[3])) <= 3 * eps and abs(float(point[1]) - float(dat_org[4])) <= 3 * eps:
            counter = counter + 1
            SPdata_A = database.select_unique_sp(point[0], point[1])
            if SPdata_A:
                PointA = f"{SPdata_A[3]} {[dat_org[3], dat_org[4]]}"
            Obs_or = ""

    if counter == 0:
        PointA = f"NotSP. Special Point not defined {[dat_org[3], dat_org[4]]} "
        Obs_or = "Origin of segment does not match with Special Point. "

    # PointB = [dat_end[3], dat_end[4]]

    counter = 0
    for point in sp:
        if abs(float(point[0]) - float(dat_end[3])) <= 3 * eps and abs(float(point[1]) - float(dat_end[4])) <= 3 * eps:
            counter = counter + 1
            SPdata_B = database.select_unique_sp(point[0], point[1])
            if SPdata_B:
                PointB = f"{SPdata_B[3]} {[dat_end[3], dat_end[4]]}"
            Obs_end = ""

    if counter == 0:
        PointB = f"NotSP. Special Point not defined {[dat_end[3], dat_end[4]]} "
        Obs_end = "End of segment does not match with Special Point. "

    v = []

    for id in seg_id:
        dat = database.select_data_forseg(id)
        v.append(dat[2])

    Vmax = max(v)

    sumv = 0
    for i in range(0, len(v)):
        sumv += v[i]
        vav = sumv / (i + 1)

    Vavg = vav

    Dateseg = str(Dateseg)
    desde = str(desde)
    hasta = str(hasta)
    Num = str(Num)
    idorg = str(idorg)
    idend = str(idend)
    Kms = str(Kms)
    Vmax = str(Vmax)
    Vavg = str(Vavg)

    seq_ = []
    for point in sp:
        seq = []
        for id in seg_id:
            lon, lat, time = database.select_data_forseq(id)
            if abs(float(point[0]) - lon) <= 3 * eps and abs(float(point[1]) - lat) <= 3 * eps:
                SPdata = database.select_unique_sp(point[0], point[1])
                if SPdata:
                    if not seq:
                        seq.append((time, SPdata[3], (lon, lat), (float(SPdata[2]), float(SPdata[1]), eps)))
                    if (seq[-1])[1] == SPdata[3]:
                        seq.append((time, SPdata[3], (lon, lat), (float(SPdata[2]), float(SPdata[1]), eps)))

        if seq:
            seq_.append(seq)

    seq_.sort()

    obs = []
    if seq_:
        for seq in seq_:
            time_ = timedelta()
            for i in range(0, len(seq) - 1):
                if (seq[i + 1])[0] - (seq[i])[0] <= timedelta(minutes=5):
                    time_ = time_ + (seq[i + 1])[0] - (seq[i])[0]
            obs.append(((seq[0])[1], time_))

    Obs_seq = ""
    for seq in obs:
        if seq[0] != SPdata_A[3] and seq[0] != SPdata_B[3]:
            Obs_seq += str(seq[0]) + " (" + str(seq[1]) + ") / "
    Obs_seq = Obs_seq[:-2]

    Obs = Obs_seq + Obs_or + Obs_end

    if Vmax != "0.0" and Vavg != "0.0" and float(Kms) > 0.5:
        seg_data = (Dateseg, desde, hasta, Num, idorg, idend, mat, PointA, PointB, Kms, Vmax, Vavg, Obs)
        database.add_seg_toSQL(Dateseg, desde, hasta, Num, idorg, idend, mat, PointA, PointB, Kms, Vmax, Vavg, Obs)
        Num = int(Num) + 1

        print(
            f"""Dateseg: {seg_data[0]} 
Desde: {seg_data[1]} 
Hasta: {seg_data[2]} 
Número de Segmento en Ruta: {seg_data[3]} 
ID origen: {seg_data[4]}
ID final: {seg_data[5]}
Matrícula: {seg_data[6]}
Special Point Origen: {seg_data[7]}   
Special Point Final: {seg_data[8]}  
Kilómetros: {seg_data[9]} 
Vmax: {seg_data[10]} 
Vavg: {seg_data[11]} 
Observaciones: {seg_data[12]} 
            """
        )

        return Num

    else:
        print("""No segment.""")
        return int(Num)


"""seg_id = [805197, 805211, 805218, 805227, 805238, 805248, 805255, 805265, 805272, 805281, 805291, 805298, 805307,
          805312, 805318, 805325, 805331, 805339, 805343, 805352, 805356, 805365, 805369, 805379, 805387, 805397,
          805404, 805412, 805420, 805432, 805439, 805453, 805467, 805480, 805488, 805498, 805505, 805515, 805522,
          805531, 805539, 805547, 805561, 805571, 805578, 805586]
Num = 0

seg_toSQL(seg_id, Num)"""
