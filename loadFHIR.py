# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 20:10:26 2019

@author: andyp
"""
import pandas as pd
import glob
import resources as rs
import hashlib
import fhirclient.models as fhirModel
from fhirclient import client
from faker import Faker
        
#def db_connect():
#    pguser = os.getenv('PGUSER', 'postgres')
#    pgpassword = os.getenv('PGPASSWORD', 'megawish')
#    pghost = os.getenv('PGHOST', 'localhost')
#    pgport = os.getenv('PGPORT', '5432')
#    dbname = os.getenv('PGDATABASE', 'fhirbase')
#
#    return psycopg2.connect(dbname=dbname, user=pguser,
#                            password=pgpassword, host=pghost, port=pgport)    

def create_identifier(ventMap_id, pt_id, breath_number):
    combined_id = ":".join([pt_id, ventMap_id, str(breath_number)])
    combined_byte_id = combined_id.encode('utf-8')
    return hashlib.md5(combined_byte_id).hexdigest()
    
def process_metadata(metadata, pt_id, vent_map):
    # Array of breath information
    breath_observations = []
    
    # Breath time arrays
    breath_start = []
    breath_end = []
    insp_breath_end = []
    insp_breath_interval = []
    exp_breath_interval = []
    
    # Ratios
    ie_ratio = []
    
    # Rates
    inst_rr = []
    
    # Tidal Volume
    tve = []
    tvi = []
    
    # Flow
    maxF = []
    minF = []
    
    # Pressure
    maxP = []
    pip = []
    maw = []
    peep = []
    minP = []
    system = 'urn:iso:std:iso:11073:10101'
    for rows in metadata.itertuples():
        breath_start = fhirModel.observation.Observation({'id': create_identifier("bs_time", pt_id, rows.ventBN), 
                                        'code': {'coding': [{"system": system, 
                                                             "code": str(vent_map.loc['bs_time', 'code']), 
                                                             "display": vent_map.loc['bs_time', 'display']}]},
                                        'status': 'final',
                                        vent_map.loc['bs_time', 'valueType']: {'value': float(rows.BS), 'unit':vent_map.loc['bs_time', 'unit']}
                                        })
        #breath_start = rs.Observation(identifier = create_identifier("bs_time", pt_id, rows.ventBN), text=vent_map.loc['bs_time', 'text'], code=vent_map.loc['bs_time', 'code'], display=vent_map.loc['bs_time', 'display'], valueType=vent_map.loc['bs_time', 'valueType'], value = float(rows.BS), breath_number=int(rows.ventBN), patientRef = {"reference": "/".join(["Patient", pt_id]), "type": "Patient"}, unit=vent_map.loc['bs_time', 'unit'])
        #breath_observations.append([breath_start])
        print(breath_start.as_json())
    return breath_observations
#    breath_end = rs.Observation(identifier = "be_time", text="The time this breath finished", code=67985, display="MDC_ATTR_TIME_STAMP_REL", valueType="valueQuantity", value = float(rows.BE), breath_number=int(rows.ventBN), unit="s")
#    insp_breath_end = rs.Observation(identifier = "i_end_time",  text="The time the inspiratory breath finished", code=67985, display="MDC_ATTR_TIME_STAMP_REL", valueType="valueQuantity", value = float(rows.IEnd), breath_number=int(rows.ventBN), unit="s")
#    insp_breath_interval = rs.Observation(identifier = "i_time",  text="The time interval for an inspiratory breath", code=152608, display="MDC_ATTR_TIME_STAMP_REL", valueType="valueQuantity", value = float(rows.iTime), breath_number=int(rows.ventBN), unit="s")
#    exp_breath_interval = rs.Observation(identifier = "e_time",  text="The time interval for an expiratory breath", code=152612, display="MDC_ATTR_TIME_STAMP_REL", valueType="valueQuantity", value = float(rows.eTime), breath_number=int(rows.ventBN), unit="s")
#    ie_ratio = rs.Observation(identifier = "ie_ratio", text="Inspiratory time divided by expiratory time", code=151832, display="MDC_RATIO_IE", valueType="valueQuantity", value = float(rows.ie_ratio), breath_number=int(rows.ventBN))
#    inst_rr = rs.Observation(identifier = "inst_rr", text="Spontaneous respiration rate, the rate of breaths or inspiratory gas flow initiated by the patient where flow and/or volume is determined by the patient and are delivered with the intention that the breath will be terminated by the patient.", code=151674, display="MDC_RESP_BTSD_PS_RATE", valueType="valueQuantity", value = float(rows.inst_RR), breath_number=int(rows.ventBN), unit="breaths/minute")
#    tve = rs.Observation(identifier = "tve", text="Expired Tidal Volume: Volume of expired gas for all breath and inflation types, reported individually.", code=152664, display="MDC_VOL_AWAY_TIDAL_EXP", valueType="valueQuantity", value = float(rows.tve), breath_number=int(rows.ventBN), unit="mL")
#    tvi = rs.Observation(identifier = "tvi",  text="Inspired Tidal Volume: Volume of inspired gas during each breath, breath type(s) not specified.", code=152660, display="MDC_VOL_AWAY_TIDAL_INSP", valueType="valueQuantity", value = float(rows.tvi), breath_number=int(rows.ventBN), unit="mL")
#    maxF = rs.Observation(identifier = "maxF", text="Maximum airway flow", code=151940, display="MDC_VENT_FLOW", valueType="valueQuantity", value = float(rows.maxF), breath_number=int(rows.ventBN))
#    minF = rs.Observation(identifier = "minF", text="Minimum airway flow", code=151940, display="MDC_VENT_FLOW", valueType="valueQuantity", value = float(rows.minF), breath_number=int(rows.ventBN))
#    maxP = rs.Observation(identifier = "maxP", text="Maximum airway pressure", code=151793, display="MDC_PRESS_AWAY_MAX", valueType="valueQuantity", value = float(rows.minF), breath_number=int(rows.ventBN), unit="cm[H2O]")
#    pip = rs.Observation(identifier = "pip", text="Peak Inspiratory Pressure", code=151817, display="MDC_PRESS_AWAY_INSP_MAX", valueType="valueQuantity", value = float(rows.pip), breath_number=int(rows.ventBN), unit="cm[H2O]")
#    maw = rs.Observation(identifier = "maw", text="Mean airway pressure", code=151795, display="MDC_PRESS_AWAY_MEAN", valueType="valueQuantity", value = float(rows.Maw), breath_number=int(rows.ventBN), unit="cm[H2O]")
#    peep = rs.Observation(identifier = "peep", text="Positive end expiratory pressure", code=151976, display="MDC_VENT_PRESS_AWAY_END_EXP_POS", valueType="valueQuantity", value = float(rows.PEEP), breath_number=int(rows.ventBN), unit="cm[H2O]")
#    minP = rs.Observation(identifier = "min_pressure", text="Minimum ventilation pressure", code=151958, display="MDC_VENT_PRESS_MIN", valueType="valueQuantity", value = float(rows.min_pressure), breath_number=int(rows.ventBN), unit="cm[H2O]")


def makePatient(ptID, name):
    pt_resource = fhirModel.patient.Patient()
    pt_resource.id = pt_id
    pt_resource.name = [fhirModel.humanname.HumanName({'text': fake.name()})]
    return pt_resource

def makePostBundleEntry(resourceName, resource):
    bundle_entry = fhirModel.bundle.BundleEntry()
    bundle_entry.resource = resource
    url = 'http://ec2-52-14-10-32.us-east-2.compute.amazonaws.com:8080/hapi-fhir-jpaserver/fhir/' + str(resourceName)
    bundle_entry.request = fhirModel.bundle.BundleEntryRequest({'url': url,
                                                                'method': 'POST'})
    return bundle_entry
    
if __name__=='__main__':
    ventMapPath = 'D:\\Documents\Health Informatics\\Thesis Paper Resources\\FHIR Implementation of Ventilation Waveform Data\\vent_breath_data\\staging\\*'
    mapping_path = "D:\\Documents\\Health Informatics\\Thesis Paper Resources\\FHIR Implementation of Ventilation Waveform Data\\mappingVentMap.xlsx"
    pt_id = []
#    vent_map = pd.read_excel(mapping_path, sheet_name="Observation_Definitions", index_col=0) 
    # Reading in all the patient files
#    for f in glob.glob(ventMapPath, recursive=True):
#        pathList = f.split(sep="\\")
#        pt_id = pathList[len(pathList) - 1]
#        for f2 in glob.glob(f + "\\*.csv", recursive=True):
#            file_path = f2.split(sep="\\")
#            file_name = file_path[len(file_path) - 1]
#            if "annotations" in pt_id:
#                annotation_df = pd.read_csv(f)
#                annotation_df_with_id = annotation_df[['BN', 'ventBN', 'dbl', 'mt', 'bs', 'dtpi', 'dtpa', 'fa', 'co', 'su', 'vd', 'aNOS', 'wNOS']]
#                annotation_df_with_id['Patient_ID'] = pt_id
#            if "metadata" in file_name:
#                metadata_df = pd.read_csv(f2)
#                breath_observations = process_metadata(metadata_df, pt_id, vent_map)
#            elif "annotation" in pt_id:
#                continue
#            else:
#                breath_data_df = pd.read_csv(f, names=["flow", "pressure"], header=None)

        # Uncomment this to remake the patient resources in the database
    fake = Faker()
    pt_bundle_list = []
    for pt in glob.glob(ventMapPath):
        pt_path_list = pt.split(sep="\\")
        pt_id = pt_path_list[len(pt_path_list) - 1]
        pt_resource = makePatient(pt_id, fake.name())
        bundle_entry = makePostBundleEntry("Patient", pt_resource)
        pt_bundle_list.append(bundle_entry)
    pt_bundle = fhirModel.bundle.Bundle()
    pt_bundle.entry = pt_bundle_list
    pt_bundle.type = 'batch'
    api_url = "http://ec2-52-14-10-32.us-east-2.compute.amazonaws.com:8080/hapi-fhir-jpaserver/fhir/"
    settings = {
        'app_id': 'hapi_fhir_app',
        'api_base': api_url
    }
    smart = client.FHIRClient(settings=settings)
         
def code_not_used():
    # Modifying column names in dataframe
    metadata_df.rename(columns={"I:E ratio":"ie_ratio", "tve:tvi ratio": "tve_tvi_ratio"}, inplace=True)
    
    # Breath time arrays
    breath_start = []
    breath_end = []
    insp_breath_end = []
    insp_breath_interval = []
    exp_breath_interval = []
    
    # Ratios
    ie_ratio = []
    
    # Rates
    inst_rr = []
    
    # Tidal Volume
    tve = []
    tvi = []
    
    # Flow
    maxF = []
    minF = []
    
    # Pressure
    maxP = []
    pip = []
    maw = []
    peep = []
    minP = []
    
    # Metadata parsing
    for rows in metadata_df.itertuples():
        breath_start.append(rs.Observation(identifier = "bs_time", text="The time this breath started", code=67985, display="MDC_ATTR_TIME_STAMP_REL", valueType="valueQuantity", value = float(rows.BS), breath_number=int(rows.ventBN), unit="s"))
        breath_end.append(rs.Observation(identifier = "be_time", text="The time this breath finished", code=67985, display="MDC_ATTR_TIME_STAMP_REL", valueType="valueQuantity", value = float(rows.BE), breath_number=int(rows.ventBN), unit="s"))
        insp_breath_end.append(rs.Observation(identifier = "i_end_time",  text="The time the inspiratory breath finished", code=67985, display="MDC_ATTR_TIME_STAMP_REL", valueType="valueQuantity", value = float(rows.IEnd), breath_number=int(rows.ventBN), unit="s"))
        insp_breath_interval.append(rs.Observation(identifier = "i_time",  text="The time interval for an inspiratory breath", code=152608, display="MDC_ATTR_TIME_STAMP_REL", valueType="valueQuantity", value = float(rows.iTime), breath_number=int(rows.ventBN), unit="s"))
        exp_breath_interval.append(rs.Observation(identifier = "e_time",  text="The time interval for an expiratory breath", code=152612, display="MDC_ATTR_TIME_STAMP_REL", valueType="valueQuantity", value = float(rows.eTime), breath_number=int(rows.ventBN), unit="s"))
        ie_ratio.append(rs.Observation(identifier = "ie_ratio", text="Inspiratory time divided by expiratory time", code=151832, display="MDC_RATIO_IE", valueType="valueQuantity", value = float(rows.ie_ratio), breath_number=int(rows.ventBN)))
        inst_rr.append(rs.Observation(identifier = "inst_rr", text="Spontaneous respiration rate, the rate of breaths or inspiratory gas flow initiated by the patient where flow and/or volume is determined by the patient and are delivered with the intention that the breath will be terminated by the patient.", code=151674, display="MDC_RESP_BTSD_PS_RATE", valueType="valueQuantity", value = float(rows.inst_RR), breath_number=int(rows.ventBN), unit="breaths/minute"))
        tve.append(rs.Observation(identifier = "tve", text="Expired Tidal Volume: Volume of expired gas for all breath and inflation types, reported individually.", code=152664, display="MDC_VOL_AWAY_TIDAL_EXP", valueType="valueQuantity", value = float(rows.tve), breath_number=int(rows.ventBN), unit="mL"))
        tvi.append(rs.Observation(identifier = "tvi",  text="Inspired Tidal Volume: Volume of inspired gas during each breath, breath type(s) not specified.", code=152660, display="MDC_VOL_AWAY_TIDAL_INSP", valueType="valueQuantity", value = float(rows.tvi), breath_number=int(rows.ventBN), unit="mL"))
        maxF.append(rs.Observation(identifier = "maxF", text="Maximum airway flow", code=151940, display="MDC_VENT_FLOW", valueType="valueQuantity", value = float(rows.maxF), breath_number=int(rows.ventBN)))
        minF.append(rs.Observation(identifier = "minF", text="Minimum airway flow", code=151940, display="MDC_VENT_FLOW", valueType="valueQuantity", value = float(rows.minF), breath_number=int(rows.ventBN)))
        maxP.append(rs.Observation(identifier = "maxP", text="Maximum airway pressure", code=151793, display="MDC_PRESS_AWAY_MAX", valueType="valueQuantity", value = float(rows.minF), breath_number=int(rows.ventBN), unit="cm[H2O]"))
        pip.append(rs.Observation(identifier = "pip", text="Peak Inspiratory Pressure", code=151817, display="MDC_PRESS_AWAY_INSP_MAX", valueType="valueQuantity", value = float(rows.pip), breath_number=int(rows.ventBN), unit="cm[H2O]"))
        maw.append(rs.Observation(identifier = "maw", text="Mean airway pressure", code=151795, display="MDC_PRESS_AWAY_MEAN", valueType="valueQuantity", value = float(rows.Maw), breath_number=int(rows.ventBN), unit="cm[H2O]"))
        peep.append(rs.Observation(identifier = "peep", text="Positive end expiratory pressure", code=151976, display="MDC_VENT_PRESS_AWAY_END_EXP_POS", valueType="valueQuantity", value = float(rows.PEEP), breath_number=int(rows.ventBN), unit="cm[H2O]"))
        minP.append(rs.Observation(identifier = "min_pressure", text="Minimum ventilation pressure", code=151958, display="MDC_VENT_PRESS_MIN", valueType="valueQuantity", value = float(rows.min_pressure), breath_number=int(rows.ventBN), unit="cm[H2O]"))
    
    # Breath pressure and flow data parsing
    breath_number = 0
    breath_start_index = 0
    flow = []
    pressure = []
    for breath_data_rows in breath_data_df.itertuples():
        if "S" in str(breath_data_rows.pressure):
            # Parsing out breath number from S:#### in pressure column
            breath_number = breath_data_rows.pressure.split(":")[1]
            breath_start_index = breath_data_rows.Index + 1
        if "BE" in str(breath_data_rows.flow):
            breath_flow = breath_data_df.iloc[breath_start_index:breath_data_rows.Index, 0]
            breath_pressure = breath_data_df.iloc[breath_start_index:breath_data_rows.Index, 0]
            breath_flow_string = ' '.join(breath_flow)
            breath_pressure_string = ' '.join(breath_pressure)
            flow.append(rs.Observation(identifier = "flow", text="Ventilator airway flow", code=151940, display="MDC_VENT_FLOW", valueType="valueSampledData", value = breath_flow_string, breath_number=int(breath_number), origin=0, period=20.0, dimensions=50))
            pressure.append(rs.Observation(identifier = "pressure", text="Airway pressure", code=151956, display="MDC_VENT_PRESS", valueType="valueSampledData", value = breath_pressure_string, breath_number=int(breath_number), origin=0, period=20.0, dimensions=50))
            
    
    conn = db_connect()
    try:
        fb = fhirbase.FHIRBase(conn)
        


    finally:
        conn.close()