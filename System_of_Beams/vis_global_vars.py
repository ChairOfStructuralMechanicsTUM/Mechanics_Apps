from Classes import DocElement as doc_el
from Classes import DataSources as dat_src
from Classes.OutputData import OutputVisu


def init(current_doc):
    global doc, DataSources, plot_data
    doc = doc_el.DocElement(current_doc)
    DataSources = dat_src.DataSources(current_doc)
    plot_data = OutputVisu(current_doc)
