import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from skimage import transform
from skimage.io import imread, imshow

# dictionary of diverse value
colorMol = {"C": "black", "H": "grey"}
sizeMol = {"C": 0.2, "H": 0.1}  # test // todo : ask if it's fine to do that. Also maybe let the user change the values
colorAroma = {0: (1, 0.898, 0.8), 1: (0.984, 0.984, 0.992), 2: (0.906, 0.906, 0.953), 3: (0.831, 0.831, 0.914),
              4: (0.753, 0.753, 0.875)}


def create_projection(filename):
    """Create a 2D projection of a molecule and it's aromaticity.
    :param filename: Location of a file that contain the data of the molecule (use the example in ressources for reference)
    """

    fig, ax = plt.subplots(1, 2, figsize=(20, 10),
                           # figsize makes no sense, I just want a square ffs
                           # //todo : find a better way to do that crap ( best guess : 20 + ( max_y/max_x ) )
                           dpi=80)

    # //todo : maybe put everything in a class and do the file reading in the constructor. (would need to send ax)
    list_mol = []
    list_aroma = []
    origin_x = None
    origin_y = None
    origin_z = None
    incr_aroma_x = 0
    incr_aroma_y = 0

    increment_value_x = 1  # size of each increment on the graph // todo : let the user change it
    increment_value_y = 0.5  # size of each increment on the graph // todo : let the user change it

    # DO NOT DELETE
    # size = 0.1  # size of the molecule circle
    # DO NOT DELETE

    file = open(filename, "r")

    max_y = 0
    max_x = 0

    for line in file.readlines():

        cur_line = line.split()
        print(cur_line)  # not needed // todo : remove at the end

        if len(cur_line) == 0:  # no word on the line => blank line separating aromaticity
            if not origin_x is None:
                list_aroma.append([])

        elif cur_line[0] == "origine":  # if the first word is "origine" => origin value
            origin_x = -float(cur_line[1])  # inelegant reverse origin
            origin_y = -float(cur_line[2])  # inelegant reverse origin
            origin_z = -float(cur_line[3])  # inelegant reverse origin

        elif len(cur_line) == 1:  # only one "word" => aromaticity value
            list_aroma[-1].append(float(cur_line[0]))

            color_aroma = get_aromaticity_color(float(cur_line[0]))

            patch = plt.Circle(
                ((len(list_aroma) - 1) * incr_aroma_x, -1 * (len(list_aroma[-1]) * incr_aroma_y - max_y)),
                0.1, facecolor=color_aroma)  # todo : fix the hardcoded size (should be added to the dictionary)
            # (len(list_aroma)-1) => minus 1 evil trick, but it saves a bit of time
            ax[1].add_patch(patch)

        elif cur_line[0] == "V1":  # if first word V1 => get the space between each aromaticity on x
            incr_aroma_x = float(cur_line[1])
            max_x = float(cur_line[4]) * incr_aroma_x

        elif cur_line[0] == "V2":  # if first word V2 => get the space between each aromaticity on y
            incr_aroma_y = float(cur_line[2])
            max_y = float(cur_line[4]) * incr_aroma_y

            fig.set_figwidth(20 + max_y/max_x)

            ax[0].set_ylim(ax[0].get_ylim()[::-1])  # invert the axis
            ax[0].xaxis.tick_top()  # and move the X-Axis
            ax[0].xaxis.set_ticks(np.arange(0, max_x, increment_value_x))  # set x-ticks
            ax[0].yaxis.set_ticks(np.arange(0, max_y, increment_value_y))  # set y-ticks
            ax[0].yaxis.tick_left()  # move the Y-Axis

            # bis for the second graph
            ax[1].set_ylim(ax[1].get_ylim()[::-1])
            ax[1].xaxis.tick_top()
            ax[1].xaxis.set_ticks(np.arange(0, max_x, increment_value_x))
            ax[1].yaxis.set_ticks(np.arange(0, max_y, increment_value_y))
            ax[1].yaxis.tick_left()

        else:  # last option is always a molecule
            list_mol.append(cur_line)

    file.close()

    for mol in list_mol:  # //todo : check if there's a way to do it in the first loop, would cut some of the processing time.

        cur_color = colorMol[mol[0]]  # chose the molecule color using dictionary

        # no idea how to do that in once instead of twice
        patch1 = plt.Circle((float(mol[1]) + origin_x, -1 * (float(mol[2]) + origin_y - max_y)),
                            sizeMol[mol[0]], facecolor=cur_color)
        patch2 = plt.Circle((float(mol[1]) + origin_x, -1 * (float(mol[2]) + origin_y - max_y)),
                            sizeMol[mol[0]], facecolor=cur_color)

        ax[0].add_patch(patch1)
        ax[1].add_patch(patch2)

    # ax[0].imshow(sign)

    #  filename_to_save = input("nommer le fichier de sauvegarde (appuyez sur entr??e pour ne pas faire de sauvegarde) : \n") //todo : uncomment that
    filename_to_save = "essai.png"  # //todo : comment that
    if not filename_to_save == '':
        save = ""
        if os.path.isfile(filename_to_save):
            save = input("Ce fichier existe deja. L'ecraser ? [y/n] \n")
        while save != "y" and save != "n":
            save = input("Reponse incorrecte, veuillez re-essayer. L'ecraser ? [y/n] \n")
        if save == "y":
            plt.savefig(filename_to_save)
            print("file saved")

    plt.show()  # show delete the graph after usage. ALWAYS AT THE END.


def get_aromaticity_color(aromaticity_value):
    """
    Returns a color depending on the aromaticity
    :param aromaticity_value: Value of the aromaticity of a point in the graph
    :return: A RGB value (x,y,z) based on the dictionary for that range of aromaticity where x, y and z are between 0 and 1
    """
    if aromaticity_value < 0:
        return colorAroma[0]
    elif aromaticity_value < 5:
        return colorAroma[1]
    elif aromaticity_value < 10:
        return colorAroma[2]
    elif aromaticity_value < 15:
        return colorAroma[3]
    else:
        return colorAroma[4]


if __name__ == '__main__':
    #  filenameToParse = input("emplacement du fichier ?? parser : \n") //todo : uncomment that
    filenameToParse = "ressources/test.txt"  # //todo : comment that
    while not os.path.isfile(filenameToParse):
        filenameToParse = input("chemin incorrect ou incomplet. veuillez re-essayer : \n")

    create_projection(filenameToParse)
