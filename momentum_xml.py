import xml.etree.ElementTree as ET
from typing import Dict, Any, List
import datetime, os
from pathlib import PureWindowsPath


def initialize_workunit(worklist, name, append, auto_load, auto_verify_load, auto_unload, auto_verify_unload):
    """
    Initiates a workunit.

    Keyword Arguments:
    worklist -- The parent XML element.
    name -- The name of the workunit (str).
    append -- Whether to append to an existing workunit (str, default 'false').

    """
    workunit = ET.SubElement(worklist, 'workunit')
    usable_kwargs = [name, append, auto_load, auto_verify_load, auto_unload, auto_verify_unload]
    kwargs = {key: value for key, value in zip(['name', 'append', 'auto_load', 'auto_verify_load', 'auto_unload', 'auto_verify_unload'], usable_kwargs)}
    for key, value in kwargs.items():
        workunit.set(key, value)
    return workunit


def create_batch(parent: ET.Element, process: str, name: str, priority: str, iterations: str, minimumDelay: str, reference: str, constraint: str) -> ET.Element:
    batch = ET.SubElement(parent, 'batch', {
        'process': process,
        'name': name,
        'priority': priority,
        'iterations': iterations,
        'minimumDelay': minimumDelay,
        'reference': reference,
        'constraint': constraint
    })
    return batch


def create_variable(parent: ET.Element, var_type: str, name: str, value: str) -> None:
    variable = ET.SubElement(parent, 'variable', {
        'type': var_type,
        'name': name
    })
    variable.text = value
    # Does this work for non-string variable types?


# Define required arguments for each process
def process_plate(workunit: ET.Element, process: str, **kwargs: Dict[str, Any]) -> ET.Element:
    """
    General function to create a plate batch.

    Keyword Arguments:
    workunit -- The parent XML element.
    process -- The process type (str).
    barcode -- The barcode of the plate (str).
    step -- The step number (str).
    plate_type -- The type of the plate (str).
    priority -- The priority of the batch (str, default '10').
    iterations -- The number of iterations (str, default '1').
    minimumDelay -- The minimum delay (str, default '0').
    ODTC_protocol -- The pathname for the ODTC process (str, optional).
    """

    barcode = kwargs.get('barcode')
    step = kwargs.get('step')
    plate_type = kwargs.get('plate_type')
    priority = kwargs.get('priority', '10')
    iterations = kwargs.get('iterations', '1')
    minimumDelay = kwargs.get('minimumDelay', '0')

    if step == '1':
        reference = 'None'
        start_condition = 'ASAP'
    else:
        reference = f'{barcode}-{int(step)-1}'
        start_condition = 'SF'

    batch = create_batch(workunit, process, f'{barcode}-{step}', priority, iterations, minimumDelay, reference, start_condition)
    if barcode:
        create_variable(batch, 'String', 'Barcode', barcode)
    if plate_type:
        create_variable(batch, 'String', 'Plate_Type', plate_type)
    return batch


def write_file(workunit: ET.Element, **kwargs: Dict[str, Any]) -> ET.Element:
    usable_kwargs = ['barcode', 'step', 'FileName', 'FileContents', 'priority', 'iterations', 'minimumDelay']
    kwargs = {key: kwargs[key] for key in kwargs if key in usable_kwargs}
    # Using 'Induction' as the process name
    batch = process_plate(workunit, 'Test_GP_watcher', **kwargs)
    return batch


def create(plate_data, plate_info):
    """
    Create an XML structure for Momentum.
    :param plate_data: List of dictionaries containing plate growth data.
    :param plate_info: List of dictionaries containing plate_type, plate_id, num_rows, and num_columns.
    :return: An ElementTree object representing the XML structure.

    """
    worklist = ET.Element("worklist")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    MOMENTUM_ROOT_PATH = PureWindowsPath('C:\\Users\\Thermo\\Desktop\\Worklist Launcher\\')
    # MOMENTUM_ROOT_PATH = ('/Users/flavia/PycharmProjects/growth_profile_watcher/output/')
    protocol = [write_file]

    # Get the integer from plate_info plare_type
    plate_type = plate_info[0]['plate_type']
    barcode = plate_info[0]['plate_id']
    plate_size = plate_info[0]['num_columns'] * plate_info[0]['num_rows']

    # Initialize the workunit
    workunit = initialize_workunit(worklist,
                                   name='Induction-Workunit',
                                   append='false',
                                   auto_load='true',
                                   auto_verify_load='true',
                                   auto_unload='true',
                                   auto_verify_unload='true')
    # Create the batch
    batches = []

    kwargs = {
        'barcode': barcode,
        'plate_size': plate_size,
        'plate_type': plate_type,
    }

    for step, process in enumerate(protocol, start=1):
        batches.append(process(workunit, step=str(step), **kwargs))
    tree = ET.ElementTree(worklist)
    ET.indent(tree, space=" ", level=0)  # For pretty printing

    # Save the XML to a file
    xml_str = ET.tostring(worklist, encoding='unicode', method='xml')

    ### --- Path to save the XML file --- ###
    xml_path = f'{barcode}.xml'
    with open(os.path.join(MOMENTUM_ROOT_PATH, xml_path), "w") as f:
        f.write(xml_str)