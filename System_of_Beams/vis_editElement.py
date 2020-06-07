import math

# import local files
import vis_callbacks as vis_cbs
import vis_initialization as vis_init
import vis_elementToPlot as vis_elToP
from Classes import ElementSupportEnum as eLnum
from Classes.CurrentDocument import CurrentDoc

# used to normalize all line loads with their maximum value and the maximum height in the input plot
line_load_max_height = 0.2
line_load_max_value = 1.0
# used to keep a distance between a line load and the corresponding beam
distance_beam = 0.08


def change_angle_indep(curr_doc: CurrentDoc, name_indep, angle, index):
    """
    Change the angle of a node independent element. Updates the glyph of the plot and the glyph data source.
    :param name_indep: name of the node independent element (string)
    :param angle: new angle (rad)
    :param index: index of the element in ds_indep_elements (int)
    :return: True if angle of element was adapted (bool)
    """
    enum_type = curr_doc.data_sources.ds_indep_elements.data['type'][index]

    if enum_type == eLnum.ElSupEnum.JOINT.value or enum_type == eLnum.ElSupEnum.NODE.value:
        return False

    width = curr_doc.data_sources.ds_images.data['w'][vis_elToP.map_enum2images[enum_type]]
    height = curr_doc.data_sources.ds_images.data['h'][vis_elToP.map_enum2images[enum_type]]

    # get offset for x and y through rotation
    if enum_type == eLnum.ElSupEnum.SUPPORT_ROLLER_JOINT.value \
            or enum_type == eLnum.ElSupEnum.SUPPORT_ROLLER_CONTINUOUS.value \
            or enum_type == eLnum.ElSupEnum.SUPPORT_FIXED_JOINT.value \
            or enum_type == eLnum.ElSupEnum.SUPPORT_FIXED_CONTINUOUS.value:
        # get y_mod for 0°
        y_mod = curr_doc.data_sources.ds_images.data['y_mod'][vis_elToP.map_enum2images[enum_type]]

        # calculate offset for x and y through rotation (center offset and fitted equation)
        x_mod = - y_mod * math.sin(angle) + 0.23 * math.sin(angle - 2.3) + width / 2
        y_mod = y_mod * math.cos(angle) + 0.24 * math.sin(angle - 3.85) - height / 2
    else:
        x_mod = 0.145 * math.sin(angle - 2.1) + width / 2
        y_mod = 0.15 * math.sin(angle - 3.65) - height / 2

    # set angle and offset of image glyph for given name
    image_glyph = curr_doc.plot_input.select(name=name_indep)
    image_glyph[0].glyph.update(angle=angle)
    image_glyph[0].glyph.update(x=curr_doc.data_sources.ds_indep_elements.data['x'][index] + x_mod)
    image_glyph[0].glyph.update(y=curr_doc.data_sources.ds_indep_elements.data['y'][index] + y_mod)
    return True


def change_angle_nodedep(curr_doc: CurrentDoc, name_nodedep, angle, index, index_glyph=False):
    """
    Change the angle of a nodedependent element of the enum_type spring_support, spring_moment_support or load_point.
    All other enum_types can only be changed if one of their nodes changed position.
    Updates glyph of the plot and the glyph data source, as well as the position in the data source ds_nodedep_elements.
    :param name_nodedep: name of the nodedependent element (string)
    :param angle: new angle (rad)
    :param index: index of the element in ds_nodedep_elements (int)
    :param index_glyph: index of the element in its glyph data source (int)
    :return: True if angle of element was adapted (bool)
    """
    enum_type = curr_doc.data_sources.ds_nodedep_elements.data['type'][index]

    if enum_type == eLnum.ElSupEnum.SPRING_SUPPORT.value or enum_type == eLnum.ElSupEnum.SPRING_MOMENT_SUPPORT.value \
            or enum_type == eLnum.ElSupEnum.LOAD_POINT.value:
        # get y_mod for 0° (center offset)
        y_mod_center = curr_doc.data_sources.ds_images.data['y_mod'][vis_elToP.map_enum2images[enum_type]]
        width = curr_doc.data_sources.ds_images.data['w'][vis_elToP.map_enum2images[enum_type]]
        height = curr_doc.data_sources.ds_images.data['h'][vis_elToP.map_enum2images[enum_type]]

        angle_sin = math.sin(angle)
        angle_cos = math.cos(angle)
        # calculate offset for x and y through rotation (center offset and fitted equation)
        if enum_type == eLnum.ElSupEnum.LOAD_POINT.value:
            x_mod = - y_mod_center * angle_sin + 0.2 * math.sin(angle - 2.75) + width / 2
            y_mod = y_mod_center * angle_cos + 0.22 * math.sin(angle - 4.35) - height / 2
        else:
            x_mod = - y_mod_center * angle_sin + 0.23 * math.sin(angle - 2.3) + width / 2
            y_mod = y_mod_center * angle_cos + 0.24 * math.sin(angle - 3.85) - height / 2

        # get x and y position of node
        x = curr_doc.data_sources.ds_nodedep_elements.data['x'][index]
        y = curr_doc.data_sources.ds_nodedep_elements.data['y'][index]

        # set angle and offset of image glyph for given name
        image_glyph = curr_doc.plot_input.select(name=name_nodedep)
        image_glyph[0].glyph.update(angle=angle)
        image_glyph[0].glyph.update(x=x+x_mod)
        image_glyph[0].glyph.update(y=y+y_mod)

        ds_glyph = curr_doc.data_sources.ds_glyph_springsPointMomentTemp
        # get index of element in glyph data source if not given
        if not index_glyph:
            for i in range(len(ds_glyph.data['name_user'])):
                if name_nodedep == ds_glyph.data['name_user'][i]:
                    index_glyph = i
                    break
        # update data source
        ds_glyph.data['glyph_x'][index_glyph] = x - (y_mod_center * 1.5) * angle_sin
        ds_glyph.data['glyph_y'][index_glyph] = y + (y_mod_center * 1.5) * angle_cos
        ds_glyph.trigger('data', ds_glyph.data, ds_glyph.data)
        return True
    else:
        return False


# TODO: idea - allow user to change position of independent elements
# def change_angle_nodedep(name_indep, name_nodedep=False):
#
#     :return:
#     """
#
#
# def change_position_indep(name_indep, new_x, new_y):
#     change_position_nodedep(name_indep)
#     change_angle_nodedep(name_indep)
#
#
# def change_position_nodedep(name_indep):
#     """
#
#     :return:
#     """
#
#
# TODO: idea - allow an arbitory angle and a user-defined function as input
def draw_lineload(curr_doc: CurrentDoc, name, load_x_n, load_y_q, local, index, index_glyph=False, create_element=False):
    """
    Draw a new or change a line load element with its patch glyph arrows and data sources. Therefore the single points
    of the line load patch glyphs and the arrows as line are calculated.
    :param name: name of the line load element (string)
    :param load_x_n: Tupel with start (node1) and end (node2) value of the x or normal load (Tupel)
    :param load_y_q: Tupel with the start (node1) and end (node2) value of the y or shear load (Tupel)
    :param local: True if line load act locally with normal and shear loads,
                False if global x and y loads are wanted (bool)
    :param index: index of the element in the ds_nodedep_elements (int)
    :param index_glyph: index of the element in its glyph data source (int)
    :param create_element: False if element already was created and only needs adaptation (bool)
    :return: none
    """
    global line_load_max_value, line_load_max_height, distance_beam

    # check which load directions are non zero
    valid_xn = False
    valid_yq = False
    if not load_x_n[0] == 0 or not load_x_n[1] == 0:
        valid_xn = True
    if not load_y_q[0] == 0 or not load_y_q[1] == 0:
        valid_yq = True

    # TODO: idea - get global max line load value and adapt line load heights of other line loads aswell
    # if valid_xn:
    #     if abs(load_x_n[0]) > line_load_max_value:
    #         line_load_max_value = abs(load_x_n[0])
    #     if abs(load_x_n[1]) > line_load_max_value:
    #         line_load_max_value = abs(load_x_n[1])
    # if valid_yq:
    #     if abs(load_y_q[0]) > line_load_max_value:
    #         line_load_max_value = abs(load_y_q[0])
    #     if abs(load_y_q[1]) > line_load_max_value:
    #         line_load_max_value = abs(load_y_q[1])

    # get magnitude of load at start (node1) and end (node2)
    start_xn = 0
    end_xn = 0
    start_yq = 0
    end_yq = 0
    if valid_xn:
        start_xn = load_x_n[0] * line_load_max_height / line_load_max_value
        end_xn = load_x_n[1] * line_load_max_height / line_load_max_value
    if valid_yq:
        start_yq = load_y_q[0] * line_load_max_height / line_load_max_value
        end_yq = load_y_q[1] * line_load_max_height / line_load_max_value

    # get values of nodedependent element data source
    x = curr_doc.data_sources.ds_nodedep_elements.data['x'][index]
    y = curr_doc.data_sources.ds_nodedep_elements.data['y'][index]
    length = curr_doc.data_sources.ds_nodedep_elements.data['length'][index]
    angle = curr_doc.data_sources.ds_nodedep_elements.data['angle'][index]
    angle_sin = math.sin(angle)
    angle_cos = math.cos(angle)

    # compute position modification
    x_mod, y_mod = get_lineload_mod(distance_beam, 0, angle)

    # compute points of the edge that is parallel to the beam for patch glyphs
    # for x/ normal load
    x1_xn = x - x_mod - length / 2 * angle_cos
    y1_xn = y - y_mod - length / 2 * angle_sin
    x2_xn = x - x_mod + length / 2 * angle_cos
    y2_xn = y - y_mod + length / 2 * angle_sin
    # for y/ shear load
    x1_yq = x1_xn + 2 * x_mod
    y1_yq = y1_xn + 2 * y_mod
    x2_yq = x2_xn + 2 * x_mod
    y2_yq = y2_xn + 2 * y_mod

    # compute remaining points for patch glyphs and add to list
    patch_x = []
    patch_y = []
    # for x/ normal load
    if valid_xn:
        patch_x.extend([x1_xn, x2_xn])
        patch_y.extend([y1_xn, y2_xn])
        if local:
            patch_x.extend([x2_xn + abs(end_xn) * angle_sin, x1_xn + abs(start_xn) * angle_sin])
            patch_y.extend([y2_xn - abs(end_xn) * angle_cos, y1_xn - abs(start_xn) * angle_cos])
        else:
            patch_x.extend([x2_xn, x1_xn])
            patch_y.extend([y2_xn - abs(end_xn), y1_xn - abs(start_xn)])
    # for y/ shear load
    if valid_yq:
        if valid_xn:
            patch_x.append('nan')
            patch_y.append('nan')
        patch_x.extend([x1_yq, x2_yq])
        patch_y.extend([y1_yq, y2_yq])
        if local:
            patch_x.extend([x2_yq - abs(end_yq) * angle_sin, x1_yq - abs(start_yq) * angle_sin])
            patch_y.extend([y2_yq + abs(end_yq) * angle_cos, y1_yq + abs(start_yq) * angle_cos])
        else:
            patch_x.extend([x2_yq, x1_yq])
            patch_y.extend([y2_yq + abs(end_yq), y1_yq + abs(start_yq)])

    # add element to datasource of line load glyphs and info
    if create_element:
        curr_doc.data_sources.ds_glyph_lineload.data['patch_x'].append(patch_x)
        curr_doc.data_sources.ds_glyph_lineload.data['patch_y'].append(patch_y)
        if valid_yq:
            curr_doc.data_sources.ds_glyph_lineload.data['glyph_x'].append(x + x_mod * 1.8)
            curr_doc.data_sources.ds_glyph_lineload.data['glyph_y'].append(y + y_mod * 1.8)
        else:
            curr_doc.data_sources.ds_glyph_lineload.data['glyph_x'].append(x - x_mod * 1.8)
            curr_doc.data_sources.ds_glyph_lineload.data['glyph_y'].append(y - y_mod * 1.8)
        curr_doc.data_sources.ds_glyph_lineload.data['x'].append(x)
        curr_doc.data_sources.ds_glyph_lineload.data['y'].append(y)
        curr_doc.data_sources.ds_glyph_lineload.data['name_user'].append(name)
    else:
        if not index_glyph:
            for i in range(len(curr_doc.data_sources.ds_glyph_lineload.data['name_user'])):
                if curr_doc.data_sources.ds_glyph_lineload.data['name_user'][i] == name:
                    index_glyph = i
                    break
        curr_doc.data_sources.ds_glyph_lineload.data['patch_x'][index_glyph] = patch_x
        curr_doc.data_sources.ds_glyph_lineload.data['patch_y'][index_glyph] = patch_y
        if valid_yq:
            curr_doc.data_sources.ds_glyph_lineload.data['glyph_x'][index_glyph] = x + x_mod * 1.8
            curr_doc.data_sources.ds_glyph_lineload.data['glyph_y'][index_glyph] = y + y_mod * 1.8
        else:
            curr_doc.data_sources.ds_glyph_lineload.data['glyph_x'][index_glyph] = x - x_mod * 1.8
            curr_doc.data_sources.ds_glyph_lineload.data['glyph_y'][index_glyph] = y - y_mod * 1.8
        curr_doc.data_sources.ds_glyph_lineload.data['x'][index_glyph] = x
        curr_doc.data_sources.ds_glyph_lineload.data['y'][index_glyph] = y
    curr_doc.data_sources.ds_glyph_lineload.trigger('data', curr_doc.data_sources.ds_glyph_lineload.data,
                                                    curr_doc.data_sources.ds_glyph_lineload.data)

    # length of arrow line and head and angle of arrow head
    arrow_length = 0.12
    arrow_head_length = 0.1
    delta = math.radians(45)

    # zero angle of arrow for globally defined load
    if local:
        gamma = angle
        distance_fac = 1.5
    else:
        gamma = 0
        distance_fac = 1.5

    # calculate modifications for arrow lines
    arrow_mod_sin = arrow_length / 2 * math.sin(gamma)
    arrow_mod_cos = arrow_length / 2 * math.cos(gamma)
    # calculate positions of arrow line of x/ normal load
    x_left, y_left, x_right, y_right = [0, 0, 0, 0]
    if valid_xn:
        x_center_leftright = x - x_mod * distance_fac
        y_center_leftright = y - y_mod * distance_fac
        x_left = x_center_leftright - arrow_mod_cos
        y_left = y_center_leftright - arrow_mod_sin
        x_right = x_center_leftright + arrow_mod_cos
        y_right = y_center_leftright + arrow_mod_sin
    # calculate positions of arrow line of y/ shear load
    x_down, y_down, x_up, y_up = [0, 0, 0, 0]
    if valid_yq:
        x_down = x + x_mod * distance_fac
        y_down = y + y_mod * distance_fac
        x_up = x_down - 2 * arrow_mod_sin
        y_up = y_down + 2 * arrow_mod_cos

    # calculate modifications for arrow heads
    arrow_mod_sin_add = arrow_head_length / 2 * math.sin(delta + gamma)
    arrow_mod_cos_add = arrow_head_length / 2 * math.cos(delta + gamma)
    arrow_mod_sin_sub = arrow_head_length / 2 * math.sin(delta - gamma)
    arrow_mod_cos_sub = arrow_head_length / 2 * math.cos(delta - gamma)

    # create arrow for x/ normal load
    if valid_xn:
        # if positive
        if start_xn > 0 or end_xn > 0:
            xs_xn = [x_left, x_right, x_right - arrow_mod_cos_add, x_right, x_right - arrow_mod_cos_sub]
            ys_xn = [y_left, y_right, y_right - arrow_mod_sin_add, y_right, y_right + arrow_mod_sin_sub]
        # if negative
        else:
            xs_xn = [x_right, x_left, x_left + arrow_mod_cos_sub, x_left, x_left + arrow_mod_cos_add]
            ys_xn = [y_right, y_left, y_left - arrow_mod_sin_sub, y_left, y_left + arrow_mod_sin_add]
    else:
        xs_xn = []
        ys_xn = []

    # create arrow for y/ shear load
    if valid_yq:
        # if positive
        if start_yq > 0 or end_yq > 0:
            xs_yq = [x_down, x_up, x_up - arrow_mod_sin_sub, x_up, x_up + arrow_mod_sin_add]
            ys_yq = [y_down, y_up, y_up - arrow_mod_cos_sub, y_up, y_up - arrow_mod_cos_add]
        # if negative
        else:
            xs_yq = [x_up, x_down, x_down - arrow_mod_sin_add, x_down, x_down + arrow_mod_cos_add]
            ys_yq = [y_up, y_down, y_down + arrow_mod_cos_add, y_down, y_down + arrow_mod_sin_add]
    else:
        xs_yq = []
        ys_yq = []

    # add element to datasource of line load arrows
    arrow_index = index_glyph * 2
    if create_element:
        # add arrow for x/ normal load
        curr_doc.data_sources.ds_arrow_lineload.data['xs'].append(xs_xn)
        curr_doc.data_sources.ds_arrow_lineload.data['ys'].append(ys_xn)
        curr_doc.data_sources.ds_arrow_lineload.data['name_user'].append(name)
        # add arrow for y/ shear load
        curr_doc.data_sources.ds_arrow_lineload.data['xs'].append(xs_yq)
        curr_doc.data_sources.ds_arrow_lineload.data['ys'].append(ys_yq)
        curr_doc.data_sources.ds_arrow_lineload.data['name_user'].append(name)
    else:
        # change arrow for x/ normal load
        curr_doc.data_sources.ds_arrow_lineload.data['xs'][arrow_index] = xs_xn
        curr_doc.data_sources.ds_arrow_lineload.data['ys'][arrow_index] = ys_xn
        # change arrow for y/ shear load
        curr_doc.data_sources.ds_arrow_lineload.data['xs'][arrow_index + 1] = xs_yq
        curr_doc.data_sources.ds_arrow_lineload.data['ys'][arrow_index + 1] = ys_yq
    curr_doc.data_sources.ds_arrow_lineload.trigger('data', curr_doc.data_sources.ds_arrow_lineload.data,
                                                    curr_doc.data_sources.ds_arrow_lineload.data)


def get_lineload_mod(distance, height, angle):
    """
    Calculates required modification of the position for the line load.
    :param distance: wanted distance between beam and line load glyph (double)
    :param height: height of the line load (double)
    :param angle: angle between the two nodes the line load is connected to (double)
    :return: needed x and y modification for x and y of the center between the two nodes (double)
    """
    x_mod = - (distance + height / 2) * math.sin(angle)
    y_mod = (distance + height / 2) * math.cos(angle)
    return x_mod, y_mod


def draw_moment_negative(curr_doc: CurrentDoc, name, index, negative):
    """
    Exchange image glyph with image glyph that depicts load_moment or spring_moment with a negative (if negative==True)
    or positive (if negative==False) value.
    :param name: name of the image glyph (string)
    :param index: index of the element in the ds_nodedep_elements data source (int)
    :param negative: whether the image glyoh should show a positive or negative depiction of the moment (bool)
    :return: none
    """
    enum_type = curr_doc.data_sources.ds_nodedep_elements.data['type'][index]

    if not(enum_type == eLnum.ElSupEnum.SPRING_MOMENT_SUPPORT.value or enum_type == eLnum.ElSupEnum.LOAD_MOMENT.value):
        return

    # mapped position in data source for image glyph
    if negative:
        ds_img_location = vis_elToP.map_enum2images[enum_type] + 1
    else:
        ds_img_location = vis_elToP.map_enum2images[enum_type]

    # get glyph and exchange url
    p = curr_doc.plot_input
    image_glyph = p.select(name=name)
    image_glyph[0].glyph.update(url=dict(value=curr_doc.data_sources.ds_images.data['url'][ds_img_location]))


def set_glyph_opacity(curr_doc: CurrentDoc, name_indep, alpha):
    """
    Set the opacity of the stated node independent glyph and all connected nodedependent glyphs.
    :param name_indep: name of the glyph of the input plot (string)
    :param alpha: alpha value to set (double)
    :return: none
    """
    # bokeh object: input plot
    p = curr_doc.plot_input

    nodedep = curr_doc.data_sources.ds_nodedep_elements
    nodedep_n1 = nodedep.data['name_node1']
    nodedep_n2 = nodedep.data['name_node2']
    nodedep_t = nodedep.data['type']
    nodedep_n = nodedep.data['name']

    # set opacity of image glyph for given name
    image_glyph = p.select(name=name_indep)
    image_glyph[0].glyph.update(global_alpha=alpha)

    # get connected nodedependent glyphs
    # TODO: draw beam/load opaque and draw glyphs opaque reliably with only one selected node
    for i in range(len(nodedep_n1)):
        if nodedep_n1[i] == name_indep or nodedep_n2[i] == name_indep:
            enum_type = nodedep_t[i]
            name = nodedep_n[i]
            if enum_type == eLnum.ElSupEnum.SPRING_SUPPORT.value or enum_type == eLnum.ElSupEnum.SPRING.value\
                    or enum_type == eLnum.ElSupEnum.SPRING_MOMENT_SUPPORT.value\
                    or enum_type == eLnum.ElSupEnum.LOAD_POINT.value or enum_type == eLnum.ElSupEnum.LOAD_MOMENT.value\
                    or enum_type == eLnum.ElSupEnum.LOAD_TEMP.value:
                image_glyph = p.select(name=name)
                image_glyph[0].glyph.update(global_alpha=alpha)
