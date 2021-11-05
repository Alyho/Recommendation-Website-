import pathlib
import pickle
import time

import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

class Model:
    def __init__(self):
        self.a_dict = {"1": 0, "18": 1, "25": 2, "35": 3, "45": 4, "50": 5, "56": 6}
        self.movie_number_dict = {}
        prefix = pathlib.Path(__file__).parent.resolve().__str__()
        with open(prefix+'/movies.dat', 'r') as f:
            for line in f:
                y = line.split("::")
                self.movie_number_dict[int(y[0])]=y[1]
        self.loaded = False
        pass

    def save(self):
        with open("file.file", 'wb+') as f:
            j = pickle.dumps(self.sols)
            f.write(j)

        print('saved')

    def load_model_from_file(self):
        with open("file.file", 'rb+') as f:
            j = pickle.loads(f.read())
            self.sols = j
        self.loaded = True
        print(self.sols)

    def predict(self, userdata, movie_to_predict_on_number):
        if self.loaded:
            y = userdata.split("::")
            uservector = np.zeros(9)
            gen = (y[1] == 'M')
            def bucket_age(given_age):
                i = int(given_age)
                bucketed_age = 1
                age_distance = 999
                for j in self.a_dict.keys():
                    if int(j)-i < age_distance:
                        age_distance = int(j)-i
                        bucketed_age = int(j)
                return bucketed_age
            y[2] = str(bucket_age(y[2]))
            age = self.a_dict[y[2]]
            # zip = int((y[4])[0])
            # UF[int(y[0])-1][7 * gen + age] = 1
            # UF[int(y[0])-1][9+int(y[3])] = 1
            uservector[gen] = 1
            uservector[age + 2] = 1
            # print(type(movie_to_predict_on_number))
            return self.sols[movie_to_predict_on_number] @ uservector
        else: return None

    def load_model(self):
        # m1, m2, m3 are sizes of the 3 sets (split on rows = users)
        m1 = 3000
        m2 = 500
        m3 = 500
        # n is the # of movies used
        n = 3952  # 1000
        # d is the size of the user vector
        # a is the alpha value
        d = 9
        a = 0.1
        z = 60

        # UM = users x movies (ratings) matrix
        # UF = users x user features matrix [gender, age, occupation]
        UM = np.zeros((m1 + m2 + m3, n))
        UF = np.zeros((m1 + m2 + m3, d))

        self.movie_number_dict = {}

        # Maps movie genres to numbers (not used yet)
        mt_dict = {"Action": 0, "Adventure": 1, " Animation": 2, "Children's": 3,
                   "Comedy": 4,
                   "Crime": 5,
                   "Documentary": 6,
                   "Drama": 7,
                   "Fantasy": 8,
                   "Film-Noir": 9,
                   "Horror": 10,
                   "Musical": 11,
                   "Mystery": 12,
                   "Romance": 13,
                   "Sci-Fi": 14,
                   "Thriller": 15,
                   "War": 16,
                   "Western": 17
                   }
        self.a_dict = {"1": 0, "18": 1, "25": 2, "35": 3, "45": 4, "50": 5, "56": 6}
        mv = [0] * n

        # ctr2[i] is the # of actual ratings for movie i in the m1 to m1+m2 part of the data
        scl = [0] * (m1 + m2 + m3)
        u_ctr = [0] * (m1 + m2 + m3)
        ctr1 = [0] * n
        ctr2 = [0] * n
        ctr3 = [0] * n
        prefix = pathlib.Path(__file__).parent.resolve().__str__()

        with open(prefix+'/ratings.dat', 'r') as f:
            for line in f:
                y = line.split('::')
                if (y[0] == "{}".format(m1 + m2 + m3 + 1)):  # stops when it sees first users > m
                    break
                if (int(y[1]) <= n):  # only includes movies from 1 to n
                    # Put the rating into UM
                    UM[int(y[0]) - 1][int(y[1]) - 1] = int(y[2])
                    u_ctr[int(y[0]) - 1] += 1
                    # Increase ctr2 by 1 if this is a rating in [m1, m1+m2)
                    ctr1[int(y[1]) - 1] += ((int(y[2]) > 0) and int(y[0]) > 0 and int(y[0]) <= m1)
                    ctr2[int(y[1]) - 1] += ((int(y[2]) > 0) and int(y[0]) > m1 and int(y[0]) <= m1 + m2)
                    ctr3[int(y[1]) - 1] += ((int(y[2]) > 0) and int(y[0]) > m1 + m2 and int(y[0]) <= m1 + m2 + m3)

        with open(prefix+'/movies.dat', 'r') as f:
            for line in f:
                y = line.split("::")
                self.movie_number_dict[int(y[0])]=y[1]

        t = True
        # reading users.dat file, forms user-feature matrix
        with open(prefix+'/users.dat', 'r') as f:
            for line in f:
                y = line.split('::')
                if (y[0] == "{}".format(m1 + m2 + m3 + 1)):  # stops when it sees user m+1
                    break
                gen = (y[1] == 'M')
                age = self.a_dict[y[2]]
                # zip = int((y[4])[0])
                # UF[int(y[0])-1][7 * gen + age] = 1
                # UF[int(y[0])-1][9+int(y[3])] = 1
                UF[int(y[0]) - 1][gen] = 1
                UF[int(y[0]) - 1][age + 2] = 1
                if t:
                    print(UF[int(y[0]) - 1])
                    t = False

        # form UFM (users who have not rated movie 0 set to 0)
        # UFM is a matrix containing all of the user vectors, each row is a user vector
        # If a user has not rated movie i, the user vectors consists of all 0s
        # UM2 is the matrix containing all of the user ratings for movie i
        # sols[i] is the movie vector for movie i produced by the LR

        UFM = np.zeros((m1, d))
        UM2 = np.zeros(m1)
        sols = np.zeros((n, d))
        t = time.time() * 1000
        for i in range(n):
            for j in range(m1):
                # if user j has rated movie i
                if (UM[j][i] > 0):
                    UFM[j] = UF[j]
                    UM2[j] = UM[j][i]
                # if not it remains 0 as default

            x = cp.Variable(d)
            cost = cp.sum_squares(UFM @ x - UM2)
            prob = cp.Problem(cp.Minimize(cost))
            prob.solve()
            # print()
            # x.value is the movie vector
            sols[i] = x.value
            # print(UF[0])
            # print(sols[i])
            # Reset UFM to all zeros
            for j in range(m1):
                if (UM[j][i] > 0):
                    UFM[j] = [0] * d

        print("everything=", time.time() * 1000 - t)

        # UP is the user prediction matrix
        # It's like UM, but each element of the matrix is our prediction
        UP = np.zeros((m1 + m2 + m3, n))
        # q is the array of 1-a quantile error
        q = [0] * n
        for j in range(n):
            # t is a ticker variable used to put in values
            # e is the array that stores for errors for movie j (hence it has size ctr2[j])
            t = 0
            e = [0] * (ctr2[j])
            for i in range(m1, m1 + m2):
                # inner product calculates the prediction
                UP[i][j] = np.inner(UF[i], sols[j])
                if (UM[i][j] > 0):
                    e[t] = abs(UM[i][j] - UP[i][j])
                    t += 1
            # if no ratings for this movie, pretend its 1.51
            if (ctr2[j] < z):
                q[j] = 0
            else:
                # q[j] = np.quantile(e, (1 - a) * (1 + 1 / max(60, ctr2[j])))
                q[j] = np.quantile(e, (1 - a))
                # print(q[j])

        t = 0
        c_num = 0
        # c_num is the number of predictions that worked, t is the total
        # hence c_num/t is the coverage

        c_movie = [0] * n
        a = [0] * n
        for i in range(m1 + m2, m1 + m2 + m3):
            for j in range(n):
                UP[i][j] = (np.inner(UF[i], sols[j]))
                if (UM[i][j] > 0 and ctr2[j] >= z):
                    # testing coverage
                    # if the true value is <= q[j] away from our prediction, a.k.a it lies in the interval
                    # increase c_num by 1
                    l = UP[i][j] - q[j]
                    l = max(l, 1)
                    l = np.ceil(l)
                    r = UP[i][j] + q[j]
                    r = min(r, 5)
                    r = np.floor(r)
                    a[j] += r - l + 1
                    c_num += l <= UM[i][j] and UM[i][j] <= r
                    t += 1
                    c_movie[j] += l <= UM[i][j] and UM[i][j] <= r

        for j in range(n):
            if (ctr3[j] == 0):
                c_movie[j] = 1
            else:
                c_movie[j] = c_movie[j] / ctr3[j]

        self.sols = sols
        self.loaded = True
        print("Model Loaded")
        self.save()

        # the problem here is that np.mean(q) is not the mean size
        # S2 is the sum of the interval sizes, iterating by 1
        # S is the number of intervals
        # hence dividing them is the average
        # S = 0
        # S2 = 0
        # for i in range(n):
        #     if (ctr2[i] >= z):
        #         S2 += a[i]
        #         S += ctr3[i]
        # print(S2 / t)
        #
        # # this is coverage
        # print(c_num / t)
        # print(np.mean(ctr1))
        #
        # print(m1 + m2 + m3)
        # print(n)
        # print(d)
        # Version 1:
        # Results of (m1, m2, m3, n, d, alpha, z) = (5000, 500, 500, 1000, 9, 0.1, 60)
        # coverage  = 0.900
        # average size = 2.80

        # Matplot lib graph (histogram of q)
        # n_bins = 20
        # fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
        # axs[0].hist(q, bins=n_bins)
        # plt.show()
        #
        # fig, ax = plt.subplots()
        # ax.scatter(ctr1, c_movie)
        # plt.xlabel('training data set size')
        # plt.ylabel('interval radius')
        # plt.show()