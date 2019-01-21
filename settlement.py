import pandas as pd
import numpy as np
import io
from scipy.interpolate import CubicSpline as cbs


def settlement(disp_X, disp_Y):
    """
    Calculate the angular distortion as slopes and
    the horizontal strains as eps_hor_
    :return:
    slopes_ :type: np.array
    eps_hor_ :type: np.array
    """
    try:
        disp_X, disp_Y
    except NameError:
        return

    df_X = pd.read_excel(io.BytesIO(disp_X), names='x y'.split())
    df_Y = pd.read_excel(io.BytesIO(disp_Y), names='x y'.split())

    # round off up to 2 digits for x coordinates
    df_X['x'] = df_X['x'].apply(lambda x: round(x, 2))
    df_Y['x'] = df_Y['x'].apply(lambda x: round(x, 2))

    # drop duplicate entries
    df_X.drop_duplicates(subset='x', keep="last", inplace=True)
    df_Y.drop_duplicates(subset='x', keep="last", inplace=True)

    # sort the x values in ascending
    df_X_sorted = df_X.sort_values('x', ascending=True)
    df_Y_sorted = df_Y.sort_values('x', ascending=True)

    # reset the index of the dataframes
    df_X_sorted.reset_index(inplace=True, drop=True)
    df_Y_sorted.reset_index(inplace=True, drop=True)

    cbs1 = cbs(x=df_Y_sorted['x'], y=df_Y_sorted['y'])
    cbs2 = cbs(x=df_X_sorted['x'], y=df_X_sorted['y'])
    xs1 = np.arange(df_Y_sorted['x'].min(), df_Y_sorted['x'].max(), 0.1)
    xs2 = np.arange(df_X_sorted['x'].min(), df_X_sorted['x'].max(), 0.1)

    x_ang = xs1
    y_ang = cbs1(xs1)
    # x_hor = xs2
    y_hor = cbs2(xs2)

    alpha = []
    for i, _ in enumerate(y_ang):
        try:
            alpha_ = abs(y_ang[i + 200] - y_ang[i]) / abs(x_ang[i + 200] -
                                                          x_ang[i])
            alpha.append(alpha_)
        except IndexError:
            pass
    alpha = np.array(alpha)

    slopes = []
    for i, (x_n, y_n) in enumerate(np.nditer([x_ang, y_ang])):
        try:
            slope = abs(y_ang[i+1] - y_ang[i]) / abs(x_ang[i+1] - x_ang[i])
            alpha = abs(y_ang[i+200] - y_ang[i]) / abs(x_ang[i+200] - x_ang[i])
            slopes.append(slope + alpha)
        except (IndexError, ZeroDivisionError):
            slopes.append(np.nan)
    slopes = np.array(slopes)

    # remove unnecessarily too close points from the array list
    stack = np.stack([slopes, y_hor], axis=-1)
    # first stack x any y coordinates together
    s = np.round(stack, decimals=4)  # then round down to 4 decimals
    s = np.unique(s, axis=0)  # drop the dublicate points
    slopes_ = s[:, 0]  # assign from 2D array first column
    eps_hor_ = s[:, 1]  # assign from 2D array second column
    return slopes_, eps_hor_


def spline(points):
    """interpolate a cubic spline from starting and end points
    while adding an intermediate point in the middle"""
    p1, p2 = points
    i, _ = p1
    _, j = p2
    inc = i/15
    p3 = (i/2 + inc, j/2 + inc)
    x = np.arange(0, i+inc, inc)
    x_ = np.array([p2[0],
                   p3[0],
                   p1[0]])
    y_ = np.array([p2[1],
                   p3[1],
                   p1[1]])
    spl = cbs(x_, y_)
    return x, spl(x)
