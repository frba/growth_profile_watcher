import xml.etree.ElementTree as ET
from typing import Dict, Any, List
from pathlib import PureWindowsPath
import datetime, os
import pandas as pd
import numpy as np


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


def mantis_dispense(workunit: ET.Element, **kwargs: Dict[str, Any]) -> ET.Element:
    required_args = ['barcode', 'step', 'plate_type', 'dispense_list']
    for arg in required_args:
        if arg not in kwargs:
            raise ValueError(f"Missing required argument '{arg}' for process 'Generic Mantis'")
    usable_kwargs = ['barcode', 'step', 'plate_type', 'dispense_list', 'priority', 'iterations', 'minimumDelay']
    kwargs = {key: kwargs[key] for key in kwargs if key in usable_kwargs}
    batch = process_plate(workunit, 'Generic Mantis', **kwargs)
    # Get only File Name from the path in dispense_list
    create_variable(parent=batch,
                    var_type='String',
                    name='Mantis_Dispense_List',
                    value=kwargs['dispense_list'].split('\\')[-1])
    return batch


def write_file(workunit: ET.Element, **kwargs: Dict[str, Any]) -> ET.Element:
    required_args = ['barcode', 'step', 'FileName', 'FileContents']
    for arg in required_args:
        if arg not in kwargs:
            raise ValueError(f"Missing required argument '{arg}' for process 'Generic write file'")
    usable_kwargs = ['barcode', 'step', 'FileName', 'FileContents', 'priority', 'iterations', 'minimumDelay']
    kwargs = {key: kwargs[key] for key in kwargs if key in usable_kwargs}
    batch = process_plate(workunit, 'FileHandler2', **kwargs)
    create_variable(parent=batch,
                    var_type='String',
                    name='FileContents',
                    value=kwargs['FileContents'])
    create_variable(parent=batch,
                    var_type='String',
                    name='FileName',
                    value=kwargs['FileName'])
    return batch


def write_mantis_file(workunit: ET.Element, **kwargs: Dict[str, Any]) -> ET.Element:
    required_args = ['barcode', 'step', 'Mantis_filename', 'Mantis_dispenselist']
    for arg in required_args:
        if arg not in kwargs:
            raise ValueError(f"Missing required argument '{arg}' for process 'Generic write file'")
    usable_kwargs = ['barcode', 'step', 'Mantis_filename', 'Mantis_dispenselist', 'priority', 'iterations', 'minimumDelay']
    kwargs = {key: kwargs[key] for key in kwargs if key in usable_kwargs}
    kwargs['FileName'] = kwargs.pop('Mantis_filename')
    kwargs['FileContents'] = kwargs.pop('Mantis_dispenselist')
    batch = write_file(workunit, **kwargs)
    return batch


def create(plate_data, plate_info):
    """
    Create an empty XML structure for Momentum.
    :return: An ElementTree object representing the XML structure.
    """
    worklist = ET.Element("worklist")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    MANTIS_ROOT_PATH = PureWindowsPath('C:\\Mantis-0740\\Mantis-0740\\Mantis\\Data\\User\\DispenseList\\')
    MOMENTUM_ROOT_PATH = PureWindowsPath('C:\\Users\\Thermo\\Desktop\\Worklist Launcher\\')
    protocol = [write_mantis_file, mantis_dispense]

    # Get the integer from plate_info plare_type
    plate_type = plate_info[0]['plate_type']
    barcode = plate_info[0]['plate_id']
    plate_size = plate_info[0]['num_columns'] * plate_info[0]['num_rows']
    print(f"Plate Type: {plate_type}, Plate Size: {plate_size}")

    # Select the plate type for the Mantis dispense based on the plate type
    if plate_size == 96:
        mantis_plate_name = 'Eppendorf twin.tec PCR_96 on adapter'
    elif plate_size == 384:
        mantis_plate_name = 'Biorad 384 PCR on Adapter'
    else:
        mantis_plate_name = 'Mantis-Other'

    # Initialize the workunit
    workunit = initialize_workunit(worklist,
                                   name='Mantis-Workunit',
                                   append='false',
                                   auto_load='true',
                                   auto_verify_load='true',
                                   auto_unload='true',
                                   auto_verify_unload='true')
    # Create the batch
    batches = []

    # Create the Mantis dispense list
    plate_dimensions = (plate_info[0]['num_columns'], plate_info[0]['num_rows'])
    tsv_section = f"1\n"
    tsv_section += f"Water\t\t1 cP\nWell\t1\n"
    reagent_values = np.full(plate_dimensions, 2).flatten()
    numeric_values = np.asarray(reagent_values).reshape(*plate_dimensions)
    numeric_values = pd.DataFrame(numeric_values.round(1))
    numeric_tsv = pd.DataFrame(numeric_values).to_csv(index=False, header=False, sep='\t')
    tsv_section += numeric_tsv

    print(f"Creating Mantis dispense list")
    print(tsv_section)

    input_file_content = f"[ Version: 6 ]\n{mantis_plate_name}.pd.txt\n0\n1\n2\t0\t\t0\t\n"
    input_file_content += "".join(tsv_section)
    mantis_tsv_text = input_file_content.replace('\n', '\r\n')
    operation_name_stem = f'{barcode}-{timestamp}'
    mantis_filename = f'{operation_name_stem}.dl.txt'

    print(mantis_filename)

    kwargs = {
        'barcode': barcode,
        'plate_type': str(plate_size) + 'PCR',
        # 'ODTC_protocol': str(ODTC_protocol),
        'dispense_list': mantis_filename,
        # 'transfer_file': str(ECHO_ROOT_PATH.joinpath(echo_filename)),
        'Mantis_filename': str(MANTIS_ROOT_PATH.joinpath(mantis_filename)),
        'Mantis_dispenselist': mantis_tsv_text,
        # 'Echo_filename': str(ECHO_ROOT_PATH.joinpath(echo_filename)),
        # 'Echo_worklist': echo_worklist.to_csv(index=False),
        # 'Source_Plate_Type': source_plate_type
    }

    for step, process in enumerate(protocol, start=1):
        batches.append(process(workunit, step=str(step), **kwargs))
    tree = ET.ElementTree(worklist)
    ET.indent(tree, space=" ", level=0)  # For pretty printing
    # tree.write('output.xml', encoding='utf-8', xml_declaration=True)

    # Save the XML to a file
    # To print the XML string
    xml_str = ET.tostring(worklist, encoding='unicode', method='xml')
    xml_path = f'{barcode}.xml'
    # with open(os.path.join(MOMENTUM_ROOT_PATH, xml_path), "w") as f:
    with open(os.path.join(xml_path), "w") as f:
        f.write(xml_str)
    print(f"XML file created: {xml_path}")