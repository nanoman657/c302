import sys
import os
from pyneuroml import pynml
import matplotlib.pyplot as plt
import numpy as np

import c302


def generate_c302_info(nml_doc, verbose=False):
    net = nml_doc.networks[0]

    cc_exc_conns = {}
    cc_inh_conns = {}
    all_cells = []

    for cp in net.continuous_projections:
        if not cp.presynaptic_population in cc_exc_conns.keys():
            cc_exc_conns[cp.presynaptic_population] = {}
        if not cp.presynaptic_population in cc_inh_conns.keys():
            cc_inh_conns[cp.presynaptic_population] = {}

        if not cp.presynaptic_population in all_cells:
            all_cells.append(cp.presynaptic_population)
        if not cp.postsynaptic_population in all_cells:
            all_cells.append(cp.postsynaptic_population)

        for c in cp.continuous_connection_instance_ws:
            if "inh" in c.post_component:
                cc_inh_conns[cp.presynaptic_population][cp.postsynaptic_population] = (
                    float(c.weight)
                )
            else:
                cc_exc_conns[cp.presynaptic_population][cp.postsynaptic_population] = (
                    float(c.weight)
                )

    gj_conns = {}
    for ep in net.electrical_projections:
        if not ep.presynaptic_population in gj_conns.keys():
            gj_conns[ep.presynaptic_population] = {}

        if not ep.presynaptic_population in all_cells:
            all_cells.append(ep.presynaptic_population)
        if not ep.postsynaptic_population in all_cells:
            all_cells.append(ep.postsynaptic_population)

        for e in ep.electrical_connection_instance_ws:
            gj_conns[ep.presynaptic_population][ep.postsynaptic_population] = float(
                e.weight
            )

    all_cells = sorted(all_cells)

    all_neuron_info, all_muscle_info = c302._get_cell_info(all_cells)

    all_neurons = []
    all_muscles = []
    for c in all_cells:
        if c302.is_muscle(c):
            all_muscles.append(c)
        else:
            all_neurons.append(c)

    info = "# Information on neuron and muscles\n"
    info += "## Generated using c302 v%s\n" % c302.__version__

    info += "### Neurons (%i)\n" % (len(all_neuron_info))
    info += "<table>\n"
    for n in all_neuron_info:
        info += "<tr>\n"
        ni = all_neuron_info[n]
        # print(ni)
        info += (
            "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>Colour: %s</td>"
            % (n, _info_set(ni[1]), _info_set(ni[2]), _info_set(ni[3]), ni[4], ni[5])
        )
        info += "</tr>\n"
    info += "</table>\n"

    info += "### Muscles (%i)\n" % (len(all_muscle_info))
    info += "<table>\n"
    for n in all_muscle_info:
        info += "<tr>\n"
        ni = all_muscle_info[n]
        info += (
            "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>Colour: %s</td>"
            % (n, _info_set(ni[1]), _info_set(ni[2]), _info_set(ni[3]), ni[4], ni[5])
        )
        info += "</tr>\n"
    info += "</table>\n"

    with open("examples/summary/summary.md", "w") as f2:
        # f2.write('<html><body>%s</body></html>'%info)
        f2.write("%s" % info)


def _info_set(s):
    s = sorted(s)
    return ", ".join(["%s" % i for i in s])


if __name__ == "__main__":
    from neuroml.loaders import read_neuroml2_file

    config = "c302_C0_Full.net.nml"

    nml_doc = read_neuroml2_file("examples/%s" % config)

    generate_c302_info(nml_doc)
