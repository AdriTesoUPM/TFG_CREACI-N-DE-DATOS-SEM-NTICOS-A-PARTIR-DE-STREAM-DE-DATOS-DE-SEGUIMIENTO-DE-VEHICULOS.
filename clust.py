# dbscan clustering
import math
from database import DataBase
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np

database = DataBase()


def clustering():
    eps = 150
    mpts = 300

    users_20 = database.select_users_20()
    users_30_10 = database.select_users_30_10()

    clusters_20 = clustering_20(users_20, eps, mpts)
    clusters_30_10 = clustering_past(users_30_10, eps, mpts)

    sp = sec_depur(clusters_20 + clusters_30_10, eps)

    return sp


def clustering_past(users_past, eps, mpts):
    locationsForDBSCAN = [list([user[2], user[3]])
                          for user in users_past]

    x = np.array(locationsForDBSCAN)
    AVERAGE_CIR = 6378.137 * 1000 * 2 * math.pi
    eps = eps * 360 / AVERAGE_CIR

    db = DBSCAN(eps=eps, min_samples=mpts,
                metric='euclidean').fit(x)

    # PARA SPECIAL POINTS
    cores = db.components_

    clusters = []
    for i in range(0, len(cores)):
        if len(clusters) > 0:
            counter = 0
            for clust in clusters:
                if abs(cores[i, 0] - clust[0]) <= eps and abs(cores[i, 1] - clust[1]) <= eps:
                    counter = counter + 1

            if counter == 0:
                clusters.append(cores[i])

        else:
            clusters.append(cores[i])

    return clusters


def clustering_20(users_20, eps, mpts):
    locationsForDBSCAN = [list([user[2], user[3]])
                          for user in users_20]

    x = np.array(locationsForDBSCAN)
    AVERAGE_CIR = 6378.137 * 1000 * 2 * math.pi
    eps = eps * 360 / AVERAGE_CIR

    db = DBSCAN(eps=eps, min_samples=mpts,
                metric='euclidean').fit(x)

    # PARA SPECIAL POINTS
    cores = db.components_

    clusters = []
    for i in range(0, len(cores)):
        if len(clusters) > 0:
            counter = 0
            for clust in clusters:
                if abs(cores[i, 0] - clust[0]) <= eps and abs(cores[i, 1] - clust[1]) <= eps:
                    counter = counter + 1

            if counter == 0:
                clusters.append(cores[i])

        else:
            clusters.append(cores[i])

    # GRAFICADO

    plt.gca().set_facecolor('white')
    plt.scatter(x[:, 1], x[:, 0], c='black')
    plt.scatter(cores[:, 1], cores[:, 0], c='aqua')
    plt.show()

    return clusters


def sec_depur(clusters, eps):

    cls = np.array(clusters)

    AVERAGE_CIR = 6378.137 * 1000 * 2 * math.pi
    eps = eps * 3 * 360 / AVERAGE_CIR

    sp = DBSCAN(eps=eps, min_samples=1,
                metric='euclidean').fit(cls)

    sp_cores = sp.components_

    sp = []
    for i in range(0, len(sp_cores)):
        if len(sp) > 0:
            counter = 0
            for clust in sp:
                if abs(sp_cores[i, 0] - clust[0]) <= eps and abs(sp_cores[i, 1] - clust[1]) <= eps:
                    counter = counter + 1

            if counter == 0:
                sp.append(sp_cores[i])

        else:
            sp.append(sp_cores[i])

    return sp


