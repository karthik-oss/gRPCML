import grpc

import generic_model_pb2
import generic_model_pb2_grpc
import pandas as pd
import numpy as np
import pickle as cp
import base64
from cassandra.cluster import Cluster
import time
#from datetime import datetime as dt
def infer(stub,df):
    df.reset_index(drop=True,inplace=True)
    response = stub.InferModel(generic_model_pb2.msg_dataframe(msg=df.to_json().encode('utf8')))
    ndf=response.msg
    print(ndf)
    print("-------------")


def run():
    #channel = grpc.insecure_channel('localhost:22222')
    channel = grpc.insecure_channel('localhost:9090')
    #channel = grpc.insecure_channel('172.17.0.2:9090')
    stub = generic_model_pb2_grpc.GenericMLServicesStub(channel)
    ######## configure Model Parameters ###############
    windowsize=2 #parameter
    metric_name='metric1'
    df_config=pd.DataFrame([[windowsize,metric_name]],columns=['moving_window_size','metric_name'])
   # metric_name='id_cpu.util'
    #df_config=df_config.append(pd.DataFrame([[4,anomaly_threshold,'Adaptive_Zscore_rolling_median',False,metric_name]],columns=['moving_window_size','anomaly_threshold','model_name','if_infer_data','metric_name']))
    df_config.reset_index(drop=True,inplace=True)
    response1 = stub.ConfigureModelParameters(generic_model_pb2.msg_dataframe(msg=df_config.to_json().encode('utf8')))
    print(response1)



    ######### Data ###################
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect('datakeyspace')
    localtime=0
    traincnt=0
    trainperiod=3 #3 hrs
    trainflg=False
    while True:
        stmt = session.prepare(" SELECT * FROM events where time >="+str(localtime)+"  order by time asc");
        rows = session.execute(stmt);
        df=pd.DataFrame()
        tdf=pd.DataFrame()
	idf=pd.DataFrame()
        for row in rows:
            #print(row[2])
            tdf=pd.DataFrame.from_dict(eval(row[2]), orient="index") ##epg_data
            #print(tdf.shape)
            if (traincnt<=trainperiod):
                df=df.append(tdf.T)
                trainflg=True
            else:
                idf=idf.append(tdf.T)
                #trainflg=False
            localtime=row[1]

        #print(df)
        traincnt=traincnt+1


        if(trainflg): ## update config
            response1 = stub.TrainModel(generic_model_pb2.msg_dataframe(msg=df.to_json().encode('utf8')))
            trainflg=False

        infer(stub,idf) ##training

        time.sleep(1)

if __name__ == "__main__":
    run()
