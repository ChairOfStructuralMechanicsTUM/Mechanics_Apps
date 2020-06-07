

import numpy as np
import math

# import bokeh modules
from bokeh.models.glyphs import ImageURL

# import local files
import vis_callbacks as vis_cbs
import vis_editElement as vis_editEl
from Classes import ElementSupportEnum as eLnum
from Classes.ColumnDataSources import ColumnDataSources
from Classes.CurrentDocument import CurrentDoc

map_enum2images = {eLnum.ElSupEnum.SUPPORT_CLAMPED.value: 0, eLnum.ElSupEnum.SUPPORT_NORMAL_FORCE.value: 1,
                   eLnum.ElSupEnum.SUPPORT_TRANSVERSE_FORCE.value: 2, eLnum.ElSupEnum.SUPPORT_FIXED_CONTINUOUS.value: 3,
                   eLnum.ElSupEnum.SUPPORT_FIXED_JOINT.value: 4, eLnum.ElSupEnum.SUPPORT_ROLLER_CONTINUOUS.value: 5,
                   eLnum.ElSupEnum.SUPPORT_ROLLER_JOINT.value: 6, eLnum.ElSupEnum.SPRING_SUPPORT.value: 7,
                   eLnum.ElSupEnum.SPRING_MOMENT_SUPPORT.value: 8,  # spring_moment_support_negativ
                   eLnum.ElSupEnum.NODE.value: 10, eLnum.ElSupEnum.JOINT.value: 11,
                   eLnum.ElSupEnum.JOINT_NORMAL_FORCE.value: 12, eLnum.ElSupEnum.JOINT_TRANSVERSE_FORCE.value: 13,
                   eLnum.ElSupEnum.SPRING.value: 14, eLnum.ElSupEnum.LOAD_POINT.value: 15,
                   eLnum.ElSupEnum.LOAD_MOMENT.value: 16,  # load_moment_negative
                   eLnum.ElSupEnum.LOAD_TEMP.value: 18}
# ds_images = ColumnDataSources.ds_images


def add_indep(curr_doc: CurrentDoc, x, y, enum_type, name, angle=0.0):
    """
    Add node independent element to the input plot.
    :param x: x value of node (double)
    :param y: y value of node (double)
    :param enum_type: enum_type of element (double of ElementSupportEnum)
    :param name: name of element (string)
    :param angle: angle of the element to the x axis (double)
    :return: none
    """
    indep = curr_doc.data_sources.ds_indep_elements
    indep_x = indep.data['x']
    indep_y = indep.data['y']
    indep_t = indep.data['type']
    indep_n = indep.data['name']
    indep_s = indep.data['same']
    indep_a = indep.data['angle']

    ds_img_location = map_enum2images[enum_type]

    # add entry to ds_plot_independent_elements
    indep_x.append(x)
    indep_y.append(y)
    indep_t.append(enum_type)
    indep_n.append(name)
    indep_s.append(False)
    indep_a.append(angle)

    # add image glyph to plot and display information
    p = curr_doc.plot_input
    image = ImageURL(url=dict(value=curr_doc.data_sources.ds_images.data['url'][ds_img_location]),
                     x=x + curr_doc.data_sources.ds_images.data['x_mod'][ds_img_location], y=y + curr_doc.data_sources.ds_images.data['y_mod'][ds_img_location],
                     w=curr_doc.data_sources.ds_images.data['w'][ds_img_location], h=curr_doc.data_sources.ds_images.data['h'][ds_img_location],
                     anchor="center")
    p.add_glyph(curr_doc.data_sources.ds_glyph_images, image, name=name)

    # change angle of image glyph if non-zero
    if angle:
        vis_editEl.change_angle_indep(curr_doc, name, angle=angle, index=len(indep_a)-1)

    # notify user that the new object was created
    curr_doc.div_input.text = "Object " + str(name) + " created at: (" + str(x) + "," + str(y) + ")"

    # show element info of the added element in element info box if not test case
    if not curr_doc.plotting_test_case:
        vis_cbs.cb_show_element_info(0, 0, 0, curr_doc, indep=True)


def add_nodedep(curr_doc: CurrentDoc, enum_type, x, y, length=0.0, angle=0.0,
                dt_t=(1.0, 0.0, 1.0), k=1.0, h=1.0, ei=1.0, ea=1.0, moment=1.0, f=1.0,
                ll_local=True, ll_x_n=(0.0, 0.0), ll_y_q=(-1.0, -1.0)):
    """
    Add a node dependent element to the ds_plot_nodedep_elements datasource and a corresponding image glyth to the
    input plot.
    :param enum_type: type of element to add (double - ElementSupportEnum)
    :param x: x position of center of the element or node if only dependent on one node (double)
    :param y: y position of the center of the element or node if only dependent on one node (double)
    :param length: length of the element (double)
    :param angle: angle of the element to the x-axis or y-axis (point load)
    :param dt_t: defines factors of a temperature load Tupel(dT, T, aT)
    :param k: factor of spring constant (double)
    :param h: factor of cross section height (double)
    :param ei: factor of EI of the beam (double)
    :param ea: factor of EA of the beam (double)
    :param moment: factor of moment load (double)
    :param f: fator of point load (double)
    :param ll_local: whether line load is defined locally or globally (bool)
    :param ll_x_n: start and end values of the line load in x or normal direction (Tuple)
    :param ll_y_q: start and end values of the line load in y or shear direction (Tuple)
    :return:
    """
    # datasource for nodedependent elements
    nodedep = curr_doc.data_sources.ds_nodedep_elements

    # bokeh object: input plot
    p = curr_doc.plot_input

    name = str(enum_type) + "-" + str(curr_doc.object_id)
    curr_doc.object_id += 1

    # name_node1 and name_node2 already added in vis_cbs.cb_adapt_plot_nodedep()
    nodedep.data['type'].append(enum_type)
    nodedep.data['name'].append(name)
    nodedep.data['x'].append(x)
    nodedep.data['y'].append(y)
    nodedep.data['angle'].append(angle)

    nodedep_l = nodedep.data['length']
    nodedep_dt = nodedep.data['dT_T']
    nodedep_k = nodedep.data['k']
    nodedep_h = nodedep.data['h']
    nodedep_ei = nodedep.data['ei']
    nodedep_ea = nodedep.data['ea']
    nodedep_m = nodedep.data['moment']
    nodedep_f = nodedep.data['f']
    nodedep_lll = nodedep.data['ll_local']
    nodedep_llxn = nodedep.data['ll_x_n']
    nodedep_llyq = nodedep.data['ll_y_q']

    # append values to all dict entries and adapt with index
    nodedep_l.append(False)
    nodedep_dt.append(False)
    nodedep_k.append(False)
    nodedep_h.append(False)
    nodedep_ei.append(False)
    nodedep_ea.append(False)
    nodedep_m.append(False)
    nodedep_f.append(False)
    nodedep_lll.append(False)
    nodedep_llxn.append(False)
    nodedep_llyq.append(False)

    index = len(nodedep_l) - 1

    # settings and image glyphs for spring_support, spring_moment_support, spring
    if enum_type == eLnum.ElSupEnum.SPRING_SUPPORT.value or enum_type == eLnum.ElSupEnum.SPRING_MOMENT_SUPPORT.value \
            or enum_type == eLnum.ElSupEnum.SPRING.value:
        nodedep_k[index] = k
        # mapped position in data source for image glyph
        ds_img_location = map_enum2images[enum_type]
        # add element to datasource of nodedep image glyph info
        ds_glyph = curr_doc.data_sources.ds_glyph_springsPointMomentTemp
        ds_glyph.data['glyph_x'].append(x + curr_doc.data_sources.ds_images.data['x_mod'][ds_img_location] * 1.5)
        ds_glyph.data['glyph_y'].append(y + curr_doc.data_sources.ds_images.data['y_mod'][ds_img_location] * 1.5)
        ds_glyph.data['x'].append(x)
        ds_glyph.data['y'].append(y)
        ds_glyph.data['name_user'].append(name)
        ds_glyph.trigger('data', ds_glyph.data, ds_glyph.data)
        # create image glyph
        if enum_type == eLnum.ElSupEnum.SPRING.value:
            nodedep_l[index] = length
            length += 0.1
            # adapt position because of weird displacement through angle
            x_mod = - angle / 15.7
            y_mod = - abs(angle) / 15.7
            x_mod = x_mod - length / 2 * math.cos(angle)
            y_mod = y_mod - length / 2 * math.sin(angle)
            image = ImageURL(url=dict(value=curr_doc.data_sources.ds_images.data['url'][ds_img_location]),
                             x=x + x_mod, y=y + y_mod, w=length, h=curr_doc.data_sources.ds_images.data['h'][ds_img_location],
                             anchor="center_left", angle=angle)
        else:
            image = ImageURL(url=dict(value=curr_doc.data_sources.ds_images.data['url'][ds_img_location]),
                             x=x + curr_doc.data_sources.ds_images.data['x_mod'][ds_img_location],
                             y=y + curr_doc.data_sources.ds_images.data['y_mod'][ds_img_location], w=curr_doc.data_sources.ds_images.data['w'][ds_img_location],
                             h=curr_doc.data_sources.ds_images.data['h'][ds_img_location], anchor="center", angle=0.0)
            # add image glyph to plot
        p.add_glyph(curr_doc.data_sources.ds_glyph_images, image, name=name)
        # adapt angle of image glyph at one node if angle given
        if angle and not enum_type == eLnum.ElSupEnum.SPRING.value:
            vis_editEl.change_angle_nodedep(curr_doc, name, angle, index=index, index_glyph=len(ds_glyph.data['x']) - 1)
        # adapt image glyph of moment if it depicts a negative value
        if k < 0 and enum_type == eLnum.ElSupEnum.SPRING_MOMENT_SUPPORT.value:
            vis_editEl.draw_moment_negative(curr_doc, name, index, negative=True)

    # settings and image glyphs for moment, point load, temperature load
    elif enum_type == eLnum.ElSupEnum.LOAD_POINT.value or enum_type == eLnum.ElSupEnum.LOAD_MOMENT.value \
            or enum_type == eLnum.ElSupEnum.LOAD_TEMP.value:
        ds_glyph = curr_doc.data_sources.ds_glyph_springsPointMomentTemp
        ds_img_location = map_enum2images[enum_type]
        # create and add image glyph to plot
        image = ImageURL(url=dict(value=curr_doc.data_sources.ds_images.data['url'][ds_img_location]),
                         x=x + curr_doc.data_sources.ds_images.data['x_mod'][ds_img_location], y=y + curr_doc.data_sources.ds_images.data['y_mod'][ds_img_location],
                         w=curr_doc.data_sources.ds_images.data['w'][ds_img_location], h=curr_doc.data_sources.ds_images.data['h'][ds_img_location],
                         anchor="center", angle=0.0)
        p.add_glyph(curr_doc.data_sources.ds_glyph_images, image, name=name)
        # adapt ds_nodedep_element and image glyphs based on the input
        # also adapt glyph position for load_point and load_moment to make both selectable
        if enum_type == eLnum.ElSupEnum.LOAD_POINT.value:
            nodedep_f[index] = f
            ds_glyph.data['glyph_x'].append(x + curr_doc.data_sources.ds_images.data['x_mod'][ds_img_location] * 1.5)
            ds_glyph.data['glyph_y'].append(y + curr_doc.data_sources.ds_images.data['y_mod'][ds_img_location] * 1.5)
        elif enum_type == eLnum.ElSupEnum.LOAD_MOMENT.value:
            nodedep_m[index] = moment
            ds_glyph.data['glyph_x'].append(x + curr_doc.data_sources.ds_images.data['x_mod'][ds_img_location] - 0.1)
            ds_glyph.data['glyph_y'].append(y + curr_doc.data_sources.ds_images.data['y_mod'][ds_img_location])
            # adapt image glyph of moment if it depicts a negative value
            if moment < 0:
                vis_editEl.draw_moment_negative(curr_doc, name, index, negative=True)
        else:
            nodedep_dt[index] = dt_t
            ds_glyph.data['glyph_x'].append(x + curr_doc.data_sources.ds_images.data['x_mod'][ds_img_location])
            ds_glyph.data['glyph_y'].append(y + curr_doc.data_sources.ds_images.data['y_mod'][ds_img_location])

        # add element to datasource of nodedep image glyph info
        ds_glyph.data['x'].append(x)
        ds_glyph.data['y'].append(y)
        ds_glyph.data['name_user'].append(name)
        ds_glyph.trigger('data', ds_glyph.data, ds_glyph.data)
        # adapt angle of image glyph at one node if angle given
        if angle and enum_type == eLnum.ElSupEnum.LOAD_POINT.value:
            vis_editEl.change_angle_nodedep(curr_doc, name, angle, index=index, index_glyph=len(ds_glyph.data['x']) - 1)

    # settings and non-image glyphs for beam
    elif enum_type == eLnum.ElSupEnum.BEAM.value:
        nodedep_l[index] = length
        nodedep_h[index] = h
        nodedep_ei[index] = ei
        nodedep_ea[index] = ea

        # create glyph
        curr_doc.data_sources.ds_glyph_beam.data['x'].append(x)
        curr_doc.data_sources.ds_glyph_beam.data['y'].append(y)
        curr_doc.data_sources.ds_glyph_beam.data['width'].append(length)
        curr_doc.data_sources.ds_glyph_beam.data['angle'].append(angle)
        curr_doc.data_sources.ds_glyph_beam.data['name_user'].append(name)
        curr_doc.data_sources.ds_glyph_beam.trigger('data', curr_doc.data_sources.ds_glyph_beam.data, curr_doc.data_sources.ds_glyph_beam.data)

    # settings and non-image glyph for line load
    else:
        nodedep_l[index] = length
        nodedep_lll[index] = ll_local
        nodedep_llxn[index] = ll_x_n
        nodedep_llyq[index] = ll_y_q
        # create glyph and add element to datasource of line load info
        vis_editEl.draw_lineload(curr_doc, name, load_x_n=nodedep_llxn[index], load_y_q=nodedep_llyq[index],
                                 local=nodedep_lll[index], index=index, create_element=True)

    # notify user that the new object was created
    curr_doc.div_input.text = "Object " + str(name) + " created."

    # show element info of the added element in element info box if not a test case
    if not curr_doc.plotting_test_case:
        vis_cbs.cb_show_element_info(0, 0, 0, curr_doc, nodedep=True)


def delete_indep(curr_doc: CurrentDoc, name, index=False):
    """
    Delete a node independent element from the data source and the input plot.
    :param name: name of the node independent element that has to be deleted (string)
    :param index: index in the node independent data source for that element (int)
    :return: none
    """
    indep = curr_doc.data_sources.ds_indep_elements
    indep_x = indep.data['x']
    indep_y = indep.data['y']
    indep_t = indep.data['type']
    indep_n = indep.data['name']
    indep_s = indep.data['same']
    indep_a = indep.data['angle']

    # search for element in data source if index was not given
    if type(index) == bool:
        for i in range(len(indep_n)):
            if name == indep_n[i]:
                index = i
                break

    # delete connected node dependent elements
    delete_nodedep(curr_doc, name)

    # delete corresponding glyph in input plot
    p = curr_doc.plot_input
    image_glyph = p.select(name=indep_n[index])
    p.renderers.remove(image_glyph[0])
    del indep_x[index]
    del indep_y[index]
    del indep_t[index]
    del indep_n[index]
    del indep_s[index]
    del indep_a[index]

    # trigger data source changed and reduce count of plot elements
    indep.trigger('data', indep.data, indep.data)
    curr_doc.data_sources.ds_element_count.data['count'][0] -= 1
    curr_doc.data_sources.ds_element_count.trigger('data', curr_doc.data_sources.ds_element_count.data, curr_doc.data_sources.ds_element_count.data)


def delete_nodedep(curr_doc: CurrentDoc, name_indep=False, name_nodedep=False, index_nodedep=False):
    """
    Delete nodedependent element glyphs that are connected to a node with the name "name_indep".
    :param name_indep: name of the node independent element that was deleted (string)
    :param name_nodedep: name of the node dependent element that shall be deleted (string)
    :param index_nodedep: index of the node dependent element (int)
    :return: none
    """
    if not name_indep and not name_nodedep:
        return

    # bokeh object: input plot
    p = curr_doc.plot_input

    nodedep = curr_doc.data_sources.ds_nodedep_elements
    nodedep_n1 = nodedep.data['name_node1']
    nodedep_n2 = nodedep.data['name_node2']
    nodedep_t = nodedep.data['type']
    nodedep_n = nodedep.data['name']
    nodedep_x = nodedep.data['x']
    nodedep_y = nodedep.data['y']
    nodedep_l = nodedep.data['length']
    nodedep_dt = nodedep.data['dT_T']
    nodedep_k = nodedep.data['k']
    nodedep_h = nodedep.data['h']
    nodedep_ei = nodedep.data['ei']
    nodedep_ea = nodedep.data['ea']
    nodedep_m = nodedep.data['moment']
    nodedep_f = nodedep.data['f']
    nodedep_lll = nodedep.data['ll_local']
    nodedep_llxn = nodedep.data['ll_x_n']
    nodedep_llyq = nodedep.data['ll_y_q']
    nodedep_a = nodedep.data['angle']

    # delete complete node dependent element, when any of its nodes was deleted (cb_adapt_plot_indep)
    indices = []

    # find node dependent elements that were connected to the independent element that was deleted
    if name_indep:
        for i in range(len(nodedep_n1)):
            if nodedep_n1[i] == name_indep or nodedep_n2[i] == name_indep:
                indices.append(i)

    if name_nodedep:
        if type(index_nodedep) == bool:
            for i in range(len(curr_doc.data_sources.ds_nodedep_elements.data['name'])):
                if curr_doc.data_sources.ds_nodedep_elements.data['name'][i] == name_nodedep:
                    index_nodedep = i
                    break
            else:
                return
        indices.append(index_nodedep)

    # delete elements of list indices, use reversed() so indices don't change through already deleted elements
    for i in reversed(indices):
        enum_type = nodedep_t[i]
        name = nodedep_n[i]
        glyph_index = -1

        if enum_type == eLnum.ElSupEnum.BEAM.value:
            ds_glyph = curr_doc.data_sources.ds_glyph_beam
            # find element in tooltips and element info data source
            for j in range(len(ds_glyph.data['name_user'])):
                if name == ds_glyph.data['name_user'][j]:
                    glyph_index = j
                    break
            # delete entry
            if not glyph_index == -1:
                del ds_glyph.data['x'][glyph_index]
                del ds_glyph.data['y'][glyph_index]
                del ds_glyph.data['width'][glyph_index]
                del ds_glyph.data['angle'][glyph_index]
                del ds_glyph.data['name_user'][glyph_index]

        elif enum_type == eLnum.ElSupEnum.LOAD_LINE.value:
            ds_glyph = curr_doc.data_sources.ds_glyph_lineload
            # find element in glyph and info data source
            for j in range(len(ds_glyph.data['name_user'])):
                if name == ds_glyph.data['name_user'][j]:
                    glyph_index = j
                    break
            # delete entry
            if not glyph_index == -1:
                del ds_glyph.data['patch_x'][glyph_index]
                del ds_glyph.data['patch_y'][glyph_index]
                del ds_glyph.data['glyph_x'][glyph_index]
                del ds_glyph.data['glyph_y'][glyph_index]
                del ds_glyph.data['x'][glyph_index]
                del ds_glyph.data['y'][glyph_index]
                del ds_glyph.data['name_user'][glyph_index]

            # delete entry for y/ normal load and afterwards for y/ shear load
            ds_arrow = curr_doc.data_sources.ds_arrow_lineload
            arrow_index = glyph_index * 2
            if not glyph_index == -1:
                del ds_arrow.data['xs'][arrow_index]
                del ds_arrow.data['ys'][arrow_index]
                del ds_arrow.data['name_user'][arrow_index]
                del ds_arrow.data['xs'][arrow_index]
                del ds_arrow.data['ys'][arrow_index]
                del ds_arrow.data['name_user'][arrow_index]
                ds_arrow.trigger('data', ds_arrow.data, ds_arrow.data)

        else:
            ds_glyph = curr_doc.data_sources.ds_glyph_springsPointMomentTemp
            # find element in tooltips and element info data source
            for j in range(len(ds_glyph.data['name_user'])):
                if name == ds_glyph.data['name_user'][j]:
                    glyph_index = j
                    break
            # delete entry
            if not glyph_index == -1:
                del ds_glyph.data['glyph_x'][glyph_index]
                del ds_glyph.data['glyph_y'][glyph_index]
                del ds_glyph.data['x'][glyph_index]
                del ds_glyph.data['y'][glyph_index]
                del ds_glyph.data['name_user'][glyph_index]
            # delete image glyph
            image_glyph = p.select(name=name)
            p.renderers.remove(image_glyph[0])

        ds_glyph.trigger('data', ds_glyph.data, ds_glyph.data)

        # delete entry in node dependent element data source
        del nodedep_n1[i]
        del nodedep_n2[i]
        del nodedep_t[i]
        del nodedep_n[i]
        del nodedep_x[i]
        del nodedep_y[i]
        del nodedep_l[i]
        del nodedep_dt[i]
        del nodedep_k[i]
        del nodedep_h[i]
        del nodedep_ei[i]
        del nodedep_ea[i]
        del nodedep_m[i]
        del nodedep_f[i]
        del nodedep_lll[i]
        del nodedep_llxn[i]
        del nodedep_llyq[i]
        del nodedep_a[i]

    nodedep.trigger('data', nodedep.data, nodedep.data)


def get_1st2nd_center_length_angle(node1_x, node1_y, node2_x, node2_y):
    """
    Calculates for two given nodes which one is the left/lower one, the distance between them and their angle to the
    x axis, if connected by a line.
    :param node1_x: x value of first given node (double)
    :param node1_y: y value of first given node (double)
    :param node2_x: x value of second given node (double)
    :param node2_y: y value of second given node (double)
    :return: left/lower node as 1st node (Tuple), right/upper node as 2nd node (Tuple), x and y of center (Tuple),
    distance between the nodes (double), angle between nodes and x axis (double)
    """
    # calculate dx and dy and the center between the two nodes
    dx = node2_x - node1_x
    dy = node2_y - node1_y
    center_x = node1_x + dx / 2
    center_y = node1_y + dy / 2
    center = (center_x, center_y)

    # calculate distance between both nodes
    length = np.sqrt(dx ** 2 + dy ** 2)

    # calculate angle to x axis
    # get left/lower and right/upper chosen node
    if dx == 0:
        angle = 1.57
        if dy < 0:
            left_lower = (node2_x, node2_y)
            right_upper = (node1_x, node1_y)
        else:
            left_lower = (node1_x, node1_y)
            right_upper = (node2_x, node2_y)
    elif dx <= 0:
        angle = math.acos(abs(dx) / length)
        if dy > 0:
            angle = -angle
        left_lower = (node2_x, node2_y)
        right_upper = (node1_x, node1_y)
    else:
        angle = math.acos(dx / length)
        if dy < 0:
            angle = -angle
        left_lower = (node1_x, node1_y)
        right_upper = (node2_x, node2_y)

    return left_lower, right_upper, center, length, angle
