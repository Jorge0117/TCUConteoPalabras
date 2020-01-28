import numpy as np
import matplotlib.pyplot as plt
import sys
import json
from lmfit import Model
import pdb


def equation_fit(x, beta, alpha):
    y = 1 / (pow(x + beta, alpha))
    return y


def calculateBestFit(x, y):
    # Cargamos ambos contendos desde el json, ambas son listas de floats convertinas a np.arrays
    rank = np.array(x, dtype=np.float64)
    frequency = np.array(y, dtype=np.float64)

    # pdb.set_trace()
    # Fijamos el modelo a usar
    model = Model(equation_fit)
    # Damos la semilla para el calculo de los parametros
    params = model.make_params(beta=2.5, alpha=1)

    # Establecemos un limite inferior para evitar que el ajuste nos de NaN values
    # Si se quita, da NaN's por eso es necesario dejarlo
    params['beta'].min = 0.0000000001
    params['alpha'].min = 0.0000000001

    # Aqui establecemos limistes maximos, pero no es necesario
    # params['A'].max = 20
    # params['beta'].max = 20
    # params['alpha'].max = 20

    # Hacemos el ajuste con los parametros y los datos
    result = model.fit(frequency, params, x=rank)

    # Capturamos los valores de los parametros de ajuste
    params_fit = result.best_values
    # beta_fit = -2.73
    # A_fit = params_fit['A']
    beta_fit = params_fit['beta']
    alpha_fit = params_fit['alpha']

    # generamos la curva de ajuste
    # frequency_fit = result.best_fit
    x_fit = np.linspace(rank[0], rank[-1], len(rank))
    # frequency_fit = equation_fit(x_fit, A_fit, beta_fit, alpha_fit)
    frequency_fit = equation_fit(x_fit, beta_fit, alpha_fit)
    return x_fit, frequency_fit, alpha_fit, beta_fit
