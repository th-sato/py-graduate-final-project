# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import cv2 as cv
import base64
import ast
import os

STATIC_PATH = os.path.join(os.getcwd(), 'web-application/static/results/')
IMG_NAME_TIME_SPEED = 'time_speed.png'
IMG_NAME_TIME_DISTCENTER ='time_distcenter.png'
IMG_NAME_TIME_ANGLE ='time_angle.png'
IMG_NAME_TIME_RCURV ='time_curv.png'
IMG_NAME_SPEED_CURV = 'speed_curv.png'
IMG_NAME_ANGLE_DISTCENTER = 'angle_distcenter.png'

IMG_NAMES = [
    IMG_NAME_TIME_SPEED,
    IMG_NAME_TIME_DISTCENTER,
    IMG_NAME_TIME_RCURV,
    IMG_NAME_TIME_ANGLE,
    IMG_NAME_SPEED_CURV,
    IMG_NAME_ANGLE_DISTCENTER
]


def get_base64_img_graphic(img_id):
    img_name = IMG_NAMES[img_id]
    img_path = STATIC_PATH + img_name
    img = cv.imread(img_path)
    _, png = cv.imencode('.png', img)
    return base64.b64encode(png)


def convert_string_to_dict(item):
    return ast.literal_eval(item)


def gen_data_by_field(points, field):
    data = []
    for i in points:
        data.append(i[field])

    return data


def gen_plot_by_values(axis_x, axis_y, name_img, title=u'Título', axis_x_name=u'Eixo x', axis_y_name=u'Eixo y'):
    plt.plot(axis_x, axis_y)
    plt.xlabel(axis_x_name)
    plt.ylabel(axis_y_name)
    plt.title(title)
    plt.savefig(STATIC_PATH + name_img)
    plt.clf()


def gen_scatter_by_values(axis_x, axis_y, name_img, title=u'Título', axis_x_name=u'Eixo x', axis_y_name=u'Eixo y'):
    plt.scatter(axis_x, axis_y)
    plt.xlabel(axis_x_name)
    plt.ylabel(axis_y_name)
    plt.title(title)
    plt.savefig(STATIC_PATH + name_img)
    plt.clf()


def gen_graphics(points):
    # order by time
    points = sorted(points, key=lambda k: k['time'])
    data = {'time': gen_data_by_field(points, 'time'), 'speed': gen_data_by_field(points, 'speed'),
            'angle': gen_data_by_field(points, 'angle'), 'dist_center': gen_data_by_field(points, 'dist_center'),
            'curv': gen_data_by_field(points, 'curv')}

    gen_plot_by_values(data['time'], data['speed'], IMG_NAMES[0], title=u'Velocidade x Tempo', axis_x_name=u'Tempo',
                       axis_y_name=u'Velocidade')
    gen_plot_by_values(data['time'], data['dist_center'], IMG_NAMES[1], title=u'Distância do centro x Tempo',
                       axis_x_name=u'Tempo', axis_y_name=u'Distância do centro')

    gen_plot_by_values(data['time'], data['curv'], IMG_NAMES[2], title=u'Raio de Curvatura x Tempo',
                       axis_x_name=u'Tempo', axis_y_name=u'Raio de Curvatura')
    gen_plot_by_values(data['time'], data['angle'], IMG_NAMES[3], title=u'Ângulo x Tempo',
                       axis_x_name=u'Tempo', axis_y_name=u'Ângulo')

    gen_scatter_by_values(data['speed'], data['curv'], IMG_NAMES[4], title=u'Curvatura x Velocidade',
                          axis_x_name=u'Velocidade', axis_y_name=u'Curvatura')
    gen_scatter_by_values(data['angle'], data['dist_center'], IMG_NAMES[5], title=u'Distância do Centro x Ângulo',
                          axis_x_name=u'Ângulo', axis_y_name=u'Distância do Centro')
